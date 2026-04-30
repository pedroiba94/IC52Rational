# -*- coding: utf-8 -*-
def classFactory(iface):
    from .ic52ic_racional import IC52ICRacionalPlugin
    return IC52ICRacionalPlugin(iface)
