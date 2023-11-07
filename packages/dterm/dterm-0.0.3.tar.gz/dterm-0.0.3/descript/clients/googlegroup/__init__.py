import csv

GROUP_FILE = 'data/google-groups'

class GoogleGroupTSV:
    def __init__(self):
        self.entries = {}

        with open(GROUP_FILE, 'r') as fp:
            reader = csv.reader(fp, delimiter='\t')
            for line in reader:
                group, name, email = line
                self.entries[name.lower().strip()] = group

    def group_lookup(self, name):
        return self.entries.get(name.lower().strip())
