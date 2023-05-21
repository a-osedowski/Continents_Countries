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

        countries_list = retrieve_region(continent)
        if (countries_list == 0):
            print("Continent name doesn't match any region")
            validation_message = "Continent name does not match any region"
            return render(request, 'home.html', {'validation_message': validation_message})

        if (number < 2 or number >10):
            print("Number should be between 2 and 10")
            validation_message = "Number should be between 2 and 10"
            return render(request, 'home.html', {'validation_message': validation_message})

        return render(request, 'home.html')
    else:
        return render(request, 'home.html')


def retrieve_region(region):
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
                code
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

    result = response.text
    print(response.status_code)
    print(result)
    return result


