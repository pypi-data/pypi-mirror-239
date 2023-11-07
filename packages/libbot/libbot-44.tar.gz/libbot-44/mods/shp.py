# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0612


"shops"


import time


from bot.disk   import sync
from bot.object import Object
from bot.find   import find, fntime, laps


class Shop(Object):

    def __init__(self):
        super().__init__()
        self.txt = ''

    def size(self):
        return len(self.__dict__)

    def length(self):
        return len(self.__dict__)


def got(event):
    if not event.args:
        return
    selector = {'txt': event.args[0]}
    for fnm, obj in find('shop', selector):
        obj.__deleted__ = True
        sync(obj)
        event.reply('ok')


def shp(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('shop'):
            lap = laps(time.time()-fntime(obj.__oid__))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no shops")
        return
    obj = Shop()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')
