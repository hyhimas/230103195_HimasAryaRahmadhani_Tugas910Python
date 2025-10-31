import csv
import os
from tracker.penilaian import Penilaian
from tracker.mahasiswa import Mahasiswa

class RekapKelas:
    """
    Manajer rekap nilai seluruh mahasiswa.
    Termasuk penyimpanan dan pembacaan data dari CSV.
    """
    def __init__(self, data_dir="data"):
        self._by_nim = {}
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.load_data()  # otomatis muat data saat mulai

    # --------------------
    # Operasi utama
    # --------------------
    def tambah_mahasiswa(self, mhs):
        if mhs.nim in self._by_nim:
            print("NIM sudah terdaftar.")
            return
        self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}
        self.save_data()

    def set_hadir(self, nim, persen):
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError("NIM tidak ditemukan")
        item['mhs'].hadir_persen = persen
        self.save_data()

    def set_penilaian(self, nim, quiz=None, tugas=None, uts=None, uas=None):
        item = self._by_nim.get(nim)
        if not item:
            raise KeyError("NIM tidak ditemukan")
        p = item['nilai']
        if quiz is not None: p.quiz = quiz
        if tugas is not None: p.tugas = tugas
        if uts is not None: p.uts = uts
        if uas is not None: p.uas = uas
        self.save_data()

    # --------------------
    # Perhitungan dan rekap
    # --------------------
    def predikat(self, skor):
        if skor >= 85: return "A"
        if skor >= 75: return "B"
        if skor >= 65: return "C"
        if skor >= 50: return "D"
        return "E"

    def rekap(self):
        rows = []
        for nim, d in self._by_nim.items():
            m = d['mhs']
            p = d['nilai']
            akhir = p.nilai_akhir()
            rows.append({
                'nim': nim,
                'nama': m.nama,
                'hadir': m.hadir_persen,
                'akhir': akhir,
                'predikat': self.predikat(akhir),
            })
        return rows

    
    def save_data(self):
        """Menyimpan data ke dua file CSV: attendance.csv dan grades.csv"""
        att_path = os.path.join(self.data_dir, "attendance.csv")
        grd_path = os.path.join(self.data_dir, "grades.csv")

        # simpan presensi
        with open(att_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nim", "nama", "hadir"])
            for nim, d in self._by_nim.items():
                m = d['mhs']
                writer.writerow([m.nim, m.nama, m.hadir_persen])

        # simpan nilai
        with open(grd_path, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nim", "quiz", "tugas", "uts", "uas"])
            for nim, d in self._by_nim.items():
                p = d['nilai']
                writer.writerow([nim, p.quiz, p.tugas, p.uts, p.uas])

    def load_data(self):
        """Membaca data dari attendance.csv dan grades.csv jika ada"""
        att_path = os.path.join(self.data_dir, "attendance.csv")
        grd_path = os.path.join(self.data_dir, "grades.csv")

        if not os.path.exists(att_path) or not os.path.exists(grd_path):
            return  # belum ada file

        # baca mahasiswa
        with open(att_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                mhs = Mahasiswa(row["nim"], row["nama"])
                mhs.hadir_persen = float(row["hadir"])
                self._by_nim[mhs.nim] = {'mhs': mhs, 'nilai': Penilaian()}

        # baca nilai
        with open(grd_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nim = row["nim"]
                if nim in self._by_nim:
                    p = self._by_nim[nim]['nilai']
                    p.quiz = float(row["quiz"])
                    p.tugas = float(row["tugas"])
                    p.uts = float(row["uts"])
                    p.uas = float(row["uas"])
