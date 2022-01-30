# Decimal places to preserve on Lon/ Lat
# 2dp ± 500m accuracy
# 3dp ± 100m accuracy
LOCATION_ACCURACY = 3
RADIUS_ACCURACY = 5

class PlaceRequest(object):
    def __init__(self, latitude, longitude, radius, keyword=None, min_price=1, max_price=4, open_now=True, rating=0.0):
        self.latitude = round(latitude, LOCATION_ACCURACY)
        self.longitude = round(longitude, LOCATION_ACCURACY)
        self.radius = 5 * round(radius / 5) # Round to nearest 5 metres
        self.keyword = keyword
        self.min_price = min_price  # $-$$$$ 1-4 dollar signs
        self.max_price = max_price
        self.open_now = open_now
        self.rating = rating
