# pip install --no-index --find-links=https://pypi.org/simple/ lyysdk
#https://pypi.org/project/lyysdk/#description
#pip install lyypy -i https://pypi.org/simple/ --trusted-host pypi.org --upgrade
"""
python setup.py sdist bdist_wheel
twine upload dist/*
pip install --upgrade lyysdk -i https://pypi.org/simple/ --trusted-host pypi.org
"""
import time
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler
"""



"""


def assign(list1, list2):
    """
    把服务器列表依次、循环分配到股票代码，让每个代码拥有专属服务器
    """
    dict_result = {}
    iter_list2 = iter(list2)
    for idx, val in enumerate(list1):
        try:
            dict_result[val] = next(iter_list2)
        except StopIteration:
            iter_list2 = iter(list2)
            dict_result[val] = next(iter_list2)
    dict_result = {k: v for k, v in dict_result.items() if v is not None}
    return dict_result

def 万能股票代码(原始股票代码, 需要的示例):
    """
    示例随便啥股票代码，关键是样式。比如 万能股票代码('sh600001','000003.sz')就会变成sz.000003
    就是这么神奇
    """
    if len(str(原始股票代码)) < 6:
        原始股票代码 = str(原始股票代码).zfill(6)
    需要的点的下标 = 原始股票代码.find('.')
    szsh位置 = max(原始股票代码.find('sz'), 原始股票代码.find('sh'))

    strPattern = '[6|3|0][0-9]{5}'
    result = re.findall(strPattern, 原始股票代码)
    数字代码 = result[0]

    市场 = "sh" if str(数字代码)[:1] == '6' else "sz"
    # print("市场=",市场)
    目标代码替代数字 = re.sub(r'[6|3|0][0-9]{5}', str(数字代码), str(需要的示例))

    目标代码 = re.sub(r'[shz]{2}', 市场, 目标代码替代数字)
    return (目标代码)


def lyydebug(debug, text):
    get_fun_name_cmd_text = "fun_name=str(sys._getframe().f_code.co_name)"
    fun_name = ""
    try:
        eval(get_fun_name_cmd_text)
    except Exception as e:
        print(e)
    out_txt = ("[" + fun_name + "]:" + text)
    print(out_txt)
    return out_txt


def divide_list(lst, n):
    quotient = len(lst) // n
    remainder = len(lst) % n
    result = []
    start = 0
    for i in range(n):
        if i < remainder:
            end = start + quotient + 1
        else:
            end = start + quotient
        result.append(lst[start:end])
        start = end
    return result


def get_time(f):

    def inner(*arg, **kwarg):
        s_time = time.time()
        res = f(*arg, **kwarg)
        e_time = time.time()
        print("\n<" + f.__name__ + "> 耗时：" + str(e_time - s_time))
        return res

    return inner


def 测速(开始时间, 额外说明):
    spend = datetime.now() - 开始时间
    print("\n<-" + 额外说明 + "-> 耗时: {}秒".format(spend))
    return spend


def speed_test(start_time, comment):
    """测试运行时间

    Args:
        start_time (time): 开始时间
        comment (str): 函数名或者其它说明，

    Returns:
        float: 运行时间秒数
    """
    debug = False
    end_time = time.time()
    run_time = end_time - start_time
    print(f"{comment} runtime: {run_time:.2f} seconds")

    rounded_run_time = round(run_time, 2)  # 保留2位小数
    return rounded_run_time


class CustomTimedRotatingFileHandler(TimedRotatingFileHandler):

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def lyyf_logger(log_filename_prefix, message, if_print=False):
    """
    可以每次调用，都会自动创建当天的日志文件，日志文件名为lyylog_前缀_日期.log
    比如lyylog_lyymsg_svc_log_2023-08-24.log
    不再被占用，可以实时删除
    基本完美了
    Args:
        log_filename_prefix (_type_): _description_
        message (_type_): _description_
    """

    if if_print:
        print(message)
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = None

    if handler is None:
        today = datetime.now().strftime("%Y-%m-%d")
        handler = CustomTimedRotatingFileHandler(f'lyylog_{log_filename_prefix}_{today}.log', when='midnight', interval=1, backupCount=7)
        handler.suffix = "%Y-%m-%d"
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s', "%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    with handler:
        logger.info(message)


if __name__ == "__main__":
    pass
