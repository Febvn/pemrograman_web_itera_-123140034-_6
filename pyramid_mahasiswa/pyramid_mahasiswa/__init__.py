"""Application factory for the Pyramid Mahasiswa service."""

from pyramid.config import Configurator


def main(global_config, **settings):
    """Create and configure the Pyramid WSGI application."""
    with Configurator(settings=settings) as config:
        # Enable templating, database models, and application routes.
        config.include('pyramid_jinja2')
        config.add_jinja2_search_path('pyramid_mahasiswa:templates')
        config.include('.models')
        config.include('.routes')
        config.scan()  # Autodiscover view/configuration decorators.
    return config.make_wsgi_app()
