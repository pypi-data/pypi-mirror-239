# https://mode.com/developer/api-reference/analytics/queries/
import logging
from dateutil import parser as date
from os import environ
from http.client import HTTPSConnection
import base64
from json import loads
from .models import *

HOST = 'app.mode.com'
TOKEN = environ.get("MODE_TOKEN")
SECRET = environ.get("MODE_PASSWORD")


class ModeClient:
    def __init__(self, **creds):
        self.token = creds.get('token', TOKEN)
        self.secret = creds.get('secret', SECRET)
        self.account = creds.get('account')
        self.conn = HTTPSConnection(HOST)

    @property
    def auth(self):
        return f"{self.token}:{self.secret}"

    @property
    def headers(self):
        return {
            "Authorization": "Basic {}".format(
                base64.b64encode(bytes(f"{self.token}:{self.secret}", "utf-8")).decode(
                "ascii")),
            'Content-Type': 'application/json',
            'Accept': 'application/hal+json'
        }

    def collections(self, obj):
        if obj is None:
            obj = self.account
        url = f"/api/{obj}/spaces"
        resp = self.request(url)
        if resp:
            return list(map(lambda args: Collection(**args), resp['_embedded']['spaces']))

    def queries(self, report):
        url = f"/api/{self.account}/reports/{report}/queries"
        resp = self.request(url)
        if resp:
            return list(map(lambda args: Query(**args), resp['_embedded']['queries']))

        return url

    def query(self, report, query):
        return f"/api/{self.account}/reports/{report}/queries/{query}"

    def schedules(self, report):
        query = f"/api/{self.account}/reports/{report}/schedules"
        result = self.request(query)
        return [Schedule(**args)
                for args in result['_embedded']['report_schedules']]

    def deschedule(self, schedule: Schedule):
        result = self.request(schedule.destroy, method='delete')
        return result

    def request(self, query, *params, method="GET"):
        self.conn.request(method, query, headers=self.headers)
        resp = self.conn.getresponse()
        if resp.status == 200:
            return loads(resp.read().decode('utf-8'))
        else:
            raise Exception(f"{resp.status}: {resp.read()}")
