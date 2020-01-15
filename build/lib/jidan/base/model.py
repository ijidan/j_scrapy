# -*- coding: utf-8 -*-

from jidan.settings import DB_USERNAME, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME
from orator import DatabaseManager, Model

config = {
    'mysql': {
        'driver': 'mysql',
        'host': DB_HOST,
        'database': DB_NAME,
        'user': DB_USERNAME,
        'password': DB_PASSWORD,
        'prefix': ''
    }
}
db = DatabaseManager(config)
Model.set_connection_resolver(db)


# 基础Model类
class BaseModel(Model):
    __timestamps__ = False
