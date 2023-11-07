import yaml


def print_table(table):
    # primary_key ( id ): INT
    # column ( firstname ): VARCHAR(100
    # column ( lastname ): VARCHAR(100)
    name = table.name
    columns = table.columns

    columns_r = "\n".join([f"      {col.name}" for col in columns])
    return """entity {name}  {{
{columns}
    }}
    """.format(name=name, columns=columns_r)


def render(source):
    out = """
    @startuml
    hide circle
    skinparam roundcorner 5
    skinparam linetype ortho
    skinparam shadowing false
    skinparam handwritten false
    skinparam class {
      BackgroundColor white
      ArrowColor #2688d4
      BorderColor #2688d4
    }\n
    """
    for table in source.tables:
        out += f"{print_table(table)}\n"

    out += "@enduml\n"
    return out


