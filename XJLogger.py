import os
from datetime import datetime

# ====================================================================================
# XJLogger логика логирования конвертации
# ====================================================================================


class XJLogger:

    @staticmethod
    def log(message):
        file = open(os.getcwd() + '\\logs.txt', 'a')
        file.write(str(datetime.now()) + "  " + message + '\n')
        file.close()

    @staticmethod
    def start_write_logs(clear):
        if os.path.isfile(os.getcwd() + '\\logs.txt'):
            if clear:
                os.remove(os.getcwd() + '\\logs.txt')
            else:
                file = open(os.getcwd() + '\\logs.txt', 'a')
                file.write('\n\n\n\n')
                file.close()
