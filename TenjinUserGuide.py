import tenjin

from tenjin.helpers import *

context = {
    'title': 'Tenjin Example',
    'items': ['<AAA>', 'B&B', '"CCC"', 1, 2, 4, 000 ,67 ,7,8, 9],
    'viewName': '大肯将'
}

engine = tenjin.Engine(path=['template'])

html = engine.render('BaseView.ts.py', context)
print(html)