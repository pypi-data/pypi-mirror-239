import json


class Arg:
    def __init__(self, dt):
        self.week = dt['week']
        self.ml = dt['ml']
        self.reload = dt.get('reload', False)
        self.max_error_num = dt.get('max_error_num', 3)
        emails = dt.get('emails', ["1321443305@qq.com"])
        self.emails = json.loads(emails) if type(emails) == str else emails
        self.error_week = dt.get('error_week', 3600)
        self.max_run_week = dt.get('max_run_week', 3600)
        self.stop = dt.get('stop', False)

    def get(self):
        return {
            'stop': self.stop,
            'week': self.week,
            'reload': self.reload,
            'max_error_num': self.max_error_num,
            'emails': json.dumps(self.emails, ensure_ascii=False),
            'error_week': self.error_week,
            'max_run_week': self.max_run_week,
            'ml': self.ml,
        }
