import geocoder

def get_location():
    g = geocoder.ip('me')
    return {
        'latitude': g.latlng[0],
        'longitude': g.latlng[1]
    }
