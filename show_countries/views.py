import json
import random
import re

import requests
from django.shortcuts import render

def home(request):
    if request.method == 'POST':
        continent = request.POST.get('continent')
        number_str = request.POST.get('number')
        number = int(number_str)
        print("requested")

        countries_list = retrieve_region(continent, number)

        # check if given continent name exist
        if (countries_list == 0):
            print("Continent name doesn't match any region")
            validation_message = "Continent does not exist"
            return render(request, 'home.html', {'validation_message': validation_message})

        countries_info = retrieve_country_info(countries_list)

        return render(request, 'home.html', {'countries': countries_info})
    else:
        return render(request, 'home.html')


def retrieve_region(region, number):
    regions = {
        "europe": "EU",
        "asia": "AS",
        "africa": "AF",
        "antarctica": "AN",
        "north america": "NA",
        "oceania": "OC",
        "south america": "SA",
    }
    # user input to lowercase letters
    lowercase_reg = region.lower()

    # check if user input match possible continents
    try:
        region_code = regions[lowercase_reg]
    except:
        print("Region not exist")
        return 0

    url = 'https://countries.trevorblades.com/graphql'

    # graphql query to take country names
    query = '''
    query Query($code: ID!) {
        continent(code: $code) {
            countries {
                name
        }
      }
    }
    '''

    payload = {
        'query': query,
        'variables': {
            'code': region_code
        }
    }

    response = requests.post(url=url, json=payload)

    result_json = response.text
    result = json.loads(result_json)
    # number of all countries in region
    countries_len = len(result['data']['continent']['countries'])
    print(response.status_code)
    print(result)
    countries_arr = []

    # get random countries
    random_numbers = random.sample(range(0, countries_len - 1), number)
    for i in random_numbers:
        country = result['data']['continent']['countries'][i]['name']
        country_new = re.sub(r'\[.*?\]', '', country)
        countries_arr.append(country_new)
    # sort countries in alphabetical order
    sorted_countries = sorted(countries_arr)
    print(countries_arr)

    return sorted_countries


def retrieve_country_info(countries_arr):
    ret_arr = []
    for country in countries_arr:
        url = "https://restcountries.com/v3.1/name/{}".format(country)
        response_json = requests.get(url=url)
        result = json.loads(response_json.text)
        try:
            name = result[0]['name']['official']
        except:
            name = country
        try:
            capital = result[0]['capital'][0]
        except:
            capital = "No information found!"
        try:
            population_str = result[0]['population']
            population = int(population_str)
        except:
            population = "No information found!"
        try:
            currencies = result[0]['currencies']
            currency_names = [value['name'] for value in currencies.values()]
        except:
            currency_names[0] = "No information found!"
        try:
            subregion = result[0]['subregion']
        except:
            subregion = "No information found!"
        try:
            languages = result[0]['languages']
            languages_names = list(languages.values())
        except:
            languages_names[0] = "No information found!"

        # dict with country and information
        country = {
            'name': name,
            'capital': capital,
            'population': population,
            'currencies': currency_names,
            'subregion': subregion,
            'languages': languages_names
        }

        ret_arr.append(country)

    print(ret_arr)
    return ret_arr
