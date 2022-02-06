import os
import time
import yaml
import logging

from diskcache import Cache

import googlemaps
from googlemaps.exceptions import ApiError

RESTAURANT_TYPE = 'restaurant'
RESULTS_COUNT_MAX = 80 # Retrieve 80 restaurants from Google Maps API - Max wait of 4 seconds

cache = Cache("cache")

with open(os.path.join(os.path.dirname(__file__), 'keys.yaml'), 'r') as c:
    cfg = yaml.safe_load(c)
gmaps = googlemaps.Client(key=cfg['gmaps'])

@cache.memoize()
def nearby_search(latitude, longitude, radius, keyword, min_price, max_price, open_now):
    page_token = None
    results = []

    while len(results) < RESULTS_COUNT_MAX:
        try:
            nearby = gmaps.places_nearby(location=f'{latitude},{longitude}',
                                         radius=radius,
                                         keyword=keyword,
                                         min_price=min_price,
                                         max_price=max_price,
                                         open_now=open_now,
                                         type=RESTAURANT_TYPE,
                                         page_token=page_token)

            status = nearby['status']
            logging.info(f'Maps API call returned status {status}')

            if status == 'INVALID_REQUEST':
                logging.error('Error: Invalid request returned from Maps API')
                return None
            elif status == 'ZERO_RESULTS':
                logging.info('No results returned from Maps API')
                break
            elif status != 'OK':
                logging.info(f'Unknown Error with status {status}')
                break
            elif status == 'OK':
                if 'results' in nearby:
                    results.extend(nearby['results'])

            if 'next_page_token' in nearby:
                page_token = nearby['next_page_token']
            else:
                logging.info('Maps API returned no next page token - End of results')
                break

            # https://developers.google.com/maps/documentation/places/web-service/search-nearby#PlacesNearbySearchResponse
            # There is a short delay between when a next_page_token is
            # issued, and when it will become valid. Therefore sleep for 2 secs.
            time.sleep(2)
        except KeyError as e:
            logging.error(f'Error: Could not find key - {e}')
        except ApiError as ae:
            logging.error(f'Error: Could not make request to Maps API - {ae}')
            break
        except Exception as e:
            logging.error(f'Error: Fatal error - {e}')
            break

    return build_response(results)

def build_response(place_results):
    response = []

    for place in place_results:
        try:
            if place['business_status'] == "OPERATIONAL":
                response.append({
                    'name': place['name'],
                    'url': f"https://www.google.com/maps/place/?q=place_id:{place['place_id']}",
                    'location': place['geometry']['location'],
                    'address': place['vicinity'],
                    'price_level': place['price_level'],
                    'rating': place['rating'],
                    'rating_count': place['user_ratings_total']
                })
        except KeyError as e:
            logging.error(f'Error: Place {place} does not contain expected keys')

    return response

def additional_filters(response, rating):
    return [r for r in response if r['rating'] >= rating]