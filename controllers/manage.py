# -*- coding: utf-8 -*-
import os
import datetime


def index():
    return dict(message="hello from manage.py")

def attlogs():
    db.logs.uploaded.default = request.now
    logs = SQLFORM.grid(db.logs)
    # form = SQLFORM(db.logs).process()
    return locals()

def generate_entry():
    logs = db(db.logs).select(orderby=~db.logs.id)
    return dict(logs=logs)

def use_log_data():
    id = request.args[0]
    log = db(db.logs.id == id).select()
    filepath = os.path.join(request.folder, 'uploads', log[0].log_file)
    f = open(filepath, 'r')
    lines = f.readlines()

    # Get the oldest and latest dates
    # to be displayed as default in the start and end date inputs
    start_date = datetime.date.today()
    end_date = datetime.date(2013, 9, 16)

    for line in lines:
        elems = line.split()
        _date = elems[1]
        _date = datetime.datetime.strptime(_date, "%Y-%m-%d").date()

        if _date < start_date:
            start_date = _date
        if _date > end_date:
            end_date = _date

    session.log_lines = lines
    employees = db(db.employees).select()

    sections = []
    previous_ids = []
    for l in lines:
        l = l.split()
        if l[0] in previous_ids:
            pass
        else:
            # Remember this id so that it doesn't get to parse again
            # next loop.
            previous_ids.append(l[0])

            for employee in employees:
                if employee['employee_id'] == int(l[0]):
                    if employee['section_id'] not in sections:
                        sections.append(employee['section_id'])

    session.num_lines = str(len(lines))
    return dict(sections=sections, start_date=start_date, end_date=end_date)

def view_section_log_data():
    section_id = request.args[0]

    section = db(db.sections.id == section_id).select()

    employees_in_section = db(db.employees.section_id == section_id).select()

    return dict(section=section, employees=employees_in_section)

def view_employee_log_data():
    employee_id = request.args[0]
    employee = db(db.employees.employee_id == int(employee_id)).select()

    lines = session.log_lines

    form = FORM(INPUT(_name='start_date', _type='date'))

    start_date = datetime.datetime(2019, 2, 1)
    end_date = datetime.datetime(2019, 2, 15)

    _employee_log = []
    for line in lines:
        elems = line.split()
        if int(elems[0]) == int(employee_id):
            _employee_log.append(line)

    # _logs = get_all_entries(start_date, end_date, lines, employee_id)
    return dict(log=_employee_log, name=employee[0]['name'], form=form)
