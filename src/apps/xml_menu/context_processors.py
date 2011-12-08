"""
author:Kovalenko Pavel (ice.tegliaf@gmail.com)
"""
from apps.xml_menu.reader import Menu


def cp_xml_menu(request):
    menu = Menu()
    menu.load_from_xml()
    menu.select(request.path)
    
    num = 1
    for m in menu.root_item:
        m.num = u'%s' % num
        if num == 1:
            m.margin_left_px = 0
        elif num == 2:
            m.margin_left_px = 95
        elif num == 3:
            m.margin_left_px = 175
        elif num == 4:
            m.margin_left_px = 380
        elif num == 5:
            m.margin_left_px = 470
        elif num == 6:
            m.margin_left_px = 440
        elif num == 7:
            m.margin_left_px = 510
        else:
            m.margin_left_px = 0
        
        num = num + 1
    
    return {
        'cp_xml_menu': menu.root_item,
    }