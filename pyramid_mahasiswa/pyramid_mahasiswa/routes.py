"""Route configuration for the Pyramid Mahasiswa application."""


def includeme(config):
    """Register static assets and CRUD endpoints."""
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/', request_method='GET')

    # REST-style endpoints for the Matakuliah resource.
    config.add_route('list_matakuliah', '/api/matakuliah', request_method='GET')
    config.add_route('create_matakuliah', '/api/matakuliah', request_method='POST')
    config.add_route(
        'get_matakuliah',
        '/api/matakuliah/{id}',
        request_method='GET',
    )
    config.add_route(
        'update_matakuliah',
        '/api/matakuliah/{id}',
        request_method='PUT',
    )
    config.add_route(
        'delete_matakuliah',
        '/api/matakuliah/{id}',
        request_method='DELETE',
    )
