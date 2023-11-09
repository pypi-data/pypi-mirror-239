import subprocess

import sys

from apscheduler.schedulers.background import BackgroundScheduler

from apscheduler.triggers.cron import CronTrigger

from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse


def run_core():
    args = "".join(sys.argv[1:])

    subprocess.run(
        f"trader_core {args}",
        shell=True,
        check=True,
    )


async def on_startup():
    trigger = CronTrigger(
        year="*", month="*", day="*", hour="17", minute="58", second="1"
    )

    scheduler = BackgroundScheduler()

    scheduler.add_job(
        run_core,
        trigger=trigger,
        name="scheduled",
    )

    scheduler.add_job(
        run_core,
        name="instant",
    )

    scheduler.start()


app = FastAPI(on_startup=[on_startup])


@app.get("/")
async def status(request: Request):
    return JSONResponse(
        {
            "status": "okay",
        }
    )
