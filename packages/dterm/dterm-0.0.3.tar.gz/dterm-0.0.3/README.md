# descript

Data Engineering Scripts for data info

## Mode.com Client

[Mode Client Docs](docs/MODE.md)

## fivetran

Fetch Fivetran connectors with status (output markdown.)

```
python3 -m descript.clients.fivetran
```

Lots of ERDs and Docs in there -- one could imagine rendering out some DBT Source YAMLS!

## `descript` module

```
> python3 -m descript -h
usage: __main__.py [-h] [--render RENDER] [--parse PARSE] in_file

parse data schemas

positional arguments:
  in_file

optional arguments:
  -h, --help       show this help message and exit
  --render RENDER  output format to render
  --parse PARSE
```

Formats:

```python
descript
 |- schema
    |
    |- avro
    |- dbt - Source YAMLs
    |- ddl - MySQL CREATEs. semi-colon delimited (delete extra stuff, parser stinks)
    |- erd - PlantUML
    |- md  - markdown
```

## Not sure if this still works
```python
from descript.schema import ddl
from descript.schema import avro
db = ddl.parse(open('some.ddl').read())
for table in db:
    print(avro.render(table))

```