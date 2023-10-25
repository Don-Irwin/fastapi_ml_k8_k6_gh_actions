from lab3 import __version__


def test_version():
    assert __version__ == '0.1.0'

from fastapi.testclient import TestClient
import sys
import json

from lab3.main import app
client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Implemented"}

def test_read_hello():
    response = client.get("/hello?name=Don")
    assert response.status_code == 200
    assert response.json() == "hello Don"

def test_read_hello_no_param():
    response = client.get("/hello")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['query', 'name'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_read_hello_wrong_param():
    response = client.get("/hello?bozo=fido")
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['query', 'name'], 'msg': 'field required', 'type': 'value_error.missing'}]}

def test_read_docs():
    response = client.get("/docs?fido=dido")
    assert response.status_code == 200
    
def test_check_health_health():
    response = client.get("/health")
    assert response.status_code == 200

#happy path
def test_predict_function():
    post_payload = [{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 }]
    response = client.post("/predict", data =json.dumps(post_payload))
    assert response.status_code == 200
    for value in response.json()["prediction_results"]:
        assert type(value["prediction_result"]) is float

#fail1
def test_predict_function_malformed_list():
    post_payload = {"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.984126984126984,"AveBedrms":1.0238095238095237,"Population":322.0,"AveOccup":2.5555555555555554,"Latitude":37.88,"Longitude":-122.23, "fido" : "dido" }
    response = client.post("/predict", data =json.dumps(post_payload))
    assert response.status_code == 422
    assert response.json()["detail"] == [
        {
            "loc": ["body"],
            "msg": "value is not a valid list",
            "type": "type_error.list"
        }
    ]    


#fail2
def test_predict_function_extra_param_list():
    post_payload = [{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":8.3252,"HouseAge":41.0,"AveRooms":6.984126984126984,"AveBedrms":1.0238095238095237,"Population":322.0,"AveOccup":2.5555555555555554,"Latitude":37.88,"Longitude":-122.23, "fido" : "dido" }]
    response = client.post("/predict", data =json.dumps(post_payload))
    assert response.status_code == 422
    assert response.json()["detail"] == [
    {
      "loc": [
        "body",
        1,
        "fido"
      ],
      "msg": "extra fields not permitted",
      "type": "value_error.extra"
    }
  ]

#wrong type
def test_predict_function_wrong_type_in_list():
    post_payload = [{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude":-122.25 },{"MedInc":5.6431,"HouseAge":52.0,"AveRooms":5.8173515981735155,"AveBedrms":1.0730593607305936,"Population":558.0,"AveOccup":2.547945205479452,"Latitude":37.85,"Longitude": "West" }]
    response = client.post("/predict", data =json.dumps(post_payload))
    assert response.status_code == 422
    assert response.json()["detail"] ==  [
        {
        "loc": [
            "body",
            1,
            "Longitude"
        ],
        "msg": "value is not a valid float",
        "type": "type_error.float"
        }
    ]
    


#cache ration tests
def test_getcacheratio_function():
    test_predict_function()
    test_predict_function()
    test_predict_function()
    response = client.get("/getcacheratio")
    assert response.status_code == 200




def main():
    test_read_main()
