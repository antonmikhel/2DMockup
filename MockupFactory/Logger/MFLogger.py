import glob
import os
import re
import datetime
import time


class MFLogger(object):

    def __init__(self, log_dir, name, start_time=time.time(), max_log_size_in_mb=5):
        self.log_dir = os.path.join(log_dir)
        self.name = name
        self.__start_time = start_time
        if os.path.exists(os.path.join(self.log_dir, self.name + '_debug_1.log')):
            if (os.path.getsize(os.path.join(self.log_dir,
                                             self.name + '_debug_1.log')) / 1024 / 1024) > max_log_size_in_mb:
                self.log_rotation_handler()
        self.logfile = open(os.path.join(self.log_dir, self.name + '_debug_1.log'), 'a')

    def __enter__(self):
        self.__init__(self.log_dir, self.name)
        return self

    def __exit__(self):
        if self.logfile:
            self.logfile.close()

    def __del__(self):
        if self.logfile:
            self.logfile.close()

    def log_rotation_handler(self):
        import traceback
        try:
            current_logs = [os.path.basename(_) for _ in glob.glob(os.path.join(self.log_dir, "*.log"))]
            filtered_logs = []
            for log in current_logs:  # Building suitable log candidates from logs directory into a list
                pattern = '%s_debug_\d\.log' % self.name
                if re.match(pattern, log):
                    filtered_logs.append(log)
            if filtered_logs:
                filtered_logs.sort(reverse=True)  # Sorting logs list
                current_ids = []
                for log in filtered_logs:  # Getting the last present log id
                    current_ids.append(int(log.split('.')[0].split('_')[-1]))
                current_ids.sort(reverse=True)
                if current_ids[0] == 9:  # Removing the oldest log
                    os.remove(os.path.join(self.log_dir, filtered_logs[0]))
                    filtered_logs.pop(0)
                    current_ids.pop(0)
                new_logs = []  # Building new logs names list
                for log_id in current_ids:
                    new_logs.append(self.name + '_debug_' + str(log_id + 1) + '.log')
                new_logs.sort(reverse=True)
                for current_log, new_log in zip(filtered_logs, new_logs):  # Renaming current logs to new logs
                    print current_log
                    print new_log
                    os.rename(os.path.join(self.log_dir, current_log), os.path.join(self.log_dir, new_log))
        except Exception as rotation_err:
            print 'Error Occurred While Handling Logs Rotation - %s' % str(rotation_err)
            print traceback.format_exc()

    @staticmethod
    def current_date():
        return str(datetime.datetime.now().date().isoformat())

    @staticmethod
    def current_time():
        return str(datetime.datetime.now().time().isoformat())

    def print_message(self, msg, level):
        msg_time = time.time()
        print "|{0:.2f}s|{1:s}>>>{2:s}".format(msg_time - self.__start_time, level, msg)

    def write(self, msg, level):
        self.print_message(msg, level)
        self.logfile.write('%s@%s - %s: %s\n' % (self.current_date(), self.current_time(), level,  msg))

    def console(self, msg):
        self.print_message(msg, "CONSOLE")
        self.logfile.write('%s@%s - CONSOLE: %s\n' % (self.current_date(), self.current_time(), msg))

    def info(self, msg):
        self.print_message(msg, "INFO")
        self.logfile.write('%s@%s - INFO: %s\n' % (self.current_date(), self.current_time(), msg))

    def debug(self, msg):
        self.print_message(msg, "DEBUG")
        self.logfile.write('%s@%s - DEBUG: %s\n' % (self.current_date(), self.current_time(), msg))

    def trace(self, msg):
        self.print_message(msg, "TRACE")
        self.logfile.write('%s@%s - TRACE: %s\n' % (self.current_date(), self.current_time(), msg))

    def warn(self, msg):
        self.print_message(msg, "WARN")
        line = '%s@%s - WARN: %s\n' % (self.current_date(), self.current_time(), msg)
        self.logfile.write(line)

    def error(self, msg):
        self.print_message(msg, "ERROR")
        line = '%s@%s - ERROR: %s\n' % (self.current_date(), self.current_time(), msg)
        self.logfile.write(line)
