import logging, os

log_fmt = logging.Formatter("%(pathname)s s%(funcName)s %(lineno)d %(levelname)s %(message)s")
def create_file(path, file_name):
    with open(path + os.sep + file_name, "w") as fp:
        pass

def delete_file(path, file_name):
    path = path + os.sep + file_name
    if os.path.exists(path):
        os.remove(path + os.sep + file_name)
        return True
    else:
        return False

def create_logger(name, level, dir, stream=False):
    log = logging.getLogger(name)
    log.setLevel(level)
    file_handler = logging.FileHandler(dir + os.sep + name + ".txt", mode="w")
    file_handler.setFormatter(log_fmt)
    log.addHandler(file_handler)

    return log

class Root_log():
    def __init__(self, master_level=logging.ERROR, master_terminal=False, max_log_age=10):


        self.format_string = "%(pathname)s s%(funcName)s %(lineno)d %(levelname)s %(message)s"
        self.root = logging.getLogger("")

        self.log_dir = os.path.dirname(__file__)+os.sep+ "logs"
        log_name = "master_log.txt"
        if not os.path.isfile(self.log_dir+ os.sep + log_name):
            create_file(self.log_dir, log_name)

        self.rootHandler = logging.FileHandler(self.log_dir + os.sep + log_name)
        self.rootHandler.setFormatter(self.format_string)
        self.root.addHandler(self.rootHandler)

        if master_terminal:
            stream = logging.StreamHandler
            self.root.addHandler(stream)
