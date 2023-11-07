from glob import glob
import yaml

doced = 0
skipped = []
autogen = []
for file in glob("data/dbtcov/*.yml", recursive=True) +\
        glob("data/dbtcov/*.yaml", recursive=True):
    with open(file) as fp:
        o = yaml.safe_load(fp)
        if 'sources' not in o:
            skipped.append(file)
            continue

        # print(o)
        sources = o['sources']
        for source in sources:
            try:
                source_name = source['name']
                db = source['database']
                schema = source['schema']

                for table in source['tables']:
                    table_name = table['name']
                    desc = table['description']
                    fqtn = ".".join((db, schema, table_name))
                    if "Auto-Generated" in desc:
                        autogen.append(fqtn)
                        continue

                    doced += 1
                    print(fqtn)

            except KeyError:
                pass
                # print(f"ERROR: {source}")


print(doced)