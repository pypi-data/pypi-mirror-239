from .mold.arg import Arg
from .mold.status import Status
from .base.body import *


class _Ceil(Body):
    # 执行开始
    def _ceil_start(self, task_name, status: Status, max_run_week) -> dict:
        with self.getSql() as sqt:
            sdt = status.run(max_run_week)
            if self._iftz: self.print(f"\x1b[33m{sdt} {task_name} 开始执行...\x1b[0m")
            self.setStatus(sqt, task_name, status)
            kwg = self.getKwg(sqt, task_name)
            return kwg

    # 执行结束
    def _ceil_end(self, exec_result, exec_error, exec_taskwg,
                  task_name, status: Status, week, error_week, emails):
        edt = self.getNow()
        with self.getSql() as sqt:
            if exec_result: self.setResult(sqt, task_name, edt, exec_result, if_commit=False)
            # 变化
            if exec_error:
                self.setError(sqt, task_name, edt, exec_error, if_commit=False)
                ifemail = status.error(error_week)
                if ifemail: emailSend(f'{self._name}-{task_name} 任务错误!', exec_error, mane_mails=emails)
            else:
                status.wait(week)
            self.setStatus(sqt, task_name, status, if_commit=False)
            self.setKwg(sqt, task_name, exec_taskwg, if_commit=False)
            sqt.commit()
        if self._iftz:
            self.print(f"\x1b[{31 if exec_error else 32}m{edt} {task_name} {'出现错误-' if exec_error else ''}执行结束!\n"
                       f"执行时间:{status.last_running_seconds:.4f}s"
                       f"\n下次执行:{status.next_time}\x1b[0m")

    # 单任务执行,不能修改固定参数
    def _ceil(self, task_name, arg: Arg, status: Status):
        __exec_taskwg__ = self._ceil_start(task_name, status, arg.max_run_week)
        ml = arg.ml.replace('\n', '\n    ')
        if arg.reload:
            self.pter = Printer()
            sys.stdout = self.pter
        try:
            exec(f'''
import traceback,sys
__ml_exec_error__ = None
try:
    {ml}
except:
    __ml_exec_error__=traceback.format_exc()
            '''.strip())
            ml_error = None
        except:
            ml_error = traceback.format_exc()
        # 从当前命名空间中获取对象,键名与赋值的变量名需要不同
        ml_result = self.pter.popContent()
        ml_error = ml_error if ml_error else locals()["__ml_exec_error__"]
        self._ceil_end(ml_result, ml_error, __exec_taskwg__, task_name, status,
                       arg.week, arg.error_week, arg.emails)


class Run(_Ceil):
    def __run(self, task_name, task_arg: Arg, task_status: Status):
        # 多进程或多线程运行
        func = Process if task_arg.reload else Thread
        t = func(target=self._ceil,
                 args=(task_name, task_arg, task_status))
        t.daemon = True
        t.start()

    # 一次周期
    def _run(self):
        with self.getSql() as sqt:
            for task in self.getArgs(sqt):
                try:
                    task_name = task['task']
                    task_arg = Arg(task)
                    if task_arg.stop: continue
                    # 获取状态
                    task_status = Status(self.getStatus(sqt, task_name), task_arg.max_error_num)
                    # 判断执行
                    status = task_status.getStatus()
                    if status == '等待':
                        self.__run(task_name, task_arg, task_status)
                    elif status == '卡死':
                        emailSend(f'{self._name}-{task_name} 任务警告!',
                                  f'任务执行时间过长!\ntask_arg:{task_arg}\ntask_status:{task_status}',
                                  mane_mails=task_arg.emails)
                        task_status.timeout(task_arg.max_run_week)
                        self.setStatus(sqt, task_name, status)
                except:
                    self.print(task_name, '错误!')
                    traceback.print_exc()
