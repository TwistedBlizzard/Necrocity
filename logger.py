import os

LOG = True
LOG_DIR = 'logs'

class Logger:
    def __init__(self):
        if LOG:
            try:
                os.mkdir(LOG_DIR)
            except OSError:
                pass
            logs = [0]
            for log in os.listdir(LOG_DIR):
                fname, ext = os.path.splitext(log)
                if ext == '.txt' and fname.startswith('log_'):
                    log_num = int(fname.split('_')[1])
                    logs.append(log_num)
            log_num = str(max(logs) + 1)
            self.path = os.path.join(LOG_DIR, 'log_%s.txt' % (log_num))
    def log(self, data):
        if LOG:
            with open(self.path, 'a') as text_file:
                text_file.write(data + '\n')
