# -*- coding: utf-8 -*-
import os
import datetime
from common.logs.entries import *


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
    log_id = request.args[0]
    log = db(db.logs.id == log_id).select()
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

    session.start_date = start_date
    session.end_date = end_date

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

    return dict(sections=sections, start_date=start_date, end_date=end_date)


def set_session_start_date():
    # Set the start_date and save to session
    start_date = request.args[0]

    session.start_date = start_date

    return start_date


def set_session_end_date():
    # Set the end_date and save to session
    end_date = request.args[0]

    session.end_date = end_date

    return end_date


def view_section_log_data():
    section_id = request.args[0]
    section = db(db.sections.id == section_id).select()

    employees_in_section = db(db.employees.section_id == section_id).select()

    return dict(section=section, employees=employees_in_section)


def view_employee_log_data():
    employee_id = request.args[0]
    employee = db(db.employees.employee_id == int(employee_id)).select()

    start_date = datetime.datetime.strptime(str(session.start_date), '%Y-%m-%d')
    end_date = datetime.datetime.strptime(str(session.end_date), '%Y-%m-%d')

    # _employee_log = get_all_time_entries(start_date, end_date, session.log_lines, int(employee_id))
    _time_logs = get_all_time_entries(start_date, end_date, session.log_lines, int(employee_id))
    _logs = get_all_entries(start_date, end_date, session.log_lines, int(employee_id))

    # Get list of date from the range
    _dates = get_dates(start_date, end_date)

    return dict(_dates=_dates, time_logs=_time_logs, logs=_logs, name=employee[0]['name'])
