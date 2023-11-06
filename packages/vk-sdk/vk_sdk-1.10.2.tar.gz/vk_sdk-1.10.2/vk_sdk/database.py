"""Custom SQLite alchemy"""

import json
import os
import re
import sqlite3
from operator import getitem
from sqlite3 import Row
from sys import version_info
from typing import Any, AnyStr, Iterable
from warnings import warn
import jsonxx

from . import thread, timeExtension
from jsonxx.listx import ListX


def getter(x: Any, attr: AnyStr): return getattr(x, attr, x)


SUPPORTS_DROP_COLUMNS = version_info.major >= 3 and version_info.minor > 9


DEFAULT_CONFIG = """
{
    "db_file": "data/db.sqlite3",
    "db_backups": false,
    "db_backups_folder": "backups/",
    "db_backup_interval": 43200,
    "sync_timezone": "Europe/Moscow",
    "vk_api_key": ""
}
"""


def on_create_config():
    print("vk_sdk config created. Make sure to fill vk_api_key before running long pooling code. Happy coding!")
    os._exit(0)


config = jsonxx.load_advanced(
    "config.json", content=DEFAULT_CONFIG, createCallback=on_create_config)


def attrgetter(x: Any): return getter(x, "value")


def _formAndExpr(baseSql, argsList=None, getattrFrom=None, add=None):
    """
    The formAndExpr function takes a baseSql string, an argsList list, and a getattrFrom object. It then adds the attributes from the add list to the baseSql string and appends their values to argsList.
    Used internally from module

    :param baseSql: Used to Store the sql query that will be used to update the database.
    :param argsList: Used to Store the values of the parameters in add.
    :param getattrFrom: Used to Get the values from the object.
    :param add: Used to Add the column names to the basesql string.
    :return: A string that is a concatenation of the strings in add, each followed by an "and" and surrounded by open and close parentheses.
    """
    method = getitem if isinstance(getattrFrom, dict) else getattr
    if argsList is None:
        argsList = ListX()
    if any([x is None for x in (getattrFrom, add)]):
        raise ValueError
    for i, k in enumerate(add):
        baseSql += f"{k}=?"
        argsList.append(method(getattrFrom, k))
        if i != len(add) - 1:
            baseSql += " and "
    return baseSql, argsList


def to_sneak_case(string):
    """
    The to_sneak_case function converts a string to snake_case.

    Args:
        string (str): The input string. 
    Returns:
        str: The output snake_case formatted string.

    :param string: String that will be converted to sneak case.
    :return: A string in sneak case.
    """
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()


def convert_to_list_if_needed(element):
    if not isinstance(element, list):
        return ListX([element])
    else:
        return ListX(element)


class Struct:
    table_map = {}

    @classmethod
    def extract_table_name(cls):
        """Searches for table_name in Struct"""
        if hasattr(cls, "table_name"):
            return getattr(cls, "table_name")
        else:
            return to_sneak_case(cls.__name__)

    @classmethod
    def extract_save_by(cls):
        """
        The extract_save_by function is used to extract the save_by attribute from a class.

        If the class has no save_by attribute, it will look for any attributes that are instances of Sqlite3Properties that has unique modifier in their "value".

        :param cls: Used to Access the class object of the current instance.
        :return: A list of the names of all the attributes that are marked for saving.
        """
        if hasattr(cls, "save_by"):
            return convert_to_list_if_needed(attrgetter(cls.save_by))
        for k, v in vars(cls).items():
            if isinstance(v, Sqlite3Property) and "unique" in v.type:
                return ListX(k)

    def __getstate__(self):
        return _formAndExpr(f"select * from {self.table_name} where ", [], self, self.save_by)

    def __setstate__(self, t):
        return db.select_one_struct(t[0], t[1], fromSerialized=self)

    def __init_subclass__(cls) -> None:
        """
        The __init_subclass__ function is called when some class derives from our Struct
        It`s purpose is to ensure that all subclasses of the base class have their own table_name and save_by attributes, 
        and that they are kept in sync with the base class via an updated table_map.

        :param cls: Used to Access the class object.
        :return: The class object that is being defined.
        """
        cls.table_name = cls.extract_table_name()
        cls.save_by = cls.extract_save_by()
        cls.table_map[cls.table_name] = cls
        return super().__init_subclass__()

    def __new__(cls, **kwargs):
        create_new = kwargs.get("create_new", True)
        instance = super().__new__(cls)
        instance.setattr("old_struct", None, ignore_duplicates=False)
        if kwargs:
            expr = f"select * from {cls.table_name} where "
            expr, args = _formAndExpr(
                expr, getattrFrom=kwargs, add=cls.save_by)
            old_struct = cls.db.select_one_struct(expr, args)
            if old_struct is None and create_new is False:
                return None
            instance.old_struct = old_struct
        return instance

    def __init__(self, create_new=None, **kwargs) -> None:
        if kwargs:
            for key, value in kwargs.items():
                setattr(self, key, value)
            if all(self.save_by.map(lambda it: it in kwargs.keys())):
                if self.old_struct is None:
                    keys, values = ListX(), ListX()
                    vrs = self.vars()
                    for key, value in vrs.items():
                        keys.append(key)
                        values.append(kwargs[key]) if kwargs.get(
                            key) is not None else values.append(value)
                    insert_string = f"insert or ignore into {self.table_name} ({','.join(keys)}) values ({values.map(lambda _: '?').join(',')})"
                    self.db.execute(insert_string, values)
                    variables = self.vars()
                    self.fill(variables.keys(), variables)
                else:
                    keys = kwargs.keys()
                    values = ListX(kwargs.values()).find_all(
                        lambda it: it not in self.save_by)
                    d = dict(zip(keys, values))
                    for k, v in d.items():
                        self.old_struct.setattr(k, v)
                    variables = self.old_struct.vars()
                    self.fill(variables.keys(), variables)
                self.initialized = True

        super().__init__()

    @classmethod
    def select_all(cls, **kwargs):
        if len(kwargs) > 0:
            expr, args = _formAndExpr(
                f"select * from {cls.table_name} where ", getattrFrom=kwargs, add=kwargs)
            return cls.db.select_all_structs(expr, args)
        else:
            return cls.db.select_all_structs(f"select * from {cls.table_name}")

    @classmethod
    def row_at(cls, num):
        return cls.db.select_one_struct(f"select * from {cls.table_name} limit 1 offset {num}")

    @classmethod
    def first(cls): return cls.row_at(0)

    def boundStructByAction(self, key, data):
        """Bounds struct by action to a given data (list or dict). Struct by action will handle the watching on elements change."""
        structByAction = jsonxx.JsonX(data, saver=lambda _: self.db.save_struct_by_action(_,
                                                                                                          self.table_name, key, self.save_by, self))
        return structByAction

    def destroy(self):
        """
        The destroy function deletes Struct record from db.
        """
        sql = f"delete from {self.table_name} where "
        sql, lst = _formAndExpr(sql, getattrFrom=self, add=self.save_by)
        self.db.execute(sql, lst)

    def setattr(self, key, value, write_to_database=True, ignore_duplicates=True):
        """
        The setattr function is a helper function that allows us to write the value of an attribute to the database.
        It is called when we set an attribute on a Struct, and it will only write to the database if:
        - The struct has been initialized (i.e., it's ready to use and that's not some internal module call)
        - The key being assigned matches one of our attributes (otherwise, we might be trying to assign something that doesn't correspond with any known field in our struct)
        - The value being assigned is different from what was previously stored for this key in our struct (unless ignore_duplicates=True). This prevents us from writing unnecessary updates.
        Otherwise it's some internal package calls.

        :param key: Used to Specify the attribute that is to be set.
        :param value: Used to Set the value of an attribute.
        :param write_to_database=True: Do we need to write changed value to db.
        :param ignore_duplicates=True: Used to Avoid writing the same value to the database multiple times.
        :return: None.
        """
        prev = getattr(self, key, None)
        if prev == value and ignore_duplicates:
            return
        if write_to_database and getattr(self, "initialized", False):
            if isinstance(prev, tuple(jsonxx.ExtensionBase.classes.values())):
                # resave
                super().__setattr__(key, self.boundStructByAction(key, value))
                getattr(self, key).save()
            else:
                self.db.write_struct(self, key, value)
                super().__setattr__(key, value)
        else:
            super().__setattr__(key, value)

    def vars(cls):
        """
        The vars function is used to extract the class variables from a class.

        :param cls: Used to Indicate the class that we want to get attributes from.
        :return: A dictionary of the class's namespace.
        """
        attrs = {k: getattr(cls, k) for k in dir(cls)}
        return {k: v for k, v in attrs.items() if not k.startswith(
                "__") and k not in ["table_name", "save_by", "initialized", "table_map", "use_db", "db", "old_struct"] and (not callable(v) or type(v) in jsonxx.ExtensionBase.classes)}

    def fill(self, keys, getitemfrom):
        """Fills attributes mapped from list[str] keys to getitemfrom object to our Struct"""
        for k in keys:
            value = jsonxx.JsonX.accept(getitemfrom[k], saver=lambda _: self.db.save_struct_by_action(_,
                                                                                                                     self.table_name, k, self.save_by, self))

            if isinstance(getattr(self, k), bool):
                value = self.str2bool(value)

            self.setattr(k, value, False)

    def __setattr__(self, name: str, value: Any) -> None:
        self.setattr(name, value)

    def str2bool(self, v):
        if hasattr(v, "lower"):
            return v.lower() in ("true", "1")
        return v

    def __repr__(self) -> str:
        return f"{self.table_name}({', '.join([f'{x}={y}' for x, y in self.vars().items()])})"


class Sqlite3Property(object):
    def __init__(self, x: Any, y: AnyStr):
        self.value = x
        self.type = y


class Database:

    typeToTypeCache = {str: "text", dict: "str", list: "str",
                       float: "real", type(None): "null", int: "int", bool: "bool", bytes: "blob"}
    db_cache = {}

    def __new__(cls, settings, **kwargs):
        file = settings["db_file"]
        if (instance := cls.db_cache.get(file)) is None:
            instance = super().__new__(cls)
            db_short = os.path.basename(
                os.path.splitext(file)[0])
            cls.db_cache[db_short] = instance  # short path
            cls.db_name = db_short  # instance.db_name ?
            cls.db_cache[file] = instance
            return instance
        return instance

    def end_changes(self):
        if self.need_commit and self.stash:
            self.db.commit()
            self.need_commit = False
            self.stash = False

    def begin_changes(self):
        self.stash = True

    def __init__(self, settings: dict, **kwargs):
        self.settings = settings
        self.backup_folder = self.settings["db_backups_folder"]
        folder = os.path.split(self.settings["db_file"])[0]

        if not os.path.exists(folder):
            os.makedirs(folder)
        self.file = self.settings["db_file"]
        self.db = sqlite3.connect(
            self.settings["db_file"], check_same_thread=False, **kwargs)
        self.row_factory = sqlite3.Row
        self.db.row_factory = self.row_factory
        self.cursor = self.db.cursor()
        self.stash = False
        self.need_commit = False

        is_main_db = self.settings["db_file"] == config["db_file"]

        if is_main_db:
            global db
            db = self

        for struct in Struct.table_map.values():
            if (not is_main_db and not hasattr(struct, "use_db")) or (hasattr(struct, "use_db") and self.db_cache.get(struct.use_db) != self):
                continue
            iterable = -1
            rows = []
            struct.db = self
            variables = struct.vars(struct)
            for key, value in variables.items():
                iterable += 1
                real_value = attrgetter(value)
                rows.append(
                    f"{key} {self.convert_type(real_value)} {getattr(value, 'type', '')} default \"{real_value}\"")
            self.execute(
                f"create table if not exists {struct.table_name} ({', '.join(rows)})")
            table_fields = self.get_column_names(struct.table_name)
            for iterable, field in enumerate(variables.keys()):
                if field not in table_fields:
                    self.execute(
                        f"alter table {struct.table_name} add column {rows[iterable]}")
            skipped_drop = ListX()
            for field in list(table_fields):
                if field not in variables:
                    if SUPPORTS_DROP_COLUMNS or config.get("disable_column_drop_checks"):
                        self.execute(
                            f"alter table {struct.table_name} drop column {field}")
                    else:
                        skipped_drop.append(
                            f"{field} (struct {struct.table_name})")
            if len(skipped_drop) > 0:
                warn(f"There are {len(skipped_drop)} columns waiting to be deleted from database {self.db_name}." +
                     f"Unfortunately, your python version doesn't support this sqlite3 operation. Please, delete the following fields by yourself:\n" +
                     f"{''.join(skipped_drop)}\n\n(You can try setting disable_column_drop_checks to True in config file and see if it works)")
        if self.settings["db_backups"]:
            thread.every(self.settings["db_backup_interval"], name="Backup")(
                self.backup)

    def backup(self):
        if not self.settings["db_backups"]:
            return

        rawName = self.file.split("/")[-1]
        manager = thread.ThreadManager()
        manager.changeInterval(
            "Backup", self.settings["db_backup_interval"])
        backup_table = sqlite3.connect(
            f"{self.backup_folder}backup_{timeExtension.Timestamp.now()}_{rawName}")
        self.db.backup(backup_table)

    def select(self, query: AnyStr, args=None):
        if args is None:
            args = []
        self.cursor.execute(query, args)
        return self.cursor.fetchall()

    def select_one(self, query: AnyStr, *args):
        if isinstance(args, list):
            self.cursor.execute(query, [str(x) for x in args])
        else:
            self.cursor.execute(query, *args)
        return self.cursor.fetchone()

    def write_struct(self, structToWrite: Struct, changedKey: AnyStr, newValue: Any):
        table = structToWrite.table_name
        unique_fields = Struct.table_map[table].save_by
        sql = f"update or ignore {table} set {changedKey} = ? where "
        argsList = [newValue]
        sql, argsList = _formAndExpr(
            sql, argsList, structToWrite, unique_fields)
        self.execute(sql, argsList)

    def select_one_struct(self, query: AnyStr, *args: tuple or jsonxx.JsonX,
                          selectedStruct: Row = None,
                          fromSerialized=None, table_name=None):
        table_name = self.parse_table_name(query, table_name)
        struct = self.select_one(
            query, *args) if selectedStruct is None else selectedStruct
        if struct is None:
            return None
        if not isinstance(table_name, str):
            raise Exception(
                f"Table name's type is not string (table_name was not provided correctly?)\n{query=}\n{args=}\n{table_name=}")
        myStruct: Struct = Struct.table_map[table_name](
        ) if fromSerialized is None else fromSerialized
        if struct is None:
            return None
        myStruct.fill(struct.keys(), struct)
        myStruct.setattr("initialized", True, write_to_database=False)
        return myStruct

    def select_all_structs(self, query: AnyStr, *args) -> ListX:
        structs = ListX(self.select(query, *args))
        return ListX([self.select_one_struct(query, *args, selectedStruct=x) for x in structs])

    def save_struct_by_action(self, value, table_name: AnyStr, key: Any,
                              unique_field: Iterable, parent_struct: Struct):
        baseSql = f"update {table_name} set {key} = ? where "
        argsList = [value]
        baseSql, argsList = _formAndExpr(
            baseSql, argsList, parent_struct, unique_field)
        self.execute(baseSql, argsList)

    def execute(self, query: AnyStr, args=None):
        if args is None:
            args = []
        for i, k in enumerate(args):
            if isinstance(k, tuple(jsonxx.ExtensionBase.classes.values())):
                args[i] = jsonxx.JsonX(k).dumps()
        self.cursor.execute(query, args)
        if self.stash:
            self.need_commit = True
        else:
            self.db.commit()
        return self.cursor

    def get_column_names(self, table: AnyStr):
        select = self.cursor.execute(f"select * from {table}")
        return [x[0] for x in select.description]

    def parse_table_name(self, query, fromCached=None):
        if fromCached is None:
            return list(tables_in_query(query))[0]
        return fromCached

    def get_table_names(self):
        return [x["name"] for x in self.select("SELECT name FROM sqlite_master WHERE type='table'")]

    @staticmethod
    def convert_type(value):
        return Database.typeToTypeCache[type(value)]


db: Database = None


# https://grisha.org/blog/2016/11/14/table-names-from-sql/
def tables_in_query(sql_str):
    q = re.sub(r"/\*[^*]*\*+(?:[^*/][^*]*\*+)*/", "", sql_str)
    lines = [line for line in q.splitlines(
    ) if not re.match(r"^\s*(--|#)", line)]
    q = " ".join([re.split(r"--|#", line)[0] for line in lines])
    tokens = re.split(r"[\s)(;]+", q)
    result = set()
    get_next = False
    for tok in tokens:
        if get_next:
            if tok.lower() not in ["", "select"]:
                result.add(tok)
            get_next = False
        get_next = tok.lower() in ["from", "join"]

    return result
