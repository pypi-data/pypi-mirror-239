from .__redis_schedule__.run import Run, Arg
from .__redis_schedule__.save_task import SaveTask
from .__redis_schedule__.base.body import Sqlite_Body, Pgsql_Body
import time
import sys
import json


#
# # 获取调度器记录的变量字典
# def getTasKwg() -> dict:
#     return __getTasKwg__()

def _run(self, sleep_time=1, if_init=True):
    with self.getSql() as sqt:
        if if_init:
            self.print('重置状态字典')
            sqt.deleteTable(self._table_status)
        sqt.createTable(self._table_status, ['task'], key='task')
        sqt.createTable(self._table_taskwg, ['task'], key='task')
        sqt.commit()
        run_tasks, stop_tasks = [], []
        for task in self.getArgs(sqt):
            task_name = task['task']
            arg = Arg(task)
            if arg.stop:
                stop_tasks.append(task_name)
            else:
                run_tasks.append(task_name)
        self.print(f'当前运行任务:{run_tasks}')
        self.print(f'当前停止任务:{stop_tasks}')
    self.print(self.getNow())
    self.print(f'周期任务开始...间隔时间{sleep_time}s')
    while True:
        self._run()
        time.sleep(sleep_time)


class RSchedule_sqlite(Sqlite_Body, Run, SaveTask):
    run = _run


class RSchedule_pgsql(Pgsql_Body, Run, SaveTask):
    run = _run
