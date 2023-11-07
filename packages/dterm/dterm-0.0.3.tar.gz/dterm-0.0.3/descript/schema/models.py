from ddlparse import DdlParseTable


class DataSource:
    """An analog for a database"""
    def __init__(self, **kwargs):
        self.name = kwargs.get('name')
        self.description = kwargs.get('description', '')
        self.tables = [Table(**kw)
                       if isinstance(kw, dict) else kw
                       for kw in kwargs.get('tables', [])]


class Table:
    """A table or collection of records"""
    def __init__(self, name=None, columns=None, description='', **kwargs):
        if columns is None:
            columns = []

        self.name = name
        self.description = description
        self.columns = columns
        self.columns = [Column(**col)
                        if isinstance(col, dict) else col
                        for col in columns]

    @classmethod
    def from_ddlparse(cls, table: DdlParseTable):
        return cls(
            name=table.name,
            columns=[Column(name=name,
                            type=col.data_type)
                     for name, col in table.columns.items()]
        )


class Column:
    """Atomic unit of data."""
    def __init__(self, name=None, type=None, description='', **kwargs):
        self.name = name
        self.description = description
        self.type = type
