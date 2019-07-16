db.define_table('employees',
                Field('employee_id', 'integer', requires=IS_NOT_EMPTY()),
                Field('name', requires=IS_NOT_EMPTY()),
                Field('section_id', 'integer', requires=IS_NOT_EMPTY()),
               migrate=True,
               plural='Employees')

db.define_table('logs',
               Field('log_file', 'upload'),
               Field('uploaded', 'datetime', writable=False), 
               Field('remarks', 'text'),
               migrate=True,
               plural='Logs Uploaded'
               )
