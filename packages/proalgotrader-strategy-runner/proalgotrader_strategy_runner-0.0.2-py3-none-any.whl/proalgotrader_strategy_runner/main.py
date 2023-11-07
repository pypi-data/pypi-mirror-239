from fastapi import FastAPI, Request

from fastapi.responses import JSONResponse

app = FastAPI()


@app.get("/")
async def status(request: Request):
    return JSONResponse(
        {
            "status": "okay",
        }
    )
