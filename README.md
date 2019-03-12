# ISO-3166 Scraper

As the project name suggests, this code scrapes ISO 3166-1 data from the Internet. The scraper aggregates data from two sources, the [Wikipedia ISO 3166-1 page](http://en.wikipedia.org/wiki/ISO_3166-1#Officially_assigned_code_elements) for alpha, numeric and [ISO 3166-2](https://en.wikipedia.org/wiki/ISO_3166-2) subdivision codes, and the [UN Statistics](https://unstats.un.org/unsd/methodology/m49/overview/) site for regional and sub-regional codes. The scraped data is saved in both CSV and JSON file formats.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

The script requires Python 3.x and makes use of the Requests and BeautifulSoup packages.

### Installing

Clone the git repository and enter the local folder.

```
git clone https://github.com/danagle/iso3166_scraper.git
cd iso3166_scraper
```

Install the required packages if you haven't already done so.

```
pip install -r requirements.txt
```

## Running the script

Execute the Python script.

```
python scrape_iso3166.py
```

This will perform the web scrape task and save the results.

```
Scraping Wikipedia...
Data found for 249 countries.
Scraping United Nations M49 data...
Unmatched data found: 1
[{'region_code': '150', 'region_name': 'Europe', 'sub_region_code': '154', 'sub_region_name': 'Northern Europe', 'intermediate_region_code': '830', 'intermediate_region_name': 'Channel Islands', 'name': 'Sark', 'iso_alpha_3': ''}]
Saving JSON file... iso3166.json
Saving CSV file... iso3166.csv
```

## Built With

* [Python 3](https://www.python.org/) - Python is a programming language that lets you work quickly
and integrate systems more effectively.
* [Requests](http://docs.python-requests.org/) - Simple HTTP library for Python.
* [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/) - Python library for pulling data out of HTML content.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

