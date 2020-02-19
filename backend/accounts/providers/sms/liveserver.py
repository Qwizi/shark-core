from accounts.providers.sms.provider import AbstractSMSProvider


class LiveServerSMSProvider(AbstractSMSProvider):
    _tag = 'liveserver'
    _api_client = '645'
    _api_pin = "9086deed059933eba7586b279fde63c2"
    _api_endpoint = "https://rec.liveserver.pl/api?channel=sms&return_method=seperator"

    def __init__(self, model, code):
        super().__init__(model, code)

    def validate(self):
        data = {
            'client_id': self._api_client,
            'pin': self._api_pin,
            'code': self._code
        }
        response = self.requests.post(self._api_endpoint, data=data)

        if response.status_code != 200:
            self._validated = False
            return False

        response_text = response.text

        results = response_text.split(' ')

        if results[0] == "INVALID":
            self._validated = False
            return False

        self._sms_number = results[4]

        try:
            self._instance = self._model.get(provider=self._tag, number=self._sms_number)
            self._validated = True
        except self._model.DoesNotExist:
            self._validated = False
            return False
        return True
