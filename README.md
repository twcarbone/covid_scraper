## **COVID Scraper**
#### Overview
This project retrieves data from the Electric Boat [EBLanding](https://eblanding.com/covid-19-case-report-summary/) COVID-19 Case Report Summary website and plots it in interesting ways.
#### Methods
`main.py` is the driver that calls all functions.

`get_web_data.py` uses the `requests` and `beautifulsoup` libraries to make the http request to the URL and parse the html.

`covid_classes.py` contains a single class that is a template for one COVID-19 case at Electric Boat.

`slice_data.py` contains functions the organize the COVID case datat by facility, department, etc.

`plot_data.py` plots the data using the 'matplotlib' library.

`postgres_db.py` is currently in testing, and adds COVID case data to a PostgreSQL database.

