from phenom.credentials.get_token import tokengeneration
from phenom.prediction.api.prediction_api import PredictionApi
from phenom.resumeparser.api.resume_parsing_api import ResumeParsingApi


class Authorization(object):
    def __init__(self, url, client_id, client_secret, gateway_url, apikey=None):
        self.url = url
        self.client_id = client_id
        self.client_secret = client_secret
        self.gateway_url = gateway_url
        self.apikey = apikey

    def token(self):
        return tokengeneration(self.url, self.client_id, self.client_secret)

    def prediction_api(self):
        Predictionapi = PredictionApi(self.token(), self.gateway_url, self.apikey)
        return Predictionapi

    def resumeparser_api(self):
        Resumeparserapi = ResumeParsingApi(self.token(), self.gateway_url, self.apikey)
        return Resumeparserapi
