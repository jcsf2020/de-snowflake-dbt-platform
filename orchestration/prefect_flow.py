from prefect import flow, task
import subprocess
import sys

@task(log_prints=True, retries=1, retry_delay_seconds=30)
def run_cmd(cmd: list[str]):
    print(f"Running command: {' '.join(cmd)}")
    result = subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {result.returncode}")

@flow(name="dbt_snowflake_pipeline")
def dbt_pipeline():
    run_cmd(["dbt", "deps"])
    run_cmd(["dbt", "build"])

if __name__ == "__main__":
    dbt_pipeline()
