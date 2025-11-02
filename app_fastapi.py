from typing import Optional
import asyncio

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import readings
import hebcal

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# mount static files so request.url_for('static', path=...) works in templates
app.mount("/static", StaticFiles(directory="static"), name="static")

# hebcal is currently synchronous; run blocking calls in a thread to avoid blocking the event loop
hebCal = hebcal.HebCal()

async def get_raw_readings(start_date: Optional[str]):
    return await asyncio.to_thread(hebCal.getRawReadingsData, start_date)

async def get_services(raw_readings):
    # readings.getReadings may be a generator or blocking; evaluate in a thread
    return await asyncio.to_thread(lambda: list(readings.getReadings(raw_readings)))


@app.get("/", response_class=HTMLResponse)
async def index(request: Request, start_date: Optional[str] = None):
    raw = await get_raw_readings(start_date)
    services = await get_services(raw)
    last_date = services[-1].date if services else None
    return templates.TemplateResponse(
        request,
        "readings.html",
        {
            "request": request,
            "services": services,
            "last_date": last_date,
            "get_shortened_haftarah": readings.getShortenedHafarah,
        },
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(request, "about.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "OK"}


if __name__ == "__main__":
    # quick developer run
    import uvicorn

    uvicorn.run("app_fastapi:app", host="0.0.0.0", port=8080, reload=True)
