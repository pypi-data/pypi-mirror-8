===================================
lribeiro.cherrypy.templating.genshi
===================================

Genshi renderer for ``lribeiro.cherrypy.templating``

It has three optional config entries:

- templating.genshi.template_directories: can be a path to the templates directory, list of paths, or anything ``genshi.template.TemplateLoader`` accepts. If none is given, ``{root module directory}/templates`` is used as the template diretory.

- templating.genshi.loader_options: ``dict`` containing additional arguments passed to the TemplateLoader constructor

- templating.genshi.render_options: ``dict`` containing arguments used when rendering the template, for example, {'method': 'html', 'doctype': 'html-transitional'}

You can also pass arguments to the render via ``@template`` decorator args and kwargs.

.. sourcecode:: python

    class Controller:
        @cherrypy.expose
        @template('template_name.html', method='xhtml', doctype='xhtml11')
        def handler(self):
            pass

When setting the template name, remember that **Genshi interprets a leading slash as an absolute path**! So the following would probably raise a TemplateNotFound:

.. sourcecode:: python

    class WrongController:
        @cherrypy.expose
        # pay attention to the leading slash
        # Genshi will look for a 'wrong_template_name.html' file on the root of the filesystem
        @template('/wrong_template_name.html')
        def wrong_handler(self):
            pass

Developed under Python3.4 and tested against Python2.7, Python3.4 and pypy.

Usage:
------

.. sourcecode:: python

    import cherrypy

    from lribeiro.cherrypy.templating import template
    from lribeiro.cherrypy.templating.genshi import renderer


    class Root(object):
        @cherrypy.expose
        @template('index.html')
        def index(self):
            return {'context': 'variables'}

        @cherrypy.expose
        @template('/var/templates/page.html')  # absolute path
        def page(self):
            return {'context': 'variables'}


    config = {
        '/': {
            'templating.renderer': renderer,
            'templating.genshi.template_directories': [
                'templates',  # relative to the module where the root class was declared
                '/var/templates'  # absolute path
            ],
            'templating.genshi.loader_options': {'default_encoding': 'utf-8'},  # this is optional
            'templating.genshi.render_options': {'method': 'html', 'doctype': 'html5'}  # this is also optional
        }
    }

    if __name__ == '__main__':
        cherrypy.quickstart(Root(), '/', config)