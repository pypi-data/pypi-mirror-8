class Timestep(object):
    def __init__(self, api_key=""):
        self.api_key = api_key

        self.name = None
        self.weather = None
        self.temperature = None
        self.feels_like_temperature = None
        self.wind_speed = None
        self.wind_direction = None
        self.wind_gust = None
        self.visibility = None
        self.uv = None
        self.precipitation = None
        self.humidity = None
