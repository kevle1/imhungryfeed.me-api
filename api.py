from flask import Flask, request, jsonify
from google.maps import nearby_search, additional_filters
from models.PlaceRequest import PlaceRequest

import logging

app = Flask(__name__, static_url_path='')
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

@app.route('/api/places', methods=['POST'])
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

    return jsonify(places)
