"""View layer yang meng-handle halaman utama dan API Matakuliah."""

from pyramid.httpexceptions import HTTPBadRequest, HTTPNotFound
from pyramid.view import view_config

from sqlalchemy.exc import DBAPIError, IntegrityError

from .. import models


def _parse_json_body(request):
    """Validasi body JSON dan kembalikan payload siap pakai."""
    try:
        data = request.json_body
    except ValueError as exc:
        raise HTTPBadRequest(f'Payload harus berupa JSON valid: {exc}') from exc

    required_fields = {'kode_mk', 'nama_mk', 'sks', 'semester'}
    missing = required_fields - data.keys()
    if missing:
        raise HTTPBadRequest(
            f'Field berikut wajib diisi: {", ".join(sorted(missing))}'
        )

    try:
        sks = int(data['sks'])
        semester = int(data['semester'])
    except (TypeError, ValueError) as exc:
        raise HTTPBadRequest('Field sks dan semester harus berupa integer') from exc

    payload = {
        'kode_mk': str(data['kode_mk']).strip(),
        'nama_mk': str(data['nama_mk']).strip(),
        'sks': sks,
        'semester': semester,
    }

    if not payload['kode_mk'] or not payload['nama_mk']:
        raise HTTPBadRequest('kode_mk dan nama_mk tidak boleh kosong')

    return payload


def _get_matakuliah_or_404(request):
    """Ambil objek Matakuliah berdasarkan id atau lempar 404."""
    try:
        mk_id = int(request.matchdict.get('id', ''))
    except (TypeError, ValueError) as exc:
        raise HTTPBadRequest('Parameter id harus berupa integer') from exc

    instance = request.dbsession.get(models.Matakuliah, mk_id)
    if instance is None:
        raise HTTPNotFound(f'Matakuliah dengan id {mk_id} tidak ditemukan')
    return instance


@view_config(route_name='home', renderer='home.jinja2', request_method='GET')
def home(request):
    """Render dokumentasi HTML sederhana di halaman root."""
    return {}


@view_config(
    route_name='list_matakuliah',
    renderer='json',
    request_method='GET',
)
def list_matakuliah(request):
    """Tampilkan seluruh data matakuliah dalam format list JSON."""
    try:
        records = request.dbsession.query(models.Matakuliah).all()
    except DBAPIError as exc:
        raise HTTPBadRequest(f'Gagal mengambil data: {exc}') from exc

    return {
        'matakuliahs': [record.to_dict() for record in records],
        'total': len(records),
    }


@view_config(
    route_name='get_matakuliah',
    renderer='json',
    request_method='GET',
)
def get_matakuliah(request):
    """Tampilkan detail satu matakuliah berdasarkan id."""
    return _get_matakuliah_or_404(request).to_dict()


@view_config(
    route_name='create_matakuliah',
    renderer='json',
    request_method='POST',
)
def create_matakuliah(request):
    """Buat record matakuliah baru setelah payload lolos validasi."""
    payload = _parse_json_body(request)
    instance = models.Matakuliah(**payload)
    request.dbsession.add(instance)

    try:
        request.dbsession.flush()  # Pastikan INSERT dipush agar id tersedia.
    except IntegrityError as exc:
        request.dbsession.rollback()
        raise HTTPBadRequest(
            'kode_mk harus unik, data yang Anda kirimkan sudah ada'
        ) from exc

    request.response.status = '201 Created'
    return instance.to_dict()


@view_config(
    route_name='update_matakuliah',
    renderer='json',
    request_method='PUT',
)
def update_matakuliah(request):
    """Perbarui data matakuliah existing."""
    instance = _get_matakuliah_or_404(request)
    payload = _parse_json_body(request)

    for key, value in payload.items():
        setattr(instance, key, value)

    try:
        request.dbsession.flush()
    except IntegrityError as exc:
        request.dbsession.rollback()
        raise HTTPBadRequest(
            'kode_mk harus unik, data yang Anda kirimkan sudah ada'
        ) from exc

    return instance.to_dict()


@view_config(
    route_name='delete_matakuliah',
    renderer='json',
    request_method='DELETE',
)
def delete_matakuliah(request):
    """Hapus data matakuliah dan kembalikan pesan konfirmasi."""
    instance = _get_matakuliah_or_404(request)
    request.dbsession.delete(instance)
    request.dbsession.flush()  # Commit perubahan delete sebelum respon.
    return {'message': f'Matakuliah {instance.kode_mk} berhasil dihapus'}
