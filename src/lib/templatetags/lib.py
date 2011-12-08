# coding: utf-8
from django import template
from django.template.defaultfilters import stringfilter
import string
import sys

register = template.Library()

@register.inclusion_tag('menu.html')
def include_menu(menu, menu_id, request):
    return {
        'menu_id': menu_id,
        'menu': menu,
        'request': request,
    }

@register.simple_tag
def trans_class_vn_plural(cls):
    parts = string.split(force_unicode(cls._meta.verbose_name_plural))
    parts[0] = string.capitalize(parts[0])
    return ' '.join(parts)

    
@register.simple_tag
def trans_class_vn(cls):
    parts = string.split(force_unicode(cls._meta.verbose_name))
    parts[0] = string.capitalize(parts[0])
    return ' '.join(parts)

    
@register.simple_tag
def class_raw_vn_name(cls):
    return cls._meta.verbose_name_raw


@register.filter
@stringfilter
def strip(value):
    return value.strip()
    

@register.simple_tag
def trans_app_name(app_name):
    app_name = app_name.lower()
    if app_name == 'auth':
        return u'Пользователи'
    elif app_name == 'comments':
        return u'Комментарии'
    else:
        try:
            app = sys.modules[app_name]
            return app.app_label.capitalize()
        except:
            try:
                app = sys.modules["apps.%s" % app_name]
                return app.app_label.capitalize()
            except:
                return app_name.capitalize()
                
  
@register.inclusion_tag('sidebox.html', takes_context=True)
def include_sidebox(context, objects, title, link_text, no):
    try:
        index_url = reverse("%s_index" % objects)
    except:
        index_url = reverse(objects)
    return {
        'objects': context["cp_%s" % objects],
        'title': title,
        'index_url': index_url,
        'link_text': link_text,
        'no': no,
    }      

@register.tag
def columnize(parser, token):
    """
        Put stuff into columns. Can also define class tags for rows and cells

        Usage: {% columnize num_cols [row_class[,row_class2...]|'' [cell_class[,cell_class2]]] %}

        num_cols:   the number of columns to format.
        row_class:  can use a comma (no spaces, please) separated list that cycles 
                    (utilizing the cycle code) can also put in '' for nothing,
                    if you want no row_class, but want a cell_class.
        cell_class: same format as row_class, but the cells only loop within a row.  
                    Every row resets the cell counter.

        Typical usage:

        <table border="0" cellspacing="5" cellpadding="5">
        {% for o in some_list %}
        	{% columnize 3 %}
        	<a href="{{ o.get_absolute_url }}">{{ o.name }}</a>
        	{% endcolumnize %}
        {% endfor %}
        </table>
    """
    nodelist = parser.parse(('endcolumnize',))
    parser.delete_first_token()

    #Get the number of columns, default 1
    columns = 1
    row_class = ''
    cell_class = ''
    args = token.contents.split(None, 3)
    num_args = len(args)
    if num_args >= 2:
        #{% columnize columns %}
        if args[1].isdigit():
            columns = int(args[1])
        else:
            raise template.TemplateSyntaxError('The number of columns must be a number. "%s" is not a number.') % args[2]
    if num_args >= 3:
        #{% columnize columns row_class %}
        if "," in args[2]:
            #{% columnize columns row1,row2,row3 %}
            row_class = [v for v in args[2].split(",") if v]    # split and kill blanks
        else:
            row_class = [args[2]]
            if row_class == "''":
                # Allow the designer to pass an empty string (two quotes) to skip the row_class and 
                #   only have a cell_class
                row_class = []
    if num_args == 4:
        #{% columnize columns row_class cell_class %}
        if "," in args[3]:
            #{% columnize row_class cell1,cell2,cell3 %}
            cell_class = [v for v in args[3].split(",") if v]    # split and kill blanks
        else:
            cell_class = [args[3]]
            if cell_class == "''":
                # This shouldn't be necessary, but might as well test for it
                cell_class = []

    return ColumnizeNode(nodelist, columns, row_class, cell_class)

class ColumnizeNode(template.Node):
    def __init__(self, nodelist, columns = 1, row_class = '', cell_class = ''):
        self.nodelist = nodelist
        self.columns = int(columns)
        self.counter = 0
        self.rowcounter = -1
        self.cellcounter = -1
        self.row_class_len = len(row_class)
        self.row_class = row_class
        self.cell_class_len = len(cell_class)
        self.cell_class = cell_class

    def render(self, context):
        output = ''
        self.counter += 1
        if (self.counter > self.columns):
            self.counter = 1
            self.cellcounter = -1

        if (self.counter == 1):
            output = '<tr'
            if self.row_class:
                self.rowcounter += 1
                output += ' class="%s">' % self.row_class[self.rowcounter % self.row_class_len]
            else:
                output += '>'

        output += '<td'
        if self.cell_class:
            self.cellcounter += 1
            output += ' class="%s">' % self.cell_class[self.cellcounter % self.cell_class_len]
        else:
            output += '>'

        output += self.nodelist.render(context) + '</td>'

        forloop = context['forloop']
        if self.counter == self.columns or forloop['last'] and forloop['counter0'] % self.columns != (self.columns - 1):
            if (self.columns < self.counter):
              for i in range(0,self.columns-self.counter):
                output += '<td>&nbsp;</td>'
            output += '</tr>'

        return output
