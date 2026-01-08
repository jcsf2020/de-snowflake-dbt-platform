import json
from pathlib import Path
from datetime import datetime, timezone
import csv

RUN_RESULTS = Path("target/run_results.json")
OUT_DIR = Path("orchestration/logs")
OUT_DIR.mkdir(parents=True, exist_ok=True)

def main():
    data = json.loads(RUN_RESULTS.read_text())

    results = data.get("results", [])
    elapsed = data.get("elapsed_time", None)

    # Aggregate
    totals = {"success": 0, "fail": 0, "error": 0, "skipped": 0, "warn": 0}
    by_resource = {}
    rows = []

    for r in results:
        status = (r.get("status") or "").lower()
        rid = r.get("unique_id", "")
        resource = r.get("resource_type", "unknown")
        name = r.get("node", {}).get("name") if isinstance(r.get("node"), dict) else None
        if not name:
            # fallback: last token after dots
            name = rid.split(".")[-1] if rid else "unknown"

        exec_s = None
        t = r.get("timing", [])
        # dbt stores timings array; we want total execution time if present
        try:
            # find "execute" timing if exists
            for item in t:
                if item.get("name") == "execute":
                    exec_s = item.get("duration")
                    break
            if exec_s is None:
                # sum all durations as fallback
                exec_s = sum(item.get("duration", 0) for item in t if isinstance(item, dict))
        except Exception:
            exec_s = None

        # status mapping
        if status in totals:
            totals[status] += 1
        else:
            # treat unknown as warn-ish
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
