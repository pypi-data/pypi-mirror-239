from mengling_tool2.database_tool2.sqlite import SqliteExecutor
from mengling_tool2.database_tool2.postgresql import PostgresqlExecutor
from .__body__ import *


class Sqlite_Body(Body):
    def __init__(self, name, path='D:/sqlite调度任务', table='arg',
                 table_status='status', table_taskwg='taskwg', table_result='result', table_error='error',
                 iftz=True):
        self._dbfilepath = f'{path}/{name}.db'
        super().__init__(name, table, table_status, table_taskwg, table_result, table_error,
                         arg_colmap={'stop': 'blob', 'week': 'integer', 'reload': 'blob', 'max_error_num': 'integer',
                                     'error_week': 'integer', 'max_run_week': 'integer'},
                         status_colmap={'fault_error_num': 'integer', 'last_running_seconds': 'real', 'td': 'real'},
                         kwg_colmap=None,
                         out_colmap=None,
                         iftz=iftz)

    def getSql(self):
        return SqliteExecutor(self._dbfilepath)


class Pgsql_Body(Body):
    def __init__(self, name, connect: dict, mode='', table='arg',
                 table_status='status', table_taskwg='taskwg', table_result='result', table_error='error',
                 iftz=True):
        self._connect = connect
        if mode: mode += '.'
        super().__init__(name, f'{mode}{table}', f'{mode}{table_status}', f'{mode}{table_taskwg}',
                         f'{mode}{table_result}', f'{mode}{table_error}',
                         arg_colmap={'stop': 'bool', 'week': 'int', 'reload': 'bool', 'max_error_num': 'int',
                                     'error_week': 'int', 'max_run_week': 'int'},
                         status_colmap={'fault_error_num': 'int', 'last_running_seconds': 'float', 'td': 'float'},
                         kwg_colmap={'kwg': 'text'},
                         out_colmap={'out': 'text'},
                         iftz=iftz)

    def getSql(self):
        return PostgresqlExecutor(**self._connect)


