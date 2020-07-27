import json
from urllib.request import urlopen
from termcolor import colored
from datetime import datetime


class Rozklad:

    def update_stops_json(self):
        today = datetime.today().strftime('%Y-%m-%d')
        with urlopen('https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/4c4025f0-01bf-41f7-a39f-d156d201b82b/download/stops.json')\
        as url_json:
            stops = url_json.read()
            stops = json.loads(stops)
            stops_dict = {}
            for item in stops[today]["stops"]:
                stop_name = item['stopDesc']
                stop_id = item['stopId']
                if stop_name in stops_dict:
                    try:
                        stops_dict.get(stop_name).append(stop_id)
                    except:
                        pass
                else:
                    stops_dict[stop_name] = [stop_id]
            
            with open('stops.json', 'w') as outfile:
                json.dump(stops_dict, outfile, sort_keys=True, indent=4)



    def update_bus_numbers_json(self):
        today = datetime.today().strftime('%Y-%m-%d')
        with urlopen("https://ckan.multimediagdansk.pl/dataset/c24aa637-3619-4dc2-a171-a23eec8f2172/resource/22313c56-5acf-41c7-a5fd-dc5dc72b3851/download/routes.json")\
        as url_json:
            bus_numbers = url_json.read()
            bus_numbers = json.loads(bus_numbers)
            bus_numbers_dict = {}
            for item in bus_numbers[today]['routes']:
                route_name = item['routeShortName']
                route_id = item['routeId']
                if  route_id in bus_numbers_dict:
                    pass
                else:
                    bus_numbers_dict[route_id] = route_name
            
            with open('bus_numbers.json', 'w') as outfile:
                json.dump(bus_numbers_dict, outfile, sort_keys=False, indent=4)


rozklad = Rozklad()
rozklad.update_stops_json()