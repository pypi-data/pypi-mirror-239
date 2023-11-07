import logging
from os import environ
from json import loads
from base64 import b64encode
from http.client import HTTPSConnection

FIVETRAN_DOMAIN = "api.fivetran.com"
FIVETRAN_KEY = environ.get("FIVETRAN_API_KEY")
FIVETRAN_SECRET = environ.get("FIVETRAN_API_SECRET")


def group2db(group):
    return {
        # SF_AMPLITUDE_DB
        # SF_APPLICATION_DB
        # SF_ZENDESK_DB
        # SF_MARKETING_DB
        # SF_RECRUITING_DB
        # SF_BANK_APPLICATION_DB
        # FINANCE
        # OVERDRAFT
        'FINANCE_SNOW': 'FINANCE'
    }.get(group.name.upper(),
          group.name.replace("SF_", ""))


class Docs:
    """
    {'id': 'facebook_ad_account' 'name': 'Facebook Ad Account'
     'type': 'Marketing', 'description': 'Facebook Ad Account provides attribute data on Facebook Ad Accounts'
      'icon_url': 'https://fivetran.com/integrations/facebook/resources/facebook.svg'
      'link_to_docs': 'https://fivetran.com/docs/applications/facebook-ad-account'
      'link_to_erd': 'https://fivetran.com/docs/applications/facebook-ad-account#schemainformation'}
    """
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.type = kwargs.get("type")
        self.description = kwargs.get("description")
        self.icon_url = kwargs.get("icon_url")
        self.link_to_docs = kwargs.get("link_to_docs")
        self.link_to_erd = kwargs.get("link_to_erd")

    def __str__(self):
        out = [str(self.description)]
        if self.link_to_docs:
            out.append(f"[docs]({self.link_to_docs})")
        if self.link_to_erd:
            out.append(f"[erd]({self.link_to_docs})")
        return " ".join(out)


class Group:
    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")

    def __repr__(self):
        return f"<Group {self.name} {self.id}>"


class Connector:
    def __init__(self, docs=None, **kwargs):
        self.group = kwargs.get('group')
        self.id = kwargs.get('id')
        self.schema = kwargs.get("schema")
        self.failed_at = kwargs.get("failed_at")
        self.succeeded_at = kwargs.get("succeeded_at")
        self.service = kwargs.get("service")
        self.frequency = kwargs.get('sync_frequency')
        status = kwargs.get('status')
        status = ", ".join((
            status['setup_state'],
            status['sync_state'],
            status['update_state']
        ))
        self.status = status
        self.history = kwargs.get('historical_sync_timeframe')
        if docs is not None:
            self.docs = docs.get(self.service)

    @property
    def table(self):
        if self.group is None:
            return
        return ".".join((
            group2db(self.group),
            self.schema
        )).upper()

    def __repr__(self):
        attrs = (
            self.group,
            self.id,
            self.schema,
            self.failed_at,
            self.succeeded_at,
            self.service,
            self.frequency,
            self.docs
        )
        return f"<Connector {' '.join(map(str, attrs))}>"


class FivetranClient:
    def __init__(self, fetch_docs=True):
        self.client = HTTPSConnection(FIVETRAN_DOMAIN)
        self.docs = None
        if fetch_docs:
            self.metadata()

    @property
    def headers(self):
        return {
            "Content-Type": "application/json",
            "Authorization": "Basic {}".format(b64encode(
                bytes(f"{FIVETRAN_KEY}:{FIVETRAN_SECRET}", "utf-8")).decode("ascii"))
        }

    def request(self, endpt):
        logging.info(f"GET {endpt}")
        self.client.request('GET', endpt, headers=self.headers)
        resp = self.client.getresponse()
        if resp.status == 200:
            return loads(resp.read())['data']['items']
        else:
            raise Exception(f"{resp.status}: {resp.read()}")

    def groups(self):
        data = self.request('/v1/groups')
        return [Group(**d) for d in data]

    def connectors(self, group):
        data = self.request(f'/v1/groups/{group.id}/connectors')
        return [Connector(self.docs, group=group, **d) for d in data]

    def metadata(self):
        logging.info("Fetching Docs Metadata")
        data = self.request('/v1/metadata/connectors')
        self.docs = dict([(d['id'], Docs(**d)) for d in data])
        return self.docs
