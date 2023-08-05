=================================
lribeiro.cherrypy.templating.mako
=================================

Mako renderer for ``lribeiro.cherrypy.templating``

It has two optional config entries:

- templating.mako.template_directories: can be a path to the templates directory, absolute (with leading slash) or
relative to the root module location, or a list of paths. If none is given, ``{root directory}/templates`` is used.

- templating.mako.config: any additional arguments to be passed to the TemplateLookup constructor

Developed under Python3.4 and tested against Python2.7, Python3.4 and pypy.

Usage:
------

.. sourcecode:: python

    import cherrypy

    from lribeiro.cherrypy.templating import template
    from lribeiro.cherrypy.templating.mako import renderer


    class Root(object):
        @cherrypy.expose
        @template('index.html')
        def index(self):
            return {'context': 'variables'}

        @cherrypy.expose
        @template('/page.html')
        def page(self):
            return {'context': 'variables'}


    config = {
        '/': {
            'templating.renderer': renderer,
            'templating.mako.template_directories': 'mako_templates',  # optional
            'templating.mako.config': {'module_directory': '/tmp/modules'}  # also optional
        }
    }

    if __name__ == '__main__':
        cherrypy.quickstart(Root(), '/', config)

