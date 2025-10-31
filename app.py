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
    return input("Pilih menu: ")

def tampilkan(records):
    if not records:
        print("Belum ada data.")
        return
    print("\n--- Rekap Nilai ---")
    print(f"{'NIM':<12} {'Nama':<15} {'Hadir%':>7} {'Nilai':>7} {'Predikat':>9}")
    print("-" * 52)
    for r in records:
        print(f"{r['nim']:<12} {r['nama']:<15} {r['hadir']:>6.1f} {r['akhir']:>8.2f} {r['predikat']:>9}")
    print("-" * 52)

def main():
    rekap = RekapKelas()

    while True:
        pilihan = menu()

        if pilihan == "1":
            nim = input("Masukkan NIM: ")
            nama = input("Masukkan nama: ")
            mhs = Mahasiswa(nim, nama)
            rekap.tambah_mahasiswa(mhs)
            print(f"Mahasiswa {nama} ditambahkan.")

        elif pilihan == "2":
            nim = input("Masukkan NIM: ")
            try:
                persen = float(input("Masukkan persentase kehadiran (0-100): "))
                rekap.set_hadir(nim, persen)
                print("Presensi berhasil diperbarui.")
            except Exception as e:
                print("Error:", e)

        elif pilihan == "3":
            nim = input("Masukkan NIM: ")
            try:
                quiz = float(input("Nilai Quiz: "))
                tugas = float(input("Nilai Tugas: "))
                uts = float(input("Nilai UTS: "))
                uas = float(input("Nilai UAS: "))
                rekap.set_penilaian(nim, quiz, tugas, uts, uas)
                print("Nilai berhasil disimpan.")
            except Exception as e:
                print("Error:", e)

        elif pilihan == "4":
            tampilkan(rekap.rekap())

        elif pilihan == "5":
            semua = rekap.rekap()
            rendah = [r for r in semua if r["akhir"] < 70]
            print("\nMahasiswa dengan nilai < 70:")
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
            print("Terima kasih, program selesai.")
            break

        else:
            print("Pilihan tidak valid.")

if __name__ == "__main__":
    main()
