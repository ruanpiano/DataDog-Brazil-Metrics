from datadog import initialize, api
import json
import requests
import pprint
import time

options = {
	'api_key': '858af784e234d903aec234c68a0af14e',
	'app_key': '46596234fa9a2c08bbd61cdebf99e5af015a16b3'
}
initialize(**options)

COVID_ENDPOINT = "https://brasil.io/api/dataset/covid19/caso/data?format=json&is_last=True"

def main():
    r = requests.get(url = COVID_ENDPOINT)
    dataset = r.json() 
    notTags = ['is_last','deaths','death_rate', 'confirmed_per_100k_inhabitants', 'confirmed','order_for_place','date','estimated_population_2019','city_ibge_code']

    for i, data in enumerate(dataset['results']):
        tags = []
        for element in data:
            if element in notTags: 
                continue
            key = element
            value = data[element]
            if value == None:
                value = 0  
            if element == "state":
                if str(value).lower() in ['am','rr','ap','pa','to','ro','ac']: tags.append("regiao:norte")
                if str(value).lower() in ['ma','pi','ce','rn','pe','pb','se','al','ba']: tags.append("regiao:nordeste")
                if str(value).lower() in ['mt','ms','go','df']: tags.append("regiao:centro-oeste")
                if str(value).lower() in ['sp','rj','es','mg']: tags.append("regiao:sudeste")
                if str(value).lower() in ['pr','rs','sc']: tags.append("regiao:sul")
            tags.append(str(key)+":"+str(value))

        value = data['deaths'] if data['deaths'] != None else 0
        api.Metric.send(metric="brazil.covid19.deaths", points=value, tags=tags) 
        value = data['confirmed'] if data['confirmed'] != None else 0
        api.Metric.send(metric="brazil.covid19.confirmed", points=value, tags=tags) 
        value = data['confirmed_per_100k_inhabitants'] if data['confirmed_per_100k_inhabitants'] != None else 0
        api.Metric.send(metric="brazil.covid19.confirmed_per_100k_inhabitants", points=value, tags=tags)        
        value = data['death_rate'] if data['death_rate'] != None else 0
        api.Metric.send(metric="brazil.covid19.death_rate", points=value, tags=tags)  
        value = data['estimated_population_2019'] if data['estimated_population_2019'] != None else 0
        api.Metric.send(metric="brazil.covid19.estimated_population_2019", points=value, tags=tags)  
        print(str(i+1)+"/"+str(len(dataset['results'])))      


        



main()