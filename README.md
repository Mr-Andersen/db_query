# db_query
Python3 module for comfortable using of database (tested for sqlite3)

Usage:

    import db_query
    table = db_query.Table(sqlite3.connect('datebase.db'), 'tablename')
    table.where(column1=value1, column2=value2) # -> list of rows matching given equalities
    table.where(column1=(value11, value12), column2=value2) # -> executes 'SELECT * FROM tablename WHERE (column1 = value11 OR column1 = value12) AND column2 = value2' and returns result
    table.where_raw('column1 LIKE "val%1" AND column2 = "kek"') # "raw" sql query (beware of vulnerabilities)
    table(...) # -> table.where(...)
    table.insert(value1, value2, ...) # insert new row into table
    table.insert(column1=value1) # this also works - can be used if columns have default values
    table.where(...).select(column1, column2) # executes 'SELECT column1, column2 FROM tablename WHERE ...' (and returnes result)
    table.where(...).select() # -> table.where(...)
    table.where(...).column1 # -> [_[0] for _ in table.where(...).select('column1')]
    table.where(...)['column1'] # same
    table.where(...).update(column1=value1, column2=value2) # update table
    table.where(...).column1 = new_value # -> table.where(...).update(column1=new_value)
    table.where(...).delete() # delete matching rows
    table.delete(*args, **kwargs) # same
