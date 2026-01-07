from prefect import flow, task, get_run_logger
import subprocess
from datetime import datetime
from pathlib import Path
import time

LOG_DIR = Path("orchestration/logs")

def _run_and_log(cmd: list[str], log_name: str):
    logger = get_run_logger()
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    log_file = LOG_DIR / f"{log_name}_{ts}.log"
    start = time.time()

    logger.info(f"Starting command: {' '.join(cmd)}")
    with log_file.open("w") as f:
        proc = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
        )
        for line in proc.stdout:
            f.write(line)
            logger.info(line.rstrip())

    rc = proc.wait()
    duration = round(time.time() - start, 2)
    logger.info(f"Finished with exit code={rc} in {duration}s. Log: {log_file}")

    if rc != 0:
        tail = log_file.read_text()[-2000:]
        raise RuntimeError(f"Command failed (rc={rc}). Tail:\n{tail}")

@task(retries=1, retry_delay_seconds=30)
def run_cmd(cmd: list[str], log_name: str):
    _run_and_log(cmd, log_name)

@flow(name="dbt_snowflake_pipeline")
def dbt_pipeline():
    run_cmd(["dbt", "deps"], "dbt_deps")
    run_cmd(["dbt", "build"], "dbt_build")

if __name__ == "__main__":
    dbt_pipeline()
