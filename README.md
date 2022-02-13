# I'm Hungry, Feed Me - API 🍜

An API for the [random restaurant picker app](https://github.com/kevinle-1/imhungryfeed.me).

Built using Flask and the Google Maps Platform.

## Woah, how do I use it? 🍔

### Endpoints

Essentially a wrapper around the [Nearby Search](https://developers.google.com/maps/documentation/places/web-service/search-nearby#required-parameters) endpoint.

POST `/api/places`

#### Request Body

Required fields:
- **latitude** - Double
- **longitude** - Double
- **radius** - Integer (Metres)

Optional fields:
- **keyword** - String (Any additional word to filter by, e.g. "Ramen")
- **min_price** - Integer (0-4 - The $, $$, $$$, $$$$ dollar signs representing the restaurant cost)
- **max_price** - Integer (0-4)
- **open_now** - Boolean (If the restaurant is open)
- **rating** - Double (0.0 - 5.0 - The minimum rating of the restaurant)

Example Request:
```
{
    "latitude": -31.9522,
    "longitude": 115.861096,
    "radius": 1500
}
```

Example very cool Response:

```
[
    {
        "address": "191/580 Hay Street, Perth",
        "location": {
            "lat": -31.9546478,
            "lng": 115.8609719
        },
        "name": "NAO Japanese Ramen",
        "price_level": 1,
        "rating": 4.4,
        "rating_count": 1260,
        "url": "https://www.google.com/maps/place/?q=place_id:ChIJcTgvzte6MioRo5NK6hCpbnw"
    },
    ...
]
```

GET `/ip`

Get IP geolocation information

Note, you will require the following config if using Nginx (recommended)

```
    location / {
        proxy_pass  http://web;
        proxy_set_header   Connection "";
        proxy_http_version 1.1;
        proxy_set_header        Host            $host;
        proxy_set_header        X-Real-IP       $remote_addr;
        proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
    }
```

## Running it yourself! 🍕

First, get an [API key for the Google Maps Platform](https://console.cloud.google.com/google/maps-apis/start)

We're only using the "Places API"

Update the `keys.sample.yaml` with your API key and save it as `keys.yaml` in the same directory

### Docker (Recommended)

You'll need Docker

1. Build image `docker build -t feedme/api .`
2. Run it! `docker run -p 5000:5000/tcp feedme/api -d`

Note: Ensure `run.sh` is executable before building the image! `chmod +x run.sh`

### Command Line

You'll need Python3.8+

1. Install requirements `pip install -r requirements.txt`
2. Run it! `python wsgi`

### Gunicorn

You'll need... Gunicorn - [installation instructions](https://docs.gunicorn.org/en/stable/install.html)

Then just run `gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app` or `./run.sh`


