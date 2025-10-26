# run locally with flask --app app --debug run

from flask import Flask, render_template, request
import readings
import hebcal

app = Flask(__name__)

app.logger.setLevel('INFO')

hebCal = hebcal.HebCal() 

@app.route('/')
def index():
    app.logger.info('Request for index')
    start_date = request.args.get('start_date')
    rawReadingsData = hebCal.getRawReadingsData(start_date)
    services = list(readings.getReadings(rawReadingsData))
    last_date = services[-1].date
    return render_template('readings.html', services=services, last_date=last_date, get_shortened_haftarah=readings.getShortenedHafarah)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/health')
def health():
    return {
        "status": "OK"
    }

if __name__ == '__main__':
    import os
    # Check if we're in development mode
    debug_mode = os.environ.get('FLASK_DEBUG', '0') == '1'
    host = os.environ.get('FLASK_RUN_HOST', '127.0.0.1')
    port = int(os.environ.get('FLASK_RUN_PORT', '5000'))
    
    app.run(debug=debug_mode, host=host, port=port)
