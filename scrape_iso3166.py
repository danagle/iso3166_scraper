from bs4 import BeautifulSoup
import codecs
import csv
import json
import requests

WIKIPEDIA_URL = 'https://en.wikipedia.org/wiki/ISO_3166-1'
UNSTATS_URL = 'https://unstats.un.org/unsd/methodology/m49/overview/'

# Dictionary to store the data
wiki_data = {}

# First scrape the Wikipedia page
print("Scraping Wikipedia...")

content = requests.get(WIKIPEDIA_URL).text

soup = BeautifulSoup(content, 'html.parser')

tables = soup.find_all('table', {'class': 'wikitable sortable'})
# We're only interested in the second table `Current codes`
for row in tables[1].find_all('tr'):
    row_data = row.find_all('td')
    if len(row_data) > 0:
        country_name, iso_alpha_2, iso_alpha_3, numeric_code, iso_3166_2, _ = row_data
        country = {}
        # Only take the country name, ignore the markup for the flag
        country['name'] = country_name.find_all('a')[-1].string.strip()
        country['alpha_2'] = iso_alpha_2.span.string.strip()
        country['alpha_3'] = iso_alpha_3.span.string.strip()
        country['numeric_code'] = numeric_code.span.string.strip()
        country['iso_3166_2'] = iso_3166_2.a.string.strip()
        wiki_data[country['alpha_3']] = country

print("Data found for %s countries." % len(wiki_data))

print("Scraping United Nations M49 data...")

# There may be additional countries in the UN data
unmatched_data = []

content = requests.get(UNSTATS_URL).text

soup = BeautifulSoup(content, 'html.parser')

table = soup.find(id='downloadTableEN')

for row in table.tbody.find_all('tr'):
    sanitized_data = [s if s is not None else '' for s in [td.string for td in row.find_all('td')]]
    _, _, region_code, region_name, sub_region_code, sub_region_name, intermediate_region_code, intermediate_region_name, country_name, _, iso_alpha_3, _, _, _, _ = sanitized_data
    country = {}
    country['region_code'] = region_code
    country['region_name'] = region_name
    country['sub_region_code'] = sub_region_code
    country['sub_region_name'] = sub_region_name
    country['intermediate_region_code'] = intermediate_region_code
    country['intermediate_region_name'] = intermediate_region_name
    country['name'] = country_name
    country['iso_alpha_3'] = iso_alpha_3
    # Merge the dictionaries
    if iso_alpha_3 in wiki_data:
        wiki_country = wiki_data[iso_alpha_3]
        wiki_data[iso_alpha_3] = { **wiki_country, **country }
    else:
        unmatched_data.append(country)

if (len(unmatched_data) > 0) :
    print("Unmatched data found: %s" % len(unmatched_data))
    print(unmatched_data)

# Transform the wiki_data dictionary to a list
data = list(wiki_data.values())

# Write data to JSON file
json_filename = 'iso3166.json'
print("Saving JSON file... %s" % json_filename)
with codecs.open(json_filename, encoding='utf-8', mode='w+') as jsonfile:
    json.dump(data, jsonfile, sort_keys=True, indent=2, ensure_ascii=False)

# Write data to CSV file
csv_filename = 'iso3166.csv'
print("Saving CSV file... %s" % csv_filename)
csv_columns = sorted(data[0].keys())
with open(csv_filename, 'w+') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
    writer.writeheader()
    for country in wiki_data:
        writer.writerow(wiki_data[country])