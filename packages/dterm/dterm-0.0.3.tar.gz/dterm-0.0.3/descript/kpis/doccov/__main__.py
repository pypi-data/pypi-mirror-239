
TABLES = 'data/tables.tsv'
DOCS = 'data/docs.tsv'


undocumented = set()

docfp = open(DOCS)
docs = set(map(lambda l: l.upper().strip(), docfp.read().split("\n")))
docfp.close()

table_count = 0.0
with open(TABLES) as tbls:
    for table in tbls:
        table_count += 1
        table = table.upper()
        if table.strip() not in docs:
            undocumented.add(table)

print(table_count)
print(len(undocumented))
print(float(len(undocumented))/table_count)
