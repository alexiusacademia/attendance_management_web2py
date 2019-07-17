# -*- coding: utf-8 -*-
import os
from entries import *


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
    return dict(sections=sections)

def view_section_log_data():
    section_id = request.args[0]

    section = db(db.sections.id == section_id).select()

    employees_in_section = db(db.employees.section_id == section_id).select()

    return dict(section=section, employees=employees_in_section)

def view_employee_log_data():
    employee_id = request.args[0]
    employee = db(db.employees.id == employee_id).select()
    return locals()
