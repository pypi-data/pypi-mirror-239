from yaml import dump, safe_load
from descript.schema.models import Table, Column, DataSource


TEMPLATE = {
    "version": 2,
    "sources": [
        {
            "name": 'database name',
            "description": "TODO",
            "tables": [],
            # dbt does not approve of extra fields
            # "owner": {
            #     "name": "",
            #     "email": ""
            # },
            # "slack": "",
            # "repository": ""
        }
    ]
}


class SourceTable:
    def __init__(self, **kwargs):
        self.connector = kwargs.get("connector")
        self.description = kwargs.get("description", "")
        if self.connector:
            self.name = self.connector.table
            if self.connector.docs:
                self.description = str(self.connector.docs)

    @property
    def as_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "columns": []
        }


class SourceYAML:
    def __init__(self, db_name, db_desc="TODO"):
        self.doc = TEMPLATE
        self.source = self.doc['sources'][0]
        self.source['name'] = db_name
        self.source['description'] = db_desc

    def add(self, table):
        self.source['tables'].append(table.as_dict)

    @property
    def as_dict(self):
        return {
            "name": self.source['name'],
            "description": self.source['description'],
            "tables": self.source['tables'] # [table.as_dict for table in self.source['tables']]
        }

    def __str__(self):
        return dump(self.doc)


def parse(yaml):
    data = safe_load(yaml)

    sources = []
    for source in data['sources']:
        db = DataSource(**source)
        sources.append(db)

        for tbl in source['tables']:
            table = Table(**tbl)
            db.tables.append(table)

    return sources


def render(db: DataSource):
    out = TEMPLATE.copy()
    out['version'] = 2
    # TODO
    out['sources'][0]['name'] = db.name
    out['sources'][0]['description'] = db.description
    out['sources'][0]['tables'] = [{
        'name': table.name,
        'description': table.description,
        'columns': [{
           'name': col.name,
           'description': col.description
        } for col in table.columns]
    } for table in db.tables]

    return dump(out)


