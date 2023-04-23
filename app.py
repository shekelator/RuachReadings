# run locally with flask --app app --debug run

from flask import Flask, render_template, request
import readings

app = Flask(__name__)


@app.route('/')
def index():
    start_date = request.args.get('start_date')
    rawReadingsData = readings.getRawReadingsData(start_date)
    services = list(readings.getReadings(rawReadingsData))
    last_date = services[-1].date
    return render_template('readings.html', services=services, last_date=last_date, get_shortened_haftarah=readings.getShortenedHafarah)

@app.route('/about/')
def about():
    return render_template('about.html')
