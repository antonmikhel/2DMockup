import os
import re
import datetime
try:
    from robot.api import logger
    endpoint_flag = False
    name = 'server'
except ImportError:
    endpoint_flag = True
    name = 'endpoint'


class RobotLogger(object):

    def __init__(self, log_dir, max_log_size_in_mb=5):
        self.log_dir = log_dir
        self.endpoint_flag = endpoint_flag
        if os.path.exists(str(self.log_dir) + name + '_debug_1.log'):
            if (os.path.getsize(str(self.log_dir) + name + '_debug_1.log') / 1024 / 1024) > max_log_size_in_mb:
                self.log_rotation_handler()
        self.logfile = open(str(self.log_dir) + name + '_debug_1.log', 'a')

    def __enter__(self):
        self.__init__(self.log_dir)
        return self

    def __exit__(self, *args):
        if self.logfile:
            self.logfile.close()

    def __del__(self):
        if self.logfile:
            self.logfile.close()

    def log_rotation_handler(self):
        import traceback
        try:
            current_logs = os.listdir(self.log_dir)
            filtered_logs = []
            for log in current_logs:  # Building suitable log candidates from logs directory into a list
                pattern = '%s_debug_\d\.log' % name
                if re.match(pattern, log):
                    filtered_logs.append(log)
            if filtered_logs:
                filtered_logs.sort(reverse=True)  # Sorting logs list
                current_ids = []
                for log in filtered_logs:  # Getting the last present log id
                    current_ids.append(int(log.split('.')[0].split('_')[-1]))
                current_ids.sort(reverse=True)
                if current_ids[0] == 9:  # Removing the oldest log
                    os.remove(self.log_dir + filtered_logs[0])
                    filtered_logs.pop(0)
                    current_ids.pop(0)
                new_logs = []  # Building new logs names list
                for log_id in current_ids:
                    new_logs.append(name + '_debug_' + str(log_id + 1) + '.log')
                new_logs.sort(reverse=True)
                for current_log, new_log in zip(filtered_logs, new_logs):  # Renaming current logs to new logs
                    os.rename(self.log_dir + current_log, self.log_dir + new_log)
        except:
            print 'Error Occurred While Handling Logs Rotation'
            print traceback.format_exc()

    @staticmethod
    def current_date():
        return str(datetime.datetime.now().date().isoformat())

    @staticmethod
    def current_time():
        return str(datetime.datetime.now().time().isoformat())

    def write(self, msg, level):
        self.logfile.write('%s@%s - %s: %s\n' % (self.current_date(), self.current_time(), level,  msg))
        if self.endpoint_flag:
            print msg
        else:
            logger.write(msg, level)

    def console(self, msg):
        self.logfile.write('%s@%s - CONSOLE: %s\n' % (self.current_date(), self.current_time(), msg))
        if self.endpoint_flag:
            print msg
        else:
            logger.console(msg)

    def info(self, msg, also_console=False):
        self.logfile.write('%s@%s - INFO: %s\n' % (self.current_date(), self.current_time(), msg))
        if self.endpoint_flag:
            print msg
        else:
            logger.info(msg, also_console=also_console)

    def debug(self, msg):
        self.logfile.write('%s@%s - DEBUG: %s\n' % (self.current_date(), self.current_time(), msg))
        if self.endpoint_flag:
            print msg
        else:
            logger.debug(msg)

    def trace(self, msg):
        self.logfile.write('%s@%s - TRACE: %s\n' % (self.current_date(), self.current_time(), msg))
        if self.endpoint_flag:
            print msg
        else:
            logger.trace(msg)

    def warn(self, msg):
        line = '%s@%s - WARN: %s\n' % (self.current_date(), self.current_time(), msg)
        self.logfile.write(line)
        if self.endpoint_flag:
            print msg
        else:
            logger.console(msg)
            logger.warn(msg)

    def error(self, msg):
        line = '%s@%s - ERROR: %s\n' % (self.current_date(), self.current_time(), msg)
        self.logfile.write(line)
        if self.endpoint_flag:
            print msg
        else:
            logger.console(msg)
            logger.error(msg)