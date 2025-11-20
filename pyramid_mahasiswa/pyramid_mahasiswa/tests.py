"""Unit tests untuk memastikan API Matakuliah bekerja sesuai ekspektasi."""

import unittest
import transaction

from pyramid import testing
from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.response import Response


def dummy_request(dbsession, **kwargs):
    """Factory helper untuk membuat DummyRequest dengan dbsession terpasang."""
    request = testing.DummyRequest(dbsession=dbsession, **kwargs)
    request.response = Response()
    return request


class BaseTest(unittest.TestCase):
    """Menyiapkan database in-memory untuk setiap test case."""

    def setUp(self):
        self.config = testing.setUp(settings={
            'sqlalchemy.url': 'sqlite:///:memory:'
        })
        self.config.include('.models')
        settings = self.config.get_settings()

        from .models import (
            get_engine,
            get_session_factory,
            get_tm_session,
            )

        self.engine = get_engine(settings)
        session_factory = get_session_factory(self.engine)

        self.session = get_tm_session(session_factory, transaction.manager)

    def init_database(self):
        """Buat seluruh tabel berdasarkan metadata model."""
        from .models.meta import Base
        Base.metadata.create_all(self.engine)

    def tearDown(self):
        from .models.meta import Base

        testing.tearDown()
        transaction.abort()
        Base.metadata.drop_all(self.engine)


class TestMatakuliahAPI(BaseTest):
    """Kumpulan test untuk seluruh endpoint CRUD."""

    def setUp(self):
        super().setUp()
        self.init_database()

    def _create_sample(self):
        """Helper untuk menyimpan satu record ke database."""
        from .models import Matakuliah
        instance = Matakuliah(
            kode_mk='IF101',
            nama_mk='Algoritma',
            sks=3,
            semester=1,
        )
        self.session.add(instance)
        self.session.flush()
        return instance

    def test_list_matakuliah(self):
        self._create_sample()
        from .views.default import list_matakuliah

        request = dummy_request(self.session)
        response = list_matakuliah(request)

        self.assertEqual(response['total'], 1)
        self.assertEqual(response['matakuliahs'][0]['kode_mk'], 'IF101')

    def test_create_matakuliah(self):
        from .views.default import create_matakuliah

        request = dummy_request(self.session)
        request.json_body = {
            'kode_mk': 'IF102',
            'nama_mk': 'Struktur Data',
            'sks': 3,
            'semester': 2,
        }

        response = create_matakuliah(request)

        self.assertEqual(request.response.status, '201 Created')
        self.assertEqual(response['kode_mk'], 'IF102')

    def test_get_invalid_id_raises(self):
        from .views.default import get_matakuliah

        request = dummy_request(self.session, matchdict={'id': '999'})

        with self.assertRaises(HTTPNotFound):
            get_matakuliah(request)

    def test_update_matakuliah(self):
        instance = self._create_sample()
        from .views.default import update_matakuliah

        request = dummy_request(self.session, matchdict={'id': str(instance.id)})
        request.json_body = {
            'kode_mk': 'IF101',
            'nama_mk': 'Algoritma Pemrograman',
            'sks': 4,
            'semester': 2,
        }

        response = update_matakuliah(request)

        self.assertEqual(response['nama_mk'], 'Algoritma Pemrograman')
        self.assertEqual(response['sks'], 4)
        self.assertEqual(response['semester'], 2)

    def test_delete_matakuliah(self):
        instance = self._create_sample()
        from .views.default import delete_matakuliah
        from .models import Matakuliah

        request = dummy_request(self.session, matchdict={'id': str(instance.id)})
        result = delete_matakuliah(request)

        self.assertIn('berhasil', result['message'])
        self.assertIsNone(self.session.get(Matakuliah, instance.id))

    def test_validate_payload(self):
        from .views.default import create_matakuliah

        request = dummy_request(self.session)
        request.json_body = {
            'kode_mk': 'IF103',
            # Missing nama_mk
            'sks': 3,
            'semester': 3,
        }

        with self.assertRaises(HTTPBadRequest):
            create_matakuliah(request)
