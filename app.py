# run locally with flask --app app --debug run

from flask import Flask, render_template
import readings

app = Flask(__name__)


@app.route('/')
def index():
    rawReadingsData = readings.getRawReadingsData()
    services = readings.getReadings(rawReadingsData)
    return render_template('readings.html', readings=services)


