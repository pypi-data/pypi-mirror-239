import easygui
import json
import time
import sys
import traceback
from datetime import datetime
from multiprocessing import Process
from threading import Thread
from mengling_tool2.database_tool2.__sqltool__ import TemplateSQLTool
from mengling_tool2.tools.notice import emailSend
from mengling_tool2.tools.time import TimeTool
from threading import Lock, get_ident


# print捕获者
class Printer:
    def __init__(self):
        # self._lock = Lock()
        self.contendt = {}

    def popContent(self):
        tid = get_ident()
        content = self.contendt.get(tid, '')
        self.flush()
        return content

    def write(self, txt):
        tid = get_ident()
        if self.contendt.get(tid) is None: self.contendt[tid] = ''
        self.contendt[tid] += txt

    def flush(self):
        tid = get_ident()
        self.contendt[tid] = ''


class Body:
    def __init__(self, name, table, table_status, table_taskwg, table_result, table_error,
                 arg_colmap, status_colmap, kwg_colmap, out_colmap, iftz):
        self._name = name
        self._table = table
        self._table_status = table_status
        self._table_taskwg = table_taskwg
        self._table_result = table_result
        self._table_error = table_error
        self._arg_colmap = arg_colmap
        self._status_colmap = status_colmap
        self._kwg_colmap = kwg_colmap
        self._out_colmap = out_colmap
        self._iftz = iftz
        self.pter = Printer()
        sys.stdout = self.pter

    def getSql(self):
        raise ValueError('需要实现')

    def getArgs(self, sqt: TemplateSQLTool) -> list[dict]:
        argdts = sqt.select('*', self._table)
        return argdts

    def getStatus(self, sqt: TemplateSQLTool, task_name) -> dict:
        status = sqt.select('*', self._table_status, where=f"task='{task_name}'")
        return status[0] if status else {}

    def getKwg(self, sqt: TemplateSQLTool, task_name) -> dict:
        kwgs = sqt.select('*', self._table_taskwg, where=f"task='{task_name}'")
        return json.loads(kwgs[0]['kwg']) if kwgs else {}

    def setArg(self, sqt: TemplateSQLTool, task_name, arg, if_commit=True):
        sqt.insert_create_dt(self._table, {'task': task_name, **arg.get()}, if_auto_lie=True, if_nan=True,
                             colmap=self._arg_colmap, key='task')
        if if_commit: sqt.commit()

    def setStatus(self, sqt: TemplateSQLTool, task_name, status, if_commit=True):
        sqt.delete(self._table_status, f"task='{task_name}'")
        sqt.insert_create_dt(self._table_status, {'task': task_name, **status.get()}, if_auto_lie=True, if_nan=True,
                             colmap=self._status_colmap, key='task')
        if if_commit: sqt.commit()

    def setKwg(self, sqt: TemplateSQLTool, task_name, kwg: dict, if_commit=True):
        sqt.delete(self._table_taskwg, f"task='{task_name}'")
        sqt.insert_create_dt(self._table_taskwg, {'task': task_name, 'kwg': json.dumps(kwg, ensure_ascii=False)},
                             if_auto_lie=True, if_nan=True, colmap=self._kwg_colmap)
        if if_commit: sqt.commit()

    def setResult(self, sqt: TemplateSQLTool, task_name, edt, result, if_commit=True):
        table = f'{self._table_result}_{task_name}'
        sqt.insert_create_dt(table, {'date': edt, 'out': result}, if_nan=True, colmap=self._out_colmap)
        if if_commit: sqt.commit()

    def setError(self, sqt: TemplateSQLTool, task_name, edt, error, if_commit=True):
        table = f'{self._table_error}_{task_name}'
        sqt.insert_create_dt(table, {'date': edt, 'out': error}, if_nan=True, colmap=self._out_colmap)
        if if_commit: sqt.commit()

    def getNow(self):
        return datetime.fromtimestamp(time.time()).strftime("%Y-%m-%d %H:%M:%S")

    def print(self, *txts):
        sys.__stdout__.write(' '.join(txts) + '\n')
        sys.__stdout__.flush()
