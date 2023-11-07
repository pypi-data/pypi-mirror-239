from descript.schema import dbt, ddl, erd
import yaml


def render_md(dbs):
    for db in dbs:
        print(f"## {db.name}")
        print()
        print(db.description)

        for table in db.tables:
            print(f"### {table.name}")
            print(table.description)
            print()

            for column in table.columns:
                print(f"**{column.name}**: {column.description}")


def data_dic():
    with open("data/schemas/cashback.yml") as yml:
        data = yaml.safe_load(yml)
        for source in data['sources']:
            print(f"## {source['name']}")
            print()
            print(source.get("description"))

            for table in source['tables']:
                print(f"### {table['name']}")
                print(table.get("description"))
                print()

                for column in table['columns']:
                    print(f"**{column['name']}**: {column.get('description')}")

