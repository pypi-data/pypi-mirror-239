"""
Table Name clean up script.

This script will look for Fully Qualified (Snowflake Table Names to replace with
`source(x, y)` tags.  This can be extended to find `ref` replacements as well.

Present strategy is to:
- continue execution on error (configurable with `ignore_errors` arg)
- be conservative with confident code replacements.

This module is a script in addition to a library.
"""
from glob import glob
import re

from dterm.models import SQLModelLoader


def sqlmodel(models, filename):
    """
    model by filename
    """
    loader = SQLModelLoader(models)
    model = list(filter(lambda m: m.filename == filename, loader.models()))
    if model:
        return model[0]
    else:
        raise Exception(f"Model {filename} not found")


def sqlmodels(models):
    """
    modelS by filename
    """
    loader = SQLModelLoader(models)

    for sqlmodel in loader.models():
        yield sqlmodel


def sources(source_dir):
    for file in glob(source_dir + "/**/*.yml", recursive=True):
        yield file
    for file in glob(source_dir + "/**/*.yaml", recursive=True):
        yield file


def replace(sqlfilename, tables, lookup):
    """
    open sqlfilename, and replace all table strings, if they exist in lookup
    """

    with open(sqlfilename) as sqlfile:
        sql = sqlfile.read()
        for regex, dbt_location in lookup.items():
            dbt_location = '{{' + f"source('{dbt_location[0]}', '{dbt_location[1]}')" + '}}'
            sql = re.sub(regex, dbt_location, sql)

    return sql