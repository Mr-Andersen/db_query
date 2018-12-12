#!/usr/bin/env python3


def fit_atom(x, kwargs={}):
    if type(x) in kwargs:
        return kwargs[type(x)](x)
    if x is None:
        return 'NULL'
    if type(x) is bool:
        return str(int(x))
    if type(x) is str:
        return f'"{x}"'
    if type(x) is int:
        return str(x)
    raise TypeError(f'Unknown type for fitting: {type(x)}')


def fit_dict(dct, sep=' AND ', subsep=' OR ',
             key_func=str, atom_func=fit_atom):
    res = []
    for key, value in dct.items():
        if type(value) is tuple:
            it = (f'{key_func(key)} = {atom_func(subval)}' for subval in value)
            res.append(f'({subsep.join(it)})')
        else:
            res.append(f'{key} = {atom_func(value)}')
    return sep.join(res)


def fit_list(lst, sep=', ', func=str):
    return sep.join(map(func, lst))


def get_columns(db, table):
    return [i[1] for i in db.execute(f'PRAGMA table_info({table})').fetchall()]


class DummyClass:
    pass


class EntryList(DummyClass):
    def __init__(self, db, table, selection):
        DummyClass.__setattr__(self, 'db', db)
        DummyClass.__setattr__(self, 'table', table)
        DummyClass.__setattr__(self, 'selection', selection)

    def select(self, *args):
        columns = get_columns(DummyClass.__getattribute__(self, 'db'),
                              DummyClass.__getattribute__(self, 'table'))
        if len(args):
            for i in args:
                if i not in columns:
                    raise AttributeError(f'Key {i} not found in columns')
        else:
            args = columns
        selection = DummyClass.__getattribute__(self, 'selection')
        if len(selection):
            query = f'SELECT {fit_list(args)} FROM '\
                    f'{DummyClass.__getattribute__(self, "table")} WHERE '\
                    f'{selection}'
        else:
            query = f'SELECT {fit_list(args)} FROM '\
                    f'{DummyClass.__getattribute__(self, "table")}'
        res = DummyClass.__getattribute__(self, 'db').execute(query).fetchall()
        return res

    def update(self, **kwargs):
        columns = get_columns(DummyClass.__getattribute__(self, 'db'),
                              DummyClass.__getattribute__(self, 'table'))
        assert(len(kwargs) > 0)
        for i in kwargs.keys():
            if i not in columns:
                raise AttributeError(f'Key {i} not found in columns')
        selection = DummyClass.__getattribute__(self, 'selection')
        if len(selection):
            query = f'UPDATE {DummyClass.__getattribute__(self, "table")} '\
                    f'SET {fit_dict(kwargs, sep=", ")} WHERE '\
                    f'{selection}'
        else:
            query = f'UPDATE {DummyClass.__getattribute__(self, "table")} '\
                    f'SET {fit_dict(kwargs, sep=", ")}'
        DummyClass.__getattribute__(self, 'db').execute(query)
        DummyClass.__getattribute__(self, 'db').commit()

    def delete(self):
        selection = DummyClass.__getattribute__(self, 'selection')
        if len(selection):
            query = 'DELETE FROM '\
                    f'{DummyClass.__getattribute__(self, "table")} '\
                    f'WHERE {selection}'
        else:
            query = 'DELETE FROM '\
                    f'{DummyClass.__getattribute__(self, "table")}'
        DummyClass.__getattribute__(self, 'db').execute(query)
        DummyClass.__getattribute__(self, 'db').commit()

    def __getitem__(self, name):
        return [i[0] for i in self.select(name)]

    def __getattr__(self, name):
        return [i[0] for i in self.select(name)]

    def __setitem__(self, name, value):
        return self.update(**{name: value})

    def __setattr__(self, name, value):
        return self.update(**{name: value})

    def __iter__(self):
        return iter(self.select())

    def __repr__(self):
        return str(list(self))

    def __call__(self, *args):
        return self.select(*args)

    def __len__(self):
        return len(self.select())


class Table:
    def __init__(self, db, table):
        if not len(get_columns(db, table)):
            raise Exception(f'Table "{table}"" doesn\'t exist')
        self.db = db
        self.table = table

    def where(self, selection=None, **kwargs):
        if selection and len(kwargs):
            raise TypeError('Table.where doesn\'t accept both '
                            'selection and **kwargs')
        if selection:
            return EntryList(self.db, self.table, selection)
        return EntryList(self.db, self.table, fit_dict(kwargs))

    def insert(self, *args, **kwargs):
        if len(args) and len(kwargs):
            raise TypeError('Table.insert doesn\' accept both '
                            '*args and **kwargs')
        if not len(args) and not len(kwargs):
            raise TypeError('Table.insert needs *args or **kwargs')
        if len(kwargs):
            query = f'INSERT INTO {self.table} ({fit_list(kwargs.keys())}) '\
                    f'VALUES ({fit_list(kwargs.values(), func=fit_atom)})'
        else:
            query = f'INSERT INTO {self.table} '\
                    f'VALUES ({fit_list(args, func=fit_atom)})'
        self.db.execute(query)
        self.db.commit()

    def delete(self, *args, **kwargs):
        self.where(*args, **kwargs).delete()

    def __call__(self, *args, **kwargs):
        return self.where(*args, **kwargs)
