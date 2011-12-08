# coding: utf-8
#
#Generated file by Revelator - (Kovalenko Pavel ice.tegliaf@gmail.com)
#
from apps.data_utils    import randomize
from models             import *
import datetime

def handle():

    print u"\nGenerate Log:",
    for i in range(100):
        try:
            Log(
                date = randomize.datetime(),
                type = randomize.integer(),
                subject = randomize.string(255),
                content = randomize.text(),
                ).save()
            randomize.out('.')
        except:
            randomize.out('*')


