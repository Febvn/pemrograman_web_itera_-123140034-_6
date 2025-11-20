# Pyramid Mahasiswa – API Matakuliah

![Python](https://img.shields.io/badge/python-3.13-blue.svg)
![Pyramid](https://img.shields.io/badge/pyramid-2.x-orange.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)

## Deskripsi Proyek
API web berbasis Pyramid untuk mengelola data matakuliah. Aplikasi ini menyediakan operasi CRUD lengkap dengan validasi payload, error handling eksplisit, serta halaman dokumentasi HTML sederhana pada route utama (`/`). Skema data menggunakan SQLAlchemy ORM dan migrasi dijalankan melalui Alembic.

## Cara Instalasi

### 1. Membuat Virtual Environment
```bash
cd pyramid_mahasiswa
python -m venv venv
venv\Scripts\activate     # Windows
# atau
source venv/bin/activate  # macOS/Linux
```

### 2. Instalasi Dependensi
```bash
python -m pip install --upgrade pip setuptools
pip install -e ".[testing]"
```

### 3. Konfigurasi Database
Secara default `development.ini` menggunakan SQLite (`sqlite:///pyramid_mahasiswa.sqlite`). Untuk mengganti database, ubah nilai berikut:
```ini
sqlalchemy.url = postgresql+psycopg2://user:pass@localhost:5432/pyramid_mahasiswa
```

## Cara Menjalankan

### 1. Menjalankan Migrasi
```bash
alembic -c development.ini upgrade head
initialize_pyramid_mahasiswa_db development.ini  # opsi untuk seed data contoh
```

### 2. Menjalankan Server
```bash
pserve development.ini --reload
```
Server aktif di `http://localhost:6543`. Halaman utama menampilkan dokumentasi singkat beserta daftar endpoint.

## API Endpoints
Seluruh response berbentuk JSON. Contoh payload di bawah diasumsikan server berjalan pada `http://localhost:6543`.

### 1. GET /api/matakuliah — daftar semua matakuliah
```bash
curl http://localhost:6543/api/matakuliah
```
Respons:
```json
{
  "total": 2,
  "matakuliahs": [
    {
      "id": 1,
      "kode_mk": "IF101",
      "nama_mk": "Algoritma",
      "sks": 3,
      "semester": 1
    },
    {
      "id": 2,
      "kode_mk": "IF201",
      "nama_mk": "Struktur Data",
      "sks": 3,
      "semester": 3
    }
  ]
}
```

### 2. GET /api/matakuliah/{id} — detail matakuliah tertentu
```bash
curl http://localhost:6543/api/matakuliah/1
```
```json
{
  "id": 1,
  "kode_mk": "IF101",
  "nama_mk": "Algoritma",
  "sks": 3,
  "semester": 1
}
```

### 3. POST /api/matakuliah — membuat matakuliah baru
```bash
curl -X POST http://localhost:6543/api/matakuliah \
  -H "Content-Type: application/json" \
  -d '{
    "kode_mk": "IF301",
    "nama_mk": "Basis Data",
    "sks": 4,
    "semester": 4
  }'
```
Respons `201 Created`:
```json
{
  "id": 3,
  "kode_mk": "IF301",
  "nama_mk": "Basis Data",
  "sks": 4,
  "semester": 4
}
```

### 4. PUT /api/matakuliah/{id} — memperbarui data
```bash
curl -X PUT http://localhost:6543/api/matakuliah/1 \
  -H "Content-Type: application/json" \
  -d '{
    "kode_mk": "IF101",
    "nama_mk": "Algoritma Pemrograman",
    "sks": 4,
    "semester": 2
  }'
```
```json
{
  "id": 1,
  "kode_mk": "IF101",
  "nama_mk": "Algoritma Pemrograman",
  "sks": 4,
  "semester": 2
}
```

### 5. DELETE /api/matakuliah/{id} — menghapus data
```bash
curl -X DELETE http://localhost:6543/api/matakuliah/1
```
```json
{
  "message": "Matakuliah IF101 berhasil dihapus"
}
```

## Testing

### 1. Unit Test Otomatis
```bash
pytest pyramid_mahasiswa/tests.py -v
```

### 2. Pengujian Manual via cURL
Jalankan kelima perintah pada bagian API Endpoints untuk mengecek:
- List data (`GET /api/matakuliah`)
- Detail (`GET /api/matakuliah/{id}`)
- Create (`POST /api/matakuliah`)
- Update (`PUT /api/matakuliah/{id}`)
- Delete (`DELETE /api/matakuliah/{id}`)

## Demo

Tampilan dokumentasi HTML bawaan saat membuka `http://localhost:6543/`:

![Demo halaman utama](static/demo.png)
![Demo daftar endpoint](static/demo1.png)

