import sys
import subprocess


def run_strategy():
    try:
        sys.argv.pop(0)

        args = " ".join(sys.argv)

        subprocess.run(
            f"trader_core {args}",
            shell=True,
            check=True,
        )

        subprocess.run(
            "uvicorn proalgotrader_strategy_runner.main:app --host 127.0.0.1 --port 5555",
            shell=True,
            check=True,
        )
    except Exception as e:
        print(e)
