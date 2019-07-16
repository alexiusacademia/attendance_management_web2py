# -*- coding: utf-8 -*-
import os


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

    '''
    sections = []
    for employee_id in employee_ids:
        section = db(db.employees.employee_id == int(employee_id)).select()[0]['section_id']
        if section not in sections:
            sections.append(section)'''

    return dict(sections=sections)
