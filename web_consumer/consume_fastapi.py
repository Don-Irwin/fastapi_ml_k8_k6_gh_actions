from includes import *
from flask import Blueprint
import os

consume_fastapi = Blueprint('consume_fastapi', __name__)

from libraries.data_objects import data_objects as do


@consume_fastapi.route('/consume_fastapi_start', methods=['POST', 'GET'])
def consume_fastapi_start():
        res = make_response(render_template('pages/section_content/placeholder.consume_fastapi.html',
        section_number="five"))
        return res

def create_home_request(form):
       hr = dict()
       hr["MedInc"] = float(request.form["medinc_text"])
       hr["HouseAge"] = float(request.form["houseage_text"])
       hr["AveRooms"]  = float(request.form["averooms_text"])
       hr["AveBedrms"] = float(request.form["avebedrms_text"])
       hr["Population"] = float(request.form["population_text"])
       hr["AveOccup"] = float(request.form["aveoccup_text"])
       hr["Latitude"] = float(request.form["lat_text"])
       hr["Longitude"] = float(request.form["long_text"])
       return hr

import requests

def insert_newlines(string, every=64):
    return '\\n'.join(string[i:i+every] for i in range(0, len(string), every))

def execute_fastapi_call(json_post):
    try:
        url = os.environ.get("ca_linear_model_api_url","http://frontend:8000") + "/predictitem"
        r = requests.post(url, json=json_post)
        return url,r.status_code,json.dumps(r.json(),indent=1)
    except Exception as ex:
        return_dict=dict()
        return_dict["url"]=url
        return_dict["status_code"]=r.status_code if "r" in locals() else "Hard Error"
        return_dict["message"]=str(ex)
        return url,"Hard Error",json.dumps(return_dict,indent=1)


@consume_fastapi.route('/health', methods=['POST', 'GET'])
def check_health(popout = False):
        res = "healthy"

        return res

@consume_fastapi.route('/consume_fastapi', methods=['POST', 'GET'])
def consume_fastapi_json(popout = False):

        got_values = True

        #make sure we got all of these and that they are float values.
        try:
                f_medinc = request.form["medinc_text"]
                f_houseage = request.form["houseage_text"]
                f_averooms  = request.form["averooms_text"]
                f_avebedrms = request.form["avebedrms_text"]
                f_population = request.form["population_text"]
                f_aveoccup = request.form["aveoccup_text"]
                f_lat = request.form["lat_text"]
                f_long = request.form["long_text"]
        except Exception as ex:
                got_values = False
                print("*"*30)                              
                print(str(ex))
                print("*"*30)

        print("got_values={}".format(got_values))
        api_json = None
        return_json = None
        status_code = None
        url = None
        if got_values is True:
               hr = create_home_request(form=request.form)
               api_json =json.dumps(hr,indent=1)
               api_json_to_post=json.dumps(hr)
               print(api_json)
               url,status_code,return_json=execute_fastapi_call(hr)


        form = home_predict_model_inputs(request.form)

        res = jsonify({'htmlresponse':render_template('modal/fastapi_consumer.modal.html',
                form=form,
                api_json=api_json,
                return_json=return_json,
                return_status_code=status_code,
                post_url=url
                )})

        return res
