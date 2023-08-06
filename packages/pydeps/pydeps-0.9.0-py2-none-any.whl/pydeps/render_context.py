# -*- coding: utf-8 -*-


from StringIO import StringIO
from contextlib import contextmanager
import textwrap


class RenderContext(object):
    def __init__(self, out=None):
        self.out = out
        self.fp = StringIO()
        self.fillcolor = '#ffffff'
        self.fontcolor = '#000000'

    @contextmanager
    def graph(self, name='G', fillcolor='#ffffff', fontcolor='#000000'):
        self.fillcolor = fillcolor
        self.fontcolor = fontcolor
        self.dedent("""
            digraph G {
                concentrate = true;
                ordering = out;
                ranksep=1.0;
                node [style=filled,fillcolor="%s",fontcolor="%s",fontname=Helvetica,fontsize=10];

        """ % (fillcolor, fontcolor))
        yield
        self.writeln('}')

    def text(self):
        if self.out:
            self.out.close()
        return self.fp.getvalue()

    def write(self, txt):
        self.fp.write(txt)
        if self.out:
            self.out.write(txt)

    def writeln(self, txt):
        self.write(txt + '\n')

    def dedent(self, txt):
        self.write(textwrap.dedent(txt))

    def write_attributes(self, attrs):
        if attrs:
            self.write(' [' + ','.join('%s="%s"' % kv for kv in attrs.items()) + ']')
            # self.write(' [' + ','.join(attrs) + ']')

    def _nodename(self, x):
        "Return a valid node name."
        return x.replace('.', '_')

    def _delattr(self, attr, key, value):
        if attr.get(key) == value:
            del attr[key]

    def write_rule(self, a, b, **attrs):
        "a -> b [a1=x,a2=y];"
        with self.rule():
            self.write('%s -> %s' % (self._nodename(a), self._nodename(b)))
            self._delattr(attrs, 'weight', 1)
            self._delattr(attrs, 'minlen', 0)
            self.write_attributes(attrs)

    def write_node(self, a, **attrs):
        "a [a1=x,a2=y];"
        with self.rule():
            nodename = self._nodename(a)
            self.write(nodename)
            self._delattr(attrs, 'label', nodename)
            self._delattr(attrs, 'fillcolor', self.fillcolor)
            self._delattr(attrs, 'fontcolor', self.fontcolor)
            self.write_attributes(attrs)

    @contextmanager
    def rule(self):
        self.write('    ')
        yield
        self.writeln(';')
