import sys
PY3 = sys.version_info[0] >= 3

try:
    from itertools import zip_longest  # Python 3
except ImportError:
    from itertools import izip_longest as zip_longest  # Python 2
from collections import Mapping

class TableCell(object):
    bg_colour = None
    
    def __init__(self, value, header=False, bg_colour=None, text_colour=None):
        self.value = value
        self.header = header
        self.bg_colour = bg_colour
        self.text_colour = text_colour
    
    def _make_css(self):
        rules = []
        if self.bg_colour:
            rules.append('background-color:%s' % self.bg_colour)
        if self.text_colour:
            rules.append('color:%s' % self.text_colour)
        return '; '.join(rules)
    
    def _repr_html_(self):
        tag = 'th' if self.header else 'td'
        attrs = []
        style = self._make_css()
        if style:
            attrs.append('style="%s"'%style)
        return "<%s %s>%s</%s>"% (tag, ' '.join(attrs), self.value, tag)

    def _repr_latex_(self):
        return (str if PY3 else unicode)(self.value)
    
class TableRow(object):
    def  __init__(self, *cells):
        self.parent = None
        self.cells = []
        for c in cells:
            self.append_cell(c)

    def set_parent(self, parent):
        self.parent = parent
            
    def append_cell(self, c):
        if not isinstance(c, TableCell):
            c = TableCell(c)
        self.cells.append(c)

    def column_count(self):
        return len(self.cells)
    
    def _repr_html_(self):
        return '<tr>' + ''.join(c._repr_html_() for c in self.cells) + '</tr>'

    def _repr_latex_(self):
        return ' & '.join(c._repr_latex_() for c in self.cells) + '\\\\\n'

class TableHeaderRow(TableRow):
    def append_cell(self, c):
        if not isinstance(c, TableCell):
            c = TableCell(c, header=True)
        self.cells.append(c)

    def set_parent(self, parent):
        super(TableHeaderRow, self).set_parent(parent)
        self.parent.has_header = True

    def _repr_latex_(self):
        return super(TableHeaderRow, self)._repr_latex_() + '\\hline\n'

class Table(object):
    def __init__(self, *rows):
        self.rows = []
        self.has_header = False

        # if argument is a single dict, convert it to a table with keys
        # as header
        if (len(rows) == 1) and isinstance(rows[0], Mapping):
            dict_arg = rows[0]
            new_rows = [TableHeaderRow(*dict_arg.keys())]
            new_rows.extend(zip_longest(*dict_arg.values(), fillvalue=''))
            rows = new_rows

        for r in rows:
            self.append_row(r)
    
    def append_row(self, r):
        if not isinstance(r, TableRow):
            r = TableRow(*r)
        r.set_parent(self)
        self.rows.append(r)
    
    def _repr_html_(self):
        return '<table>\n' + '\n'.join(r._repr_html_() for r in self.rows) + '\n</table>'

    def _repr_latex_(self):
        out = '\n'.join(r._repr_latex_() for r in self.rows)
        if self.has_header:
            out = '\\hline\n' + out + '\\hline\n'
        return '\\begin{tabular}{*{%d}{l}}\n%s\\end{tabular}' % \
                        (max(row.column_count() for row in self.rows), out)

