"""Database models for the Matakuliah entity."""

from sqlalchemy import (
    Column,
    Integer,
    Text,
)

from .meta import Base


class Matakuliah(Base):
    """Represent satu baris data matakuliah pada tabel `matakuliah`."""

    __tablename__ = 'matakuliah'

    # Primary key dan kolom bisnis yang relevan.
    id = Column(Integer, primary_key=True)
    kode_mk = Column(Text, unique=True, nullable=False)
    nama_mk = Column(Text, nullable=False)
    sks = Column(Integer, nullable=False)
    semester = Column(Integer, nullable=False)

    def to_dict(self):
        """Serialize instance menjadi dict agar mudah di-render sebagai JSON."""
        return {
            'id': self.id,
            'kode_mk': self.kode_mk,
            'nama_mk': self.nama_mk,
            'sks': self.sks,
            'semester': self.semester,
        }

    def __repr__(self):
        """Representasi string yang memudahkan proses debugging."""
        return (
            f"<Matakuliah id={self.id} kode_mk={self.kode_mk!r} "
            f"nama_mk={self.nama_mk!r} sks={self.sks} semester={self.semester}>"
        )
