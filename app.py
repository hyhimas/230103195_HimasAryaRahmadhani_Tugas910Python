from tracker import Mahasiswa, RekapKelas, build_markdown_report, build_html_report, save_text

def menu():
    print("\n=== Student Performance Tracker ===")
    print("1) Tambah mahasiswa")
    print("2) Ubah presensi")
    print("3) Ubah nilai")
    print("4) Lihat rekap")
    print("5) Filter nilai < 70")
    print("6) Simpan laporan Markdown")
    print("7) Simpan laporan HTML")
    print("8) Keluar")
    print("9) Muat ulang data dari CSV")
    return input("Pilih menu: ")

def tampilkan(records):
    """Menampilkan data rekap ke terminal."""
    if not records:
        print("Belum ada data.")
        return
    print("\n--- Rekap Nilai ---")
    print(f"{'NIM':<12} {'Nama':<15} {'Hadir%':>7} {'Nilai':>8} {'Predikat':>9}")
    print("-" * 56)
    for r in records:
        print(f"{r['nim']:<12} {r['nama']:<15} {r['hadir']:>6.1f} {r['akhir']:>8.2f} {r['predikat']:>9}")
    print("-" * 56)

def main():
    rekap = RekapKelas()  # otomatis load CSV saat start

    while True:
        pilihan = menu().strip()

        if pilihan == "1":
            nim = input("Masukkan NIM: ").strip()
            nama = input("Masukkan nama: ").strip()
            mhs = Mahasiswa(nim, nama)
            rekap.tambah_mahasiswa(mhs)
            print(f"Mahasiswa {nama} ditambahkan dan data disimpan ke CSV.")

        elif pilihan == "2":
            nim = input("Masukkan NIM: ").strip()
            try:
                persen = float(input("Masukkan persentase kehadiran (0-100): "))
                rekap.set_hadir(nim, persen)
                print("Presensi berhasil diperbarui dan disimpan ke CSV.")
            except Exception as e:
                print("Error:", e)

        elif pilihan == "3":
            nim = input("Masukkan NIM: ").strip()
            try:
                quiz = float(input("Nilai Quiz: "))
                tugas = float(input("Nilai Tugas: "))
                uts = float(input("Nilai UTS: "))
                uas = float(input("Nilai UAS: "))
                rekap.set_penilaian(nim, quiz, tugas, uts, uas)
                print("Nilai berhasil disimpan ke CSV.")
            except Exception as e:
                print("Error:", e)

        elif pilihan == "4":
            data = rekap.rekap()
            tampilkan(data)

        elif pilihan == "5":
            # ✅ perbaikan filter
            data = rekap.rekap()
            if not data:
                print("Belum ada data untuk difilter.")
            else:
                rendah = [r for r in data if float(r.get("akhir", 0)) < 70]
                if not rendah:
                    print("Tidak ada mahasiswa dengan nilai akhir di bawah 70.")
                else:
                    print("\nMahasiswa dengan nilai akhir < 70:")
                    tampilkan(rendah)

        elif pilihan == "6":
            records = rekap.rekap()
            if not records:
                print("Tidak ada data untuk disimpan.")
            else:
                content = build_markdown_report(records)
                save_text("out/report.md", content)
                print("Laporan Markdown berhasil disimpan ke out/report.md")

        elif pilihan == "7":
            records = rekap.rekap()
            if not records:
                print("Tidak ada data untuk disimpan.")
            else:
                html = build_html_report(records)
                save_text("out/report.html", html)
                print("Laporan HTML berhasil disimpan ke out/report.html")

        elif pilihan == "8":
            print("Terima kasih, program selesai. Semua data sudah tersimpan di folder data/.")
            break

        elif pilihan == "9":
            # ✅ fitur muat ulang data CSV
            try:
                rekap.load_data()
                print("Data berhasil dimuat ulang dari file CSV.")
            except Exception as e:
                print("Gagal memuat data dari CSV:", e)

        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
