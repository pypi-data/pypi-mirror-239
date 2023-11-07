import re
from jinja2 import Environment, FileSystemLoader
from glob import glob
from sqlglot import parse_one, parse
import sqlglot.expressions as exp
from yaml import safe_load

from sqlglot.errors import ParseError
from jinja2.exceptions import UndefinedError
from .exposures import *

NOTATABLE = "NOTATABLE"


class MissingMethodObject:
    def star(self, *args, **kwargs):
        return '*'

    def __getattr__(self, item):
        def missing_method(*args, **kwargs):
            return ''

        return missing_method


def string(*args, **kwargs):
    return 'STRING_VALUE'


def notatable(*args, **kwargs):
    return NOTATABLE


def blank(*args, **kwargs):
    return ''

REPLACED_FUNCTIONS = {
    "source":  notatable,
    "ref":  notatable,
    "format_metric":  blank,
    "dbt_utils":  MissingMethodObject(),
    "var":  string,
    "is_incremental":  string,
    "calculate_pop_daily":  string,
    "calculate_pop_ratio_daily":  string,
    "run_started_at":  MissingMethodObject(),
    "config":  blank
}


class SQLModel:
    def __init__(self, filename, env: Environment):
        self.filename = filename
        blah = filename.replace(env.loader.searchpath[0], '')
        self.tmpl = env.get_template(blah)

    def sql(self):
        return open(self.filename).read()

    def render(self):
        """
        hacks in here to remove casting/json
        """
        out = self.tmpl.render()
        out = re.sub(r"::[a-zA-Z_]+", '', out)
        out = out.replace(":", "") # don't care about casting

        return out

    def ctes(self):
        for stmt in parse(self.render()):
            for cte in stmt.find_all(exp.CTE):
                print(cte)
                yield cte

    def tables(self, fqtn_only=True, ignore_errors=True):
        try:
            for stmt in parse(self.render()):
                for table in stmt.find_all(exp.Table):
                    if table.name == NOTATABLE:
                        continue
                    if fqtn_only and (not table.db  or not table.catalog):
                        continue
                    yield ".".join((table.db, table.catalog, table.name))
        except UndefinedError as ex:
            if not ignore_errors:
                raise ex
            print(f"Try implementing models REPLACED_FUNCTION: {ex}")
        except ParseError as ex:
            if not ignore_errors:
                print(self.filename)
                raise ex
            print(f"Parsing error: {self.filename}") #  {ex.message}")


class SQLModelLoader:
    def __init__(self, model_dir):
        self.model_dir = model_dir
        self.env = Environment(loader=FileSystemLoader(model_dir))
        self.env.globals.update(**REPLACED_FUNCTIONS)

    def models(self):
        for file in glob(self.model_dir + "/**/*.sql", recursive=True):
            yield SQLModel(file, self.env)


class DBTSource:
    def __init__(self, filename):
        self.filename = filename
        self.data = safe_load(open(filename).read())
        self.sources = self.data.get('sources', [])
        self.tables = {}

        self.load()

    def load(self):
        for source in self.sources:
            name = source.get('name')
            database = source.get('database')
            schema = source.get('schema')
            for table in source.get('tables', []):
                try:
                    # quote or no quote?
                    fqtn = r'"?' + '"?."?'.join((database, schema, table['name'])).upper() + '"?'
                    self.tables[fqtn] = (name, table['name'])
                except TypeError as ex:
                    print(f"Partial Config: {database}.{schema}.{table['name']}")

    def table_lookup(self):
        return self.tables

    def table(self, fqtn):
        location = self.tables.get(fqtn.upper())
        if location:
            return f"source('{location[0]}', '{location[1]}')"


class SourceYAMLLoader:
    def __init__(self, source_dir):
        self.source_dir = source_dir

    def sources(self, recursive=True):
        """
        returns a lame hash map of tuples
        FQTN -> (source_name, table_name)
        """
        lookup = {}
        for file in glob(self.source_dir + "/**/*.yml", recursive=recursive):
            lookup = dict(lookup, **DBTSource(file).table_lookup())
        for file in glob(self.source_dir + "/**/*.yaml", recursive=recursive):
            lookup = dict(lookup, **DBTSource(file).table_lookup())

        return lookup
