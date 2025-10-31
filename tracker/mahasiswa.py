class Mahasiswa:
    """
    Kelas untuk menyimpan data mahasiswa dan persentase kehadiran.
    """
    def __init__(self, nim, nama):
        self.nim = nim
        self.nama = nama
        self._hadir = 0.0

    @property
    def hadir_persen(self):
        return self._hadir

    @hadir_persen.setter
    def hadir_persen(self, v):
        if v < 0 or v > 100:
            raise ValueError("hadir harus 0–100")
        self._hadir = float(v)

    def info(self):
        return f"{self.nim} - {self.nama} ({self._hadir:.2f}%)"

    def __repr__(self):
        return f"<Mahasiswa {self.nim} {self.nama} hadir={self._hadir:.2f}%>"
