from descript.schema.models import Table


def get_avro_type(t):
    """
    Map type to avro type

    null: no value
    boolean: a binary value
    int: 32-bit signed integer
    long: 64-bit signed integer
    float: single precision (32-bit) IEEE 754 floating-point number
    double: double precision (64-bit) IEEE 754 floating-point number
    bytes: sequence of 8-bit unsigned bytes
    string: unicode character sequence
    """
    return t


def parse(*args):
    raise NotImplementedError("Implement me!")


def render(table: Table, namespace="com.dave.avro.schemas"):
    return {"type": "record",
            "name": table.table,
            "namespace": namespace,
            "fields": [{
                "name": column.name,
                "type": get_avro_type(column.type)
            } for column in table.columns]}
