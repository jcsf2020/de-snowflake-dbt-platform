import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional

def load_json(path: Path):
    try:
        return json.loads(path.read_text())
    except FileNotFoundError:
        return None


def _manifest_resource_type(manifest, unique_id: str) -> str:
    """Lookup resource_type from manifest using the unique_id."""
    if not unique_id or not isinstance(manifest, dict):
        return "unknown"
    for section in (
        "nodes",
        "sources",
        "snapshots",
        "macros",
        "exposures",
        "metrics",
        "semantic_models",
        "unit_tests",
        "saved_queries",
    ):
        d = manifest.get(section, {}) or {}
        node = d.get(unique_id)
        if isinstance(node, dict):
            rt = node.get("resource_type")
            if rt:
                return rt
    return "unknown"


def _duration_from_timing(timing) -> Optional[float]:
    """Sum durations from dbt timing entries, deriving when duration is missing."""
    total = 0.0
    found = False
    for item in timing or []:
        if not isinstance(item, dict):
            continue
        dur = item.get("duration")
        if isinstance(dur, (int, float)):
            total += float(dur)
            found = True
            continue
        start = item.get("started_at")
        end = item.get("completed_at")
        if start and end:
            try:
                s = datetime.fromisoformat(start.replace("Z", "+00:00"))
                e = datetime.fromisoformat(end.replace("Z", "+00:00"))
                total += (e - s).total_seconds()
                found = True
            except Exception:
                continue
    return total if found else None

RUN_RESULTS = Path("target/run_results.json")
MANIFEST = Path("target/manifest.json")
OUT_DIR = Path("orchestration/logs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    data = load_json(RUN_RESULTS) or {}
    manifest = load_json(MANIFEST)

    results = data.get("results", [])
    elapsed = data.get("elapsed_time", None)

    # Aggregate
    totals = {"success": 0, "fail": 0, "error": 0, "skipped": 0, "warn": 0}
    by_resource = {}
    rows = []

    for r in results:
        status_raw = (r.get("status") or "").lower()
        status = "success" if status_raw == "pass" else status_raw
        rid = r.get("unique_id", "")
        resource = _manifest_resource_type(manifest, rid)
        name = r.get("node", {}).get("name") if isinstance(r.get("node"), dict) else None
        if not name:
            # fallback: last token after dots
            name = rid.split(".")[-1] if rid else "unknown"

        exec_s = r.get("execution_time")
        if not isinstance(exec_s, (int, float)):
            exec_s = _duration_from_timing(r.get("timing"))

        # status mapping
        if status in totals:
            totals[status] += 1
        else:
            totals["warn"] += 1

        by_resource.setdefault(resource, {"count": 0, "success": 0, "fail": 0, "error": 0, "skipped": 0, "warn": 0})
        by_resource[resource]["count"] += 1
        if status in by_resource[resource]:
            by_resource[resource][status] += 1
        else:
            by_resource[resource]["warn"] += 1

        rows.append({
            "resource_type": resource,
            "status": status,
            "name": name,
            "unique_id": rid,
            "exec_seconds": round(exec_s, 4) if isinstance(exec_s, (int, float)) else "",
        })

    # Top slowest
    slow = [r for r in rows if isinstance(r["exec_seconds"], (int, float))]
    slow.sort(key=lambda x: x["exec_seconds"], reverse=True)
    top10 = slow[:10]

    ts = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    summary = {
        "generated_utc": ts,
        "run_results_path": str(RUN_RESULTS),
        "elapsed_seconds": elapsed,
        "totals": totals,
        "by_resource_type": by_resource,
        "top10_slowest": top10,
    }

    out_json = OUT_DIR / "metrics_latest.json"
    out_csv = OUT_DIR / "metrics_latest.csv"
    out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=True))

    # CSV of all nodes
    with out_csv.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["resource_type", "status", "name", "unique_id", "exec_seconds"])
        w.writeheader()
        w.writerows(rows)

    print(f"OK: wrote {out_json} and {out_csv}")
    print(f"Totals: {totals} | elapsed_seconds={elapsed}")

if __name__ == "__main__":
    main()
