import json
from flask import Flask, request, jsonify, Response
from flask_cors import CORS, cross_origin
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from google.maps import nearby_search, additional_filters
from ip.ip import ip_location

from models.PlaceRequest import PlaceRequest

import logging

app = Flask(__name__, static_url_path='')
limiter = Limiter(app, key_func=get_remote_address)
CORS(app)

logging.basicConfig(filename='./logs/api.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler())

BAD_REQUEST = 400

@app.route('/')
def index():
    return "<h2>I'm Hungry, Feed Me API</h2><br><br\> \
            <a href='https://imhungryfeed.me'>Website</a>"

@limiter.limit("60/minute")
@app.route('/places', methods=['POST'])
def feed_me():
    logging.debug(f"Inbound request: {request.json}")
    place = PlaceRequest(**request.json)

    bad_request_msg = None
    if not 1 <= place.min_price <= 4 or not 1 <= place.max_price <= 4:
        bad_request_msg = "Error: Invalid price specified, must be between 1 and 4"
    elif place.max_price < place.min_price:
        bad_request_msg = "Error: Invalid price range"
    elif place.radius < 100 or place.radius > 24000:
        bad_request_msg = "Error: Max range limit of 24KM"
    elif not 0.0 <= place.rating <= 5.0:
        bad_request_msg = "Error: Invalid rating"

    if bad_request_msg:
        logging.error(bad_request_msg)
        return bad_request_msg, BAD_REQUEST

    # NOTE: Cache will be missed if these params are updated (likely often)
    #       Consider just filtering on returned properties rather
    #       than hitting Google. May cause reduced result set.
    places = nearby_search(place.latitude,
                           place.longitude,
                           place.radius,
                           place.keyword,
                           place.min_price,
                           place.max_price,
                           place.open_now)

    places = additional_filters(places, place.rating)

    response = Response(json.dumps(places))
    response.headers['Cache-Control'] = 's-maxage=60' # Cache for 60 seconds
    response.headers['Content-Type'] = 'application/json' 

    return response

@limiter.limit("80/minute")
@app.route('/ip', methods=['GET'])
def get_ip():
    #logging.debug(f"Inbound request: {request.remote_addr}")
    ip = request.headers.get('X-Real-Ip')

    logging.debug(f"Inbound headers: {ip}")  # nginx config will have headers set
    ip_info = ip_location(ip)

    if ip_info:
        logging.debug(f"Outbound IP request: {ip_info}")
        return jsonify(ip_info), 200
    else:
        return "Error: No location response from ip-api.com", 400
