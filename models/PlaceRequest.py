import math

# Decimal places to preserve on Lon/ Lat
# 2dp ± 500m accuracy
# 3dp ± 100m accuracy
LOCATION_ACCURACY = 3
RADIUS_ACCURACY = 100

class PlaceRequest(object):
    def __init__(self, latitude, longitude, radius, keyword=None, min_price=1, max_price=4, open_now=True, rating=0.0):
        self.latitude = round(latitude, LOCATION_ACCURACY)
        self.longitude = round(longitude, LOCATION_ACCURACY)
        self.radius = math.ceil(float(radius) / RADIUS_ACCURACY) * RADIUS_ACCURACY # Round to nearest 100 metres
        self.keyword = keyword
        self.min_price = min_price or 1  # $-$$$$ 1-4 dollar signs
        self.max_price = max_price or 4
        self.open_now = open_now
        self.rating = rating or 0.0
