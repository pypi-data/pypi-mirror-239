# sourcerer

Replacing hard-coded SQL table names to `source` and `ref` tags (more refsourceful.)

To Run:

```
python3 -m dbtterm.sourcerer ~/projects/dave-dbt/dave-sql/models/
```

Seeing ~103 replacements in `dave-dbt` with present configuration.

## Library

```
Help on package dbtterm.sourcerer in dbtterm:

NAME
    dbtterm.sourcerer - Table Name clean up script.

DESCRIPTION
    This script will look for Fully Qualified (Snowflake Table Names to replace with
    `source(x, y)` tags.  This can be extended to find `ref` replacements as well.

    Present strategy is to:
    - continue execution on error (configurable with `ignore_errors` arg)
    - be conservative with confident code replacements.

    This module is a script in addition to a library.

PACKAGE CONTENTS
    __main__
    models (package)

FUNCTIONS
    replace(sqlfilename, tables, lookup)
        open sqlfilename, and replace all table strings, if they exist in lookup

    sources(source_dir)

    sqlmodel(models, filename)
        model by filename

    sqlmodels(models)

FILE
    dbtterm/sourcerer/__init__.py
```

## CLI

```
python3 -m dbtterm.sourcerer -h
usage: sourcerer [-h] [--sources SOURCES] [--model MODEL] [--dryrun DRYRUN] models

forcing dbt sources on SQL

positional arguments:
  models             path to models dir

options:
  -h, --help         show this help message and exit
  --sources SOURCES  Path to Sources dir
  --model MODEL      only run one SQL file
  --dryrun DRYRUN    SQL destination dir
```

