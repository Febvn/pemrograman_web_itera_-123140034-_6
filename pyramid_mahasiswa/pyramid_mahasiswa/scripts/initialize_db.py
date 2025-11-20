"""Script utilitas untuk menginisialisasi database dengan data contoh."""

import argparse
import sys

from pyramid.paster import bootstrap, setup_logging
from sqlalchemy.exc import OperationalError

from .. import models


def setup_models(dbsession):
    """Tambahkan data seed hanya jika tabel masih kosong."""
    if dbsession.query(models.Matakuliah).count():
        return

    # Contoh data awal untuk membantu proses demo/manual testing.
    seeds = [
        {
            'kode_mk': 'IF101',
            'nama_mk': 'Algoritma dan Pemrograman',
            'sks': 3,
            'semester': 1,
        },
        {
            'kode_mk': 'IF201',
            'nama_mk': 'Struktur Data',
            'sks': 3,
            'semester': 3,
        },
        {
            'kode_mk': 'IF301',
            'nama_mk': 'Basis Data',
            'sks': 4,
            'semester': 4,
        },
    ]

    for seed in seeds:
        dbsession.add(models.Matakuliah(**seed))


def parse_args(argv):
    """Parse config URI dari argumen CLI."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'config_uri',
        help='Configuration file, e.g., development.ini',
    )
    return parser.parse_args(argv[1:])


def main(argv=sys.argv):
    """Bootstrap Pyramid dan jalankan proses seeding."""
    args = parse_args(argv)
    setup_logging(args.config_uri)
    env = bootstrap(args.config_uri)

    try:
        with env['request'].tm:
            dbsession = env['request'].dbsession
            setup_models(dbsession)
    except OperationalError:
        print('''
Pyramid is having a problem using your SQL database.  The problem
might be caused by one of the following things:

1.  You may need to initialize your database tables with `alembic`.
    Check your README.txt for description and try to run it.

2.  Your database server may not be running.  Check that the
    database server referred to by the "sqlalchemy.url" setting in
    your "development.ini" file is running.
            ''')
