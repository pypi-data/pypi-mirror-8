============================
lribeiro.cherrypy.templating
============================

Template rendering tool for cherrypy.

**It does not render any template**, so you must provide a renderer for your template system to do the actual rendering.

The renderer must be a callable accepting two arguments:

- The name of the template to be rendered
- A context object, which can be a ``dict`` or any other object that your template system can handle

The template name comes from the ``@template`` decorator argument and the context is the value return from the handler.

Usage:
------

.. sourcecode:: python

    from os import path

    import cherrypy
    import pystache

    from lribeiro.cherrypy.templating import template


    def _renderer(template_name, context):
        """
        Template renderer using Pystache
        """

        search_dir = path.join(path.dirname(path.abspath(__file__)), 'templates')
        renderer = pystache.Renderer(file_extension='html', search_dirs=search_dir)

        template_str = renderer.load_template(template_name)
        return renderer.render(template_str, context)


    class Root:
        @cherrypy.expose
        @template('index')
        def index(self):
            return {'name': 'Lorem', 'lastname': 'Ipsum'}

        @cherrypy.expose
        @template('page')
        def page(self):
            return {'name': 'Lorem', 'lastname': 'Ipsum'}


    config = {
        '/': {
            'templating.renderer': _renderer,
        }
    }

    if __name__ == '__main__':
        cherrypy.quickstart(Root(), '/', config)