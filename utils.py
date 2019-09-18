import time


def log(*args, **kwargs):
    format = '%H:%M:%S'
    value = time.localtime(int(time.time()))
    dt = time.strftime(format, value)
    print(dt, *args, **kwargs)
    with open('fanfou.log', 'a', encoding='utf-8') as f:
        print(dt, *args, file=f, **kwargs)
