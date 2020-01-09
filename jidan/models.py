# -*- coding: utf-8 -*-

from jidan.base.model import BaseModel


class Quotes(BaseModel):
    __table__ = "quotes"

    def __repr__(self):
        return "<table %s>" % self.__table__
