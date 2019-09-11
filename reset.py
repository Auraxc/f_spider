import pymysql

import config


def reset():
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password=config.db_pwd,
        db=config.db_name,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )


    sql_create = """
    CREATE TABLE `fanfou` (
        `id`          INT NOT NULL AUTO_INCREMENT,
        `content`     VARCHAR(255) NOT NULL,
        `time`        VARCHAR(255) NOT NULL,
        `device`      VARCHAR(255) NOT NULL,
        `link`        VARCHAR(255) NOT NULL,
        `pic`         VARCHAR(255) NULL,
        `pic_link`    VARCHAR(255) NULL,
        PRIMARY KEY (`id`)
    );
    """

    with connection.cursor() as cursor:
        cursor.execute('DROP DATABASE IF EXISTS`fanfou`')
        cursor.execute('CREATE DATABASE `fanfou` CHARACTER SET utf8mb4')
        cursor.execute('USE `fanfou`')

        cursor.execute(sql_create)

    connection.commit()
    connection.close()


if __name__ == '__main__':
    reset()