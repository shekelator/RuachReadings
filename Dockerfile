# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

WORKDIR /ruachReadings

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
# Use Gunicorn with Uvicorn worker to serve the FastAPI ASGI app in production
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "app_fastapi:app", "-b", "0.0.0.0:8080", "-w", "2"]
