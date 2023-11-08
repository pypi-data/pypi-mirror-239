import sys
import subprocess

from multiprocessing import Pool


def run_core():
    sys.argv.pop(0)

    args = " ".join(sys.argv)

    subprocess.run(
        f"trader_core {args}",
        shell=True,
        check=True,
    )


def run_api():
    subprocess.run(
        "uvicorn proalgotrader_strategy_runner.main:app --host 127.0.0.1 --port 5555",
        shell=True,
        check=True,
    )


def run_processes(process):
    process()


def run_strategy():
    try:
        processes = (run_api, run_core)
        pool = Pool(processes=3)
        pool.map(run_processes, processes)
    except Exception as e:
        print(e)
