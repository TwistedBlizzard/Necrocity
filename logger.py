import os, json

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
            self.subdir = os.path.join(LOG_DIR, 'log_' + log_num)
            os.mkdir(self.subdir)
            self.savedir = os.path.join(self.subdir, 'savedata')
            os.mkdir(self.savedir)
            self.path = os.path.join(self.subdir, 'log.txt')
    def log(self, data):
        if LOG:
            with open(self.path, 'a') as text_file:
                text_file.write(data + '\n')
    def save(self, name, data):
        path = os.path.join(self.savedir, name + '.json')
        with open(path, 'w') as json_file:
            json.dump(data, json_file)
