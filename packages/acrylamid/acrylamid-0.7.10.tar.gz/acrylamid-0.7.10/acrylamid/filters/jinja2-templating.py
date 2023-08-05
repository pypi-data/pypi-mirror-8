# -*- encoding: utf-8 -*-
#
# Copyright 2012 Martin Zimmermann <info@posativ.org>. All rights reserved.
# License: BSD Style, 2 clauses -- see LICENSE.

import io
import re
from os.path import join, isfile

from acrylamid import log
from acrylamid.filters import Filter
from acrylamid.helpers import system as defaultsystem
from acrylamid.errors import AcrylamidException

from jinja2 import Environment, TemplateError


class Jinja2(Filter):
    """Jinja2 filter that pre-processes in Markdown/reStructuredText
    written posts. XXX: and offers some jinja2 extensions."""

    match = ['Jinja2', 'jinja2']
    version = 1

    priority = 90.0

    def init(self, conf, env, *args):

        def system(cmd, stdin=None):
            try:
                return defaultsystem(cmd, stdin, shell=True).strip()
            except (OSError, AcrylamidException) as e:
                log.warn('%s: %s' % (e.__class__.__name__, e.args[0]))
                return e.args[0]

        self.conf = conf
        self.env = env

        # jinja2 is stupid and can't import any module
        import time, datetime, urllib

        if hasattr(env.engine, 'jinja2'):
            self.jinja2_env = env.engine.jinja2.overlay(cache_size=0)
        else:
            self.jinja2_env = Environment(cache_size=0)

        self.jinja2_env.filters['system'] = system
        self.jinja2_env.filters['split'] = unicode.split
        self.jinja2_env.filters.update({
            'time': time, 'datetime': datetime, 'urllib': urllib,
            })

        for module in (time, datetime, urllib):
            for name in dir(module):
                if name.startswith('_'):
                    continue

                self.jinja2_env.filters[module.__name__ + '.' + name] = getattr(module, name)

    @property
    def macros(self):
        """Import macros from ``THEME/macro.html`` into context of the
        post environment.  Very hackish, but it should work."""

        path = join(self.conf['theme'], 'macros.html')
        if not (isfile(path) and hasattr(self.env.engine, 'jinja2')):
            return ''

        with io.open(path, encoding='utf-8') as fp:
            text = fp.read()

        return "{%% from 'macros.html' import %s with context %%}\n" % ', '.join(
            re.findall('^\{% macro ([^\(]+)', text, re.MULTILINE))

    def transform(self, content, entry):

        try:
            tt = self.jinja2_env.from_string(self.macros + content)
            return tt.render(conf=self.conf, env=self.env, entry=entry)
        except (TemplateError, AcrylamidException) as e:
            log.warn('%s: %s in %r' % (e.__class__.__name__, e.args[0], entry.filename))
            return content
