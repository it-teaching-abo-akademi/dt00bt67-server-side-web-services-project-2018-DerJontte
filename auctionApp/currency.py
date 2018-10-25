from urllib import request
import json
from django.http import HttpResponse
from django.views import View
from auctionApp.models import ExchangeRate

class Currency:
    def exchange(input, code):
        return round(input * Currency.get_rate(code), 2)

    def get_rate(code):
        with open('./testdata.json', 'r') as infile:
            data = infile.read().replace('\n', '')
        parsed = json.loads(data)
        return parsed['rates'][code]

    def code_list(**type):
        with open('./testdata.json', 'r') as infile:
            data = infile.read().replace('\n', '')
        parsed = json.loads(data)
        keylist = []
        for key in parsed['rates'].keys():
            if type.get('type') == 'pairlist':
                keylist.append([key, key])
            else:
                keylist.append(key)
            rate = parsed['rates'][key]
#            pair = ExchangeRate(code=key, rate=rate)
#            pair.save()
        return keylist

    # def fetch_rates():
    #     url = 'http://data.fixer.io/api/latest?access_key=5833765f3462250964a319f06fd6b3d1&format=1'
    #     response = request.urlopen(url)
    #     data = response.read()
    #     text = data.decode('utf-8')
    #     parsed = json.loads(data)
    #     for rate in parsed['rates'].items():
    #         tosave = ExchangeRate(key=rate[0], value=rate[1])
    #         tosave.save()
