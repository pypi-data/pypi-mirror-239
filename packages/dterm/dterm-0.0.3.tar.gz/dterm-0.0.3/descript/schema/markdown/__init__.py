from descript.schema.models import DataSource


def render(db: DataSource):
    print(f"## {db.name}")
    print()
    print(db.description)

    for table in db.tables:
        print(f"### {table.name}")
        print(table.description)
        print()

        for column in table.columns:
            print(f"**{column.name}**: {column.description}")
