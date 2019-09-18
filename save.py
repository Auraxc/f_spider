import pymysql
from utils import log
import config


def _pymysql_connection():
    """
    连接数据库
    :return:
    """
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=config.db_pwd,
        db='fanfou',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
    return connection


def SQLsave(fanfou):
    """
    保存
    """
    connection = _pymysql_connection()
    try:
        sql_keys = []
        sql_values = []
        for k in fanfou.keys():
            sql_keys.append('`{}`'.format(k))
            sql_values.append('%s')
        formatted_sql_keys = ', '.join(sql_keys)
        formatted_sql_values = ', '.join(sql_values)

        sql_insert = 'INSERT INTO `{}` ({}) VALUES ({});'.format(
            'fanfou', formatted_sql_keys, formatted_sql_values
        )
        log('保存消息', fanfou, formatted_sql_keys, formatted_sql_values)
        values = tuple(fanfou.values())
        with connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            # 避免和内置函数 id 重名，所以用 _id
            _id = cursor.lastrowid
        connection.commit()
    finally:
        connection.close()

    # 先 commit，再关闭链接，再返回
    return _id


