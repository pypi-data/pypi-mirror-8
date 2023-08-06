# -*- coding: utf-8 -*-
import os
from datetime import datetime

import wsgi
from config import cfg
from util import obj_from_str, cached_function

def render_to_string(rq, template, context=None):
    context = context or {}
    if not isinstance(context, dict):
        return unicode(context)
    for k, v in rq.context.iteritems():
        if k not in context:
            context[k] = v
    return _env().get_template(template).render(context or {})

def render(rq, to, context=None, **response_kwargs):
    if to == 'json':
        data = _json_dumps()(context)
        if 'callback' in rq.GET:
            data = '%s(%s)' % (rq.GET['callback'], data)  # jsonp
            content_type = 'application/x-javascript'
        else:
            content_type = 'application/json'
    elif to == 'text':
        data = unicode(context)
        content_type = 'text/plain'
    elif to == 'html':
        data = unicode(context)
        content_type = 'text/html'
    else:
        data = render_to_string(rq, to, context)
        content_type = 'text/html'
    if 'content_type' not in response_kwargs:
        response_kwargs['content_type'] = content_type
    return wsgi.Response(data, **response_kwargs)

@cached_function
def _json_dumps():
    import asjson
    return lambda obj: asjson.dumps(obj, debug=cfg.DEBUG)


@cached_function
def _env():
    import jinja2
    import pysi

    env = jinja2.Environment(
        loader = jinja2.FunctionLoader(obj_from_str(cfg.TEMPLATE_LOADER)),
        autoescape = True,
        cache_size = cfg.TEMPLATE_CACHE_SIZE,
        auto_reload = cfg.TEMPLATE_AUTO_RELOAD,
        extensions = cfg.JINJA2_EXTENSIONS,
    )
    env.globals = cfg.JINJA2_GLOBALS or {
            'url4': pysi.url4,
            'cfg': pysi.cfg,
            'static_url': pysi.static_url,

            'xrange': xrange,
            'enumerate': enumerate,
            'len': len,
    }
    return env

class FileLoader(object):
    mtimes = {}

    def load(self, path):
        try:
            f = open('templates/%s' % path)
        except IOError:
            try:
                app_name, path = path.split('/', 1)
                f = open('%s/templates/%s' % (app_name, path))
            except (IOError, ValueError):
                assert 0, 'template not found: %s' % path

        path = os.path.normpath(os.path.join(os.getcwd(), f.name))
        self.mtimes[path] = os.path.getmtime(path)
        source = f.read().decode('utf-8')
        source = '\n'.join(line.lstrip() for line in source.splitlines())
        return (source, path,
                lambda: self.mtimes[path] == os.path.getmtime(path))
file_loader = FileLoader().load
