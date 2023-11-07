from descript.clients.charthop import EmployeeExport
from descript.clients.googlegroup import GoogleGroupTSV

CHARTHOP_CHART = 'data/charthop-dave.csv'

groups = GoogleGroupTSV()
def charthop(name_parital):
    employee_chart = EmployeeExport(CHARTHOP_CHART)
    employee_chart.pecking_order()

    emps = []
    for fullname, employee in employee_chart.fullname_lookup.items():
        if name_parital.lower() in fullname.lower():
            employee.group = groups.group_lookup(employee.fullname)
            emps.append(employee)

    return emps
