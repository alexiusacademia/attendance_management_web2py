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

    _am_time_ins = []
    _am_time_outs = []
    _pm_time_ins = []
    _pm_time_outs = []
    _lates = []
    _undertimes = []
    _messages = []

    for _date in _dates:
        _day_log_entries = get_log_entries_for_a_day(_date, _logs)
        _day_time_entries = get_time_entries_for_a_day(_date, _time_logs)
        in1 = get_time_in(_day_time_entries, _day_log_entries, am=True)

        _late = 0
        _undertime = 0

        if in1['time_in'] is not None:
            _am_time_ins.append(in1['time_in'])
            _late += in1['late']
        else:
            _am_time_ins.append('')

        out1 = get_time_out(_day_time_entries, _day_log_entries, am=True)
        if out1['time_out'] is not None:
            _am_time_outs.append(out1['time_out'])
            _undertime += out1['under_time']
        else:
            _am_time_outs.append('')

        in2 = get_time_in(_day_time_entries, _day_log_entries, am=False)
        if in2['time_in'] is not None:
            _pm_time_ins.append(in2['time_in'])
            _late += in2['late']
        else:
            _pm_time_ins.append('')

        out2 = get_time_out(_day_time_entries, _day_log_entries, am=False)
        if out2['time_out'] is not None:
            _pm_time_outs.append(out2['time_out'])
            _undertime += out2['under_time']
        else:
            _pm_time_outs.append('')

        if _late == 0:
            _lates.append('')
        else:
            _lates.append(_late)
        if _undertime == 0:
            _undertimes.append('')
        else:
            _undertimes.append(_undertime)

    _complete_day_log = []
    for _index in range(len(_dates)):

        _absent = 0

        if _dates[_index].weekday() < 5:
            # Weekday
            _log_count = 0
            if _am_time_ins[_index] != '':
                _log_count += 1
            if _am_time_outs[_index] != '':
                _log_count += 1
            if _pm_time_ins[_index] != '':
                _log_count += 1
            if _pm_time_outs[_index] != '':
                _log_count += 1

            if _log_count <= 2:
                _absent = 1

        if _absent == 0:
            _absent = ''

        _complete_day_log.append([_dates[_index],
                                  _am_time_ins[_index],
                                  _am_time_outs[_index],
                                  _pm_time_ins[_index],
                                  _pm_time_outs[_index],
                                  _lates[_index],
                                  _undertimes[_index],
                                  _absent,
                                  INPUT(_type='checkbox', _class='_field_check_box', _id=str('_field_check_' + str(_index)))])

    return dict(_complete_day_log=_complete_day_log,
                _dates=_dates,
                time_logs=_time_logs,
                logs=_logs,
                name=employee[0]['name'],
                _am_time_ins=_am_time_ins,
                _am_time_outs=_am_time_outs,
                _pm_time_ins=_pm_time_ins,
                _pm_time_outs=_pm_time_outs,
                _lates=_lates,
                _undertimes=_undertimes,
                _messages=_messages)
