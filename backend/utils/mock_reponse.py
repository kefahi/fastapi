import json


class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json.loads(json_data)
        self.status = status_code
        self.ok = True

    def json(self):
        return self.json_data
