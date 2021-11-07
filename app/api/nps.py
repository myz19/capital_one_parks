from flask import Blueprint, Request, Response, render_template, request, session
import httpx
import random

parks_blueprint = Blueprint('parks', __name__, url_prefix='/parks')

def get_data(entity, param = {}):
    with httpx.Client() as client:
        client.headers = {"X-Api-Key":"5n3ehepOD1fptaOs9Yd3vCydcC6hZL8EEByTfIEu"}
        url = f'https://developer.nps.gov/api/v1/{entity}'
        params = param
        resp = client.get(url = url, params = params)
        data = resp.json()
    return data

@parks_blueprint.route('/activities/')
def get_activities():
    data = get_data('activities')
    return render_template('main_page.html', data = data['data'])

@parks_blueprint.route('/activities/<activity>/state-parks')
def get_parks(activity):
    limit = int(request.args.get('limit'))
    start = int(request.args.get('start'))
    # if session.get("park_data", '') == '':
    #     session["park_data"] = get_data('activities/parks', {'id': activity})['data'][0]
    session["park_data"] = get_data('activities/parks', {'id': activity})['data'][0]
    # return {"message": session["park_data"]}
    number_of_parks = len(session["park_data"]["parks"])
    name_of_activity = session["park_data"]["name"]
    end = 0
    hide_next_menu = False
    if (start+limit > number_of_parks):
        end = number_of_parks
        hide_next_menu = True
    else:
        end = start+limit
    print(f'start is {start} and end is {end}')
    parks_list = []
    for park in session["park_data"]["parks"][start:end]:
        _data = get_data('parks', {'parkCode': park['parkCode']})['data']
        if len(_data) != 0:
            park_dict = {
                'fullName': _data[0]['fullName'],
                'parkCode': _data[0]['parkCode'],
                'description': _data[0]['description'],
                'image': _data[0]['images'][0]['url']
            }
            parks_list.append(park_dict)
    # print(number_of_parks)
    url = request.path+"?limit=10&start="+str(end)
    return render_template('listofparks.html', data = parks_list, url = url, hide = hide_next_menu, name_activity = name_of_activity)

@parks_blueprint.route('/activities/park/<parkcode>')
def get_park_data(parkcode):
    _data = get_data('parks', {'parkCode': parkcode})['data'][0]
    park_details = {}
    for _address in _data['addresses']:
        if _address["type"] == "Physical":
            park_details["address"] =_address # dictionary
    
    for _contact in _data['contacts']["phoneNumbers"]:
        if _contact['type'] == "Voice":
            park_details['phoneNumber'] = _contact # dictionary
    park_details['fullName'] = _data['fullName']
    park_details["images"] = _data['images'] # list of dictionary
    park_details["url"] = _data['url']
    park_details["directionInfo"] = _data['directionsInfo']
    park_details['fees'] = _data['entranceFees'] # dictionary
    park_details['hours'] = _data['operatingHours'][0]['standardHours'] # dictionary
    
    # return {'message': park_details}
    return render_template('parkphotos.html', data = park_details)