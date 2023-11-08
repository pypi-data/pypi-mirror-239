import logging
import datetime
import os


class Mylogger():
    def __init__(self):
        log_dir = './logs'

        if not os.path.exists(log_dir):
            os.mkdir(log_dir)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)

        # 创建文件处理器，设置日志文件名称
        today = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        log_file = f'./logs/log_{today}.log'
        file_handler = logging.FileHandler(log_file)

        # 创建格式化器，设置日志记录的格式和时间格式
        formatter = logging.Formatter('%(asctime)s.%(msecs)03d - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        file_handler.setFormatter(formatter)

        # 将处理器添加到 logger
        logger.addHandler(file_handler)
        self.logger = logger
        #self.tabname = tabname
    def print(self,data):
        self.logger.info(str(data))

def test():
    print("测试成功")


if __name__ == '__main__':
    mylog=Mylogger()
    print = mylog.print
    print('这是一条日志记录')
    print("shjkdskdsd")
    test()
    # mylog1 = Mylogger()
    # mylog1.print('这是另一条日志记录')
# 写入日志
# logger.info('这是一条日志记录')
# logger.warning('这是一条警告信息')
# logger.error('这是一条错误信息')
# logger.critical('这是一条致命错误')

# 关闭 logger
# logging.shutdown()