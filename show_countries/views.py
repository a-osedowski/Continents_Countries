import json
import random
import re

import requests
from django.http import HttpResponse
from django.shortcuts import render
# Create your views here.
from django.views.generic import CreateView


def home(request):

    if request.method == 'POST':
        continent = request.POST.get('continent')
        number_str = request.POST.get('number')
        number = int(number_str)
        print("requested")

        if (number < 2 or number >10):
            print("Number should be between 2 and 10")
            validation_message = "Number should be between 2 and 10"
            return render(request, 'home.html', {'validation_message': validation_message})

        countries_list = retrieve_region(continent, number)

        if (countries_list == 0):
            print("Continent name doesn't match any region")
            validation_message = "Continent name does not match any region"
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
        "south africa": "SA",
    }
    lowercase_reg = region.lower()

    try:
        region_code = regions[lowercase_reg]
    except:
        print("Region not exist")
        return 0



    url = 'https://countries.trevorblades.com/graphql'

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
    countries_len = len(result['data']['continent']['countries'])
    print(response.status_code)
    print(result)
    countries_arr = []
    for i in range(number):
        random_number = random.randint(0, countries_len-1)
        country = result['data']['continent']['countries'][random_number]['name']
        country_new = re.sub(r'\[.*?\]', '', country)
        countries_arr.append(country_new)
    print(countries_arr)

    return countries_arr

def retrieve_country_info(countries_arr):
    ret_arr = []
    i = 0
    for country in countries_arr:
        in_arr = []
        url = "https://restcountries.com/v3.1/name/{}".format(country)
        response_json = requests.get(url=url)
        result = json.loads(response_json.text)
        print(result[0]['name']['official'])
        currencies = result[0]['currencies']
        currency_names = [value['name'] for value in currencies.values()]
        languages = result[0]['languages']
        languages_names = list(languages.values())
        country = {
            'name': result[0]['name']['official'],
            'capital': result[0]['capital'][0],
            'population': result[0]['population'],
            'currencies': currency_names,
            'subregion': result[0]['subregion'],
            'languages': languages_names
        }
        i += 1

        ret_arr.append(country)

    print(ret_arr)
    return ret_arr
