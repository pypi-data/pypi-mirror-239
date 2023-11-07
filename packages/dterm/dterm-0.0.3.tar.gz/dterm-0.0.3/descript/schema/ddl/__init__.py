from ddlparse import DdlParse
import pyparsing

from descript.schema.models import Table, DataSource


def parse(ddl, raises=True):
    """
    Parse DDL, return descript.schema objects
    """
    parser = DdlParse()
    db = DataSource()
    for statement in ddl.split(';'):
        try:
            result = parser.parse(statement)
            db.tables.append(
                Table.from_ddlparse(result)
            )
        except pyparsing.ParseException as ex:
            if raises:
                raise ex

    return db


def render(db):
    raise NotImplementedError("DDL Rendering is not implemented.")