# -*- coding: utf-8 -*-
# try something like
def index():
    return dict(message="hello from tables.py")

@auth.requires_login()
def table():
    response.view = 'generic.html' # use a generic view
    tablename = request.args(0)
    if not tablename in db.tables: raise HTTP(403)
    grid = SQLFORM.smartgrid(db[tablename], args=[tablename], deletable=False, editable=True)
    return dict(grid=grid)
