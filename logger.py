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
            x = 0
            while True:
                log_num = str(x)
                self.subdir = os.path.join(LOG_DIR, 'log_' + log_num)
                try:
                    os.mkdir(self.subdir)
                except OSError:
                    x += 1
                    continue
                break
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
            json.dump(data, json_file, indent=4)
