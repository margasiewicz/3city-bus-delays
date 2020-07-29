import json
from urllib.request import urlopen
from datetime import datetime


class Timetable:
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

    def print_delay(self, stop_id):
        current_time = datetime.now().strftime("%H:%M")
        with open('bus_numbers.json') as json_file:
            bus_numbers = json.load(json_file)
        with urlopen(f"https://ckan2.multimediagdansk.pl/delays?stopId={stop_id}") as url:
            data = json.loads(url.read().decode())
        print('Godzina:', current_time.rjust(46))
        print('')
        print('Linia'.ljust(6),'Kierunek'.ljust(22)[:22],'Przyjazd'.ljust(19))
        for item in data['delay']:
            #get current and estimated times and convert them to datetime objects
            estimated_time = datetime.strptime(item["estimatedTime"], '%H:%M')
            curr_time = datetime.strptime(current_time, '%H:%M')

            time_delta = (estimated_time-curr_time).seconds//60
            route_id = str(item["routeId"])

            print(  bus_numbers[route_id].ljust(6), 
                    item["headsign"].ljust(22)[:22], 
                    str(time_delta), 'min')
    def json_delay(self, stop_id):
        json_delays = []
        current_time = datetime.now().strftime("%H:%M")
        with open('bus_numbers.json') as json_file:
            bus_numbers = json.load(json_file)
        with urlopen(f"https://ckan2.multimediagdansk.pl/delays?stopId={stop_id}") as url:
            data = json.loads(url.read().decode())
        for item in data['delay']:
            estimated_time = datetime.strptime(item["estimatedTime"], '%H:%M')
            curr_time = datetime.strptime(current_time, '%H:%M')
            time_delta = (estimated_time-curr_time).seconds//60
            route_id = str(item["routeId"])
            dict_for_appending = {
                'route_id':bus_numbers[route_id],
                'headsign':item["headsign"],
                'delay_mins':time_delta
            }
            json_delays.append(dict_for_appending)

        json_delays = json.dumps(json_delays, indent=4)
        return json_delays
# t = Timetable()
# delay = t.json_delay(39100)

# print(type(delay))