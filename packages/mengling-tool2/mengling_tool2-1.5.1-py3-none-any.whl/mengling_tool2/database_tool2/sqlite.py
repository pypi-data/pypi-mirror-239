# -*- coding: UTF-8 -*-

import sqlite3
from .__sqltool__ import TemplateSQLTool
import os


# postgresql执行类
class SqliteExecutor(TemplateSQLTool):
    def __init__(self, dbfilepath, if_new=True, ifassert=True, iftz=False):
        # SELECT * FROM sqlite_master 可以查询详细信息,包含表的创建sql
        self.dbfilepath = dbfilepath

        # 打开数据库连接
        def db_func():
            if not if_new and not os.path.exists(self.dbfilepath):
                raise ValueError(f'没有 {self.dbfilepath} 文件!')
            db = sqlite3.connect(self.dbfilepath)
            return db

        TemplateSQLTool.__init__(self, db_func, ifassert, iftz, placeholder='?', default_lie_class='TEXT')

    def getTablestr(self, table, **kwargs):
        return f'"{table}"'

    def getLiestrs(self, lies, **kwargs):
        if type(lies) == str:
            if lies in {'*', '1', 'count(1)'}:
                return [lies]
            else:
                lies = [lies]
        lies = [f'"{lie}"' for lie in lies]
        return lies

    def ifExist(self, table):
        b = self.run(f"SELECT 1 FROM sqlite_master WHERE type='table' AND name='{table}'")
        return b and len(self.cursor.fetchall()) > 0
