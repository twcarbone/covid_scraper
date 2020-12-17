## **COVID Scraper**
#### Overview
This project retrieves data from the Electric Boat
[EBLanding](https://eblanding.com/covid-19-case-report-summary/) COVID-19 Case Report
Summary website and plots it in interesting ways.
#### Execution
Run `python3 main.py` from your terminal.
#### Methods
`main.py` is the driver that calls all functions.

`scrape.py` uses the `requests` and `beautifulsoup` libraries to make the http
request to the URL and parse the html.

`covid_case.py` contains a single class that is a template for one COVID-19 case
at Electric Boat.

`analyze.py` contains functions that organize the COVID case data by facility,
department, etc.

`plot.py` plots the data using the `matplotlib` library.

`db.py` is currently in testing, and adds COVID case data to a PostgreSQL
database.

`log.py` sets up a logger that logs to `covid.log`, which is not under version
control.
#### Example Output
![Example Output](figure1.png?raw=true)
