# syntax=docker/dockerfile:1

FROM python:3.12-slim-bookworm

WORKDIR /ruachReadings

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

# CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]
CMD [ "gunicorn", "app:app" ]
