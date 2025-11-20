"""Helper untuk pshell agar session dan models otomatis tersedia."""

from . import models


def setup(env):
    """Siapkan variabel bantu yang bisa diakses saat menjalankan `pshell`."""
    request = env['request']

    # Mulai transaksi manual agar operasi di shell bisa commit/rollback.
    request.tm.begin()

    # Inject objek penting agar bisa langsung digunakan di interpreter.
    env['tm'] = request.tm
    env['dbsession'] = request.dbsession
    env['models'] = models
