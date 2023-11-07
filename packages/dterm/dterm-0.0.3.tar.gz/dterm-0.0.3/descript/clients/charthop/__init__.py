"""
https://app.charthop.com/xxx/sheet
"""

from dataclasses import dataclass
from typing import Optional
import csv

@dataclass
class Employee:
    avatar: str
    name: str
    title: str
    manager_str: str
    department: str
    group: Optional[str] = None

    @property
    def first_name(self):
        try:
            return self.name.split(',')[1].strip()
        except IndexError:
            return ''

    @property
    def last_name(self):
        try:
            return self.name.split(',')[0].strip()
        except IndexError:
            return ''

    @property
    def fullname(self):
        return " ".join((self.first_name, self.last_name))

    @property
    def manager_fullname(self):
        return self.manager_str.split('-')[0].strip()

    @property
    def team(self):
        return self.manager_str.split(',')[1].strip()
    def __repr__(self):
        return f"{self.fullname}, {self.title} ({self.group})\n" \
               f"\t{self.team}, {self.manager_fullname}"

class EmployeeExport:
    def __init__(self, filename):
        self.filename = filename
        self.hierarchy_hash = {}
        self.fullname_lookup = {}

    def employees(self):
        with open(self.filename, 'r') as fp:
            reader = csv.reader(fp)
            for record in reader:
                employee = Employee(*record)
                yield employee

    def pecking_order(self):
        for employee in self.employees():
            self.fullname_lookup[employee.fullname] = employee
            self.hierarchy_hash[employee.fullname] = []
        for employee in self.employees():
            if employee.manager_fullname in self.hierarchy_hash:
                self.hierarchy_hash[employee.manager_fullname].append(employee)

    def subordinates(self, fullname):
        return self.hierarchy_hash[fullname]
