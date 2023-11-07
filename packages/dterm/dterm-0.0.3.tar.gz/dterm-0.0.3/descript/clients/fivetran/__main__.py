from . import *
from yaml import safe_dump
from descript.schema.dbt import SourceYAML, SourceTable

logging.basicConfig(level=logging.WARN)

client = FivetranClient()
groups = client.groups()

fmt = 'csv'
sources = []

for group in groups:
    source = SourceYAML(group.name)
    sources.append(source)
    connectors = client.connectors(group)
    for connector in connectors:
        table = SourceTable(connector=connector)
        source.add(table)

if fmt == 'dbt':
    print("\n---\n".join(map(str, sources)))
else:
    for source in sources:
        print(safe_dump(source.as_dict))
