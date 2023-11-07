from argparse import ArgumentParser
from . import ModeClient

ACCOUNT = 'dave_saves'

parser = ArgumentParser(description="Mode.com Client")
parser.add_argument('--action', default="schedules",
                    help="mode endpoint to hit")
parser.add_argument('--q', required=False, default=None,
                    help="provide report url, get queries in data dir")
parser.add_argument('--reports', required=False, default=None,
                    help="list all reports")
parser.add_argument('--report_file', required=False, default=None,
                    help="File with Mode Report 'URL\tname'")
args = parser.parse_args()

client = ModeClient(account=ACCOUNT)

reports = {}
report_ids = set()


def get_report_id(url):
    return url.split('/')[5]


if args.reports:
    reports = client.collections(args.reports) # dave_saves
    for r in reports:
        print(r)
if args.q:
    rid = get_report_id(args.q)
    queries = client.queries(rid)
    print(", ".join(map(str, queries)))

    for q in queries:
        filename = 'data/' + q.name.lower().replace(' ', '_') + '.sql'
        with open(filename, 'w') as fp:
            fp.write(q.sql)

    exit(0)


if args.report_file:
    with open('data/reports.tsv') as usage:
        for line in usage:
            url, name = line.split("\t")
            report_id = None
            try:
                report_id = get_report_id(url)
                if report_id:
                    report_ids.add(report_id)
                    reports[report_id] = name
            except IndexError:
                pass
    print(f"report count: {len(report_ids)}")

# views of reports
if args.action == 'schedules':
    for report_id in report_ids:
        try:
            name = reports.get(report_id, "UNKNOWN TITLE")
            schedules = client.schedules(report_id)
            if schedules:
                print(name, report_id, "\t".join(map(str, schedules)))
        except Exception as ex:
            # print(f"ERROR: {report_id} {ex}")
            pass
