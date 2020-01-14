# -*- coding: utf-8 -*-

# -*- coding: utf-8 -*-
from sqlalchemy import create_engine

def gen_db_uri():
    DB_USERNAME = 'hnb'  # 数据库用户名
    DB_PASSWORD = 'alyHnb2015'  # 数据库密码
    DB_HOST = '172.16.10.251'  # 主机名
    DB_PORT = 3306  # 端口号 mysql 默认的是3306
    DB_NAME = 'jidan'  # 数据库的名字
    DB_URI = 'mysql+pymysql://%s:%s@%s:%s/%s?charset=utf8' % (DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME)
    return DB_URI

if __name__ == "__main__":
    DB_URI=gen_db_uri()
    engine = create_engine(DB_URI)
    with engine.connect() as con:
        rs = con.execute("show tables")
        print(rs.fetchone())


