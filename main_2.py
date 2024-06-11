#!/usr/bin/python3
"""Testing file
"""
import json
import requests

if __name__ == "__main__":
    """ PUT /api/v1/amenities/<amenity_id>
    """
    r = requests.put("http://0.0.0.0:5000/api/v1/amenities/{}".format("doesn_t_exist"), data=json.dumps({ 'name': "NewAmenityName" }), headers={ 'Content-Type': "application/json" })
    print(r.status_code)
