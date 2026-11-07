# Intake — Superapps

| Butir | Isi |
|---|---|
| Proyek | Superapps — Portal layanan publik digital terpadu |
| Jenis proyek | Aplikasi baru — brief meminta portal yang akan dibangun, tanpa surat perubahan, daftar bug, atau sistem berjalan yang disebut; repositori belum berisi kode aplikasi [S1; S2 "modules"] |
| Bahasa dokumen | Bahasa Indonesia |
| Disiapkan | 2026-11-07 |
| Sumber | 2 |
| Fakta | 13 |
| Kesenjangan | 16 |
| Asumsi | 16 |

## Sumber

| # | Sumber | Jenis | Tanggal | Penulis | Catatan |
|---|---|---|---|---|---|
| S1 | "Portal layanan publik digital terpadu (Superapps)" | brief satu baris | tidak diketahui (diterima 2026-11-07) | klien | Satu-satunya masukan klien; dibaca utuh; hasilnya tipis, dilanjutkan ke wawancara. Dikutip sebagai `[S1]` karena tidak punya halaman atau bagian |
| S2 | `.claude/kit.json` | konfigurasi (JSON) | tidak diketahui | tidak diketahui | Dibaca utuh; dikutip per kunci JSON (`[S2 "stack"]`). Berisi stack, modul, branch, wilayah kerja, gerbang CI, lokasi dokumen, forge |

Catatan: permintaan pengguna (`prompt.md`) dikutip sebagai `[request]`. `out.json` dan `err.txt` adalah berkas kosong dari proses uji, bukan sumber.

## Fakta

### Tujuan

- [goal] Klien meminta "Portal layanan publik digital terpadu" dengan nama "Superapps" [S1]
- [goal] Nama proyek di konfigurasi repositori: `superapps` [S2 "project"]

### Aktor

- Kesenjangan G2: pengguna dan hak aksesnya tidak disebut — lihat Kesenjangan

### Fitur

- [feature] Produk berbentuk portal digital untuk layanan publik yang bersifat "terpadu" [S1]

### Aturan bisnis

- Kesenjangan G14: aturan per layanan (persyaratan, lama proses, alur status) tidak disebut — lihat Kesenjangan

### Data

- Kesenjangan G9: data yang dimiliki dan dibagi tidak disebut — lihat Kesenjangan

### Layar dan desain

- Kesenjangan G13: tidak ada desain atau tangkapan layar — lihat Kesenjangan

### Integrasi

- Kesenjangan G4: integrasi dan cara masuk tidak disebut — lihat Kesenjangan

### Batasan

- [constraint] Stack aplikasi: Laravel [S2 "stack"]
- [constraint] Modul aplikasi: `portal` dan `api` [S2 "modules"]
- [constraint] Branch: dasar `staging`, rilis `main`, integrasi `integration-{n}`, branch kerja `sprint-{nn}/{region}/{id}` [S2 "branch"]
- [constraint] Wilayah kerja: `module` (peran `module-dev`, menulis `{module}/**` kecuali `{module}/tests/**`, per modul); `shared` (peran `shared-module-owner`, menulis `database/**`); `tests` (peran `qa-test-engineer`, menulis `*/tests/**`); `tooling` (peran `platform-tooling`, menulis `.claude/**`, `.github/**`) [S2 "regions"]
- [constraint] Gerbang CI: `php artisan test` [S2 "gates"]
- [constraint] Forge: GitHub, proyek `example/superapps` [S2 "forge"]
- [constraint] Lokasi dokumen sprint: backlog `docs/sprints/sprint-{nn}-backlog.md`, laporan `docs/sprints/reports/sprint-{nn}/`, serah terima `docs/sprints/handover.md`, utang kode `docs/sprints/code-debt.md` [S2 "docs"]
- [constraint] Spesifikasi eksternal tidak diwajibkan (`required`: false, tanpa folder Drive) [S2 "external_spec"]

### Non-fungsional

- Kesenjangan G5 dan G15: ketentuan keamanan, data pribadi, dan target non-fungsional tidak disebut — lihat Kesenjangan

### Jadwal

- [timeline] Pengerjaan dimulai Senin, 16 November 2026 [request]

### Anggaran

- Kesenjangan G11: anggaran tidak disebut — lihat Kesenjangan

### Pemangku kepentingan

- [stakeholder] Klien adalah pemberi brief; unit, peran, dan hak keputusannya tidak disebut [request]

## Konflik

Tidak ada: kedua sumber tidak saling bertentangan.

## Kesenjangan

| # | Yang belum ada | Mengapa penting | Status |
|---|---|---|---|
| G1 | Jenis proyek dan makna "terpadu" / "Superapps": aplikasi baru atau perluasan sistem lama, kanal web atau seluler, layanan mana yang dipadukan | Menentukan kerangka SRS dan batas cakupan | Ditanyakan Q1 / ASSUMPTION A-01 |
| G2 | Aktor dan hak aksesnya | SRS 2.2, aturan otorisasi, peran pengguna | Ditanyakan Q2 / ASSUMPTION A-02 |
| G3 | Fitur inti rilis pertama | Kebutuhan fungsional dan isi sprint | Ditanyakan Q3 / ASSUMPTION A-03 |
| G4 | Integrasi eksternal dan cara masuk | SRS 7, risiko jadwal | Ditanyakan Q4 / ASSUMPTION A-04 |
| G5 | Ketentuan hukum, keamanan, dan data pribadi | Kebutuhan non-fungsional dan kepatuhan | Ditanyakan Q5 / ASSUMPTION A-05 |
| G6 | Tenggat | Jumlah sprint | Ditanyakan Q6 / ASSUMPTION A-06 |
| G7 | Tim (peran, orang) | Kapasitas sprint | Ditanyakan Q6 / ASSUMPTION A-07 |
| G8 | Tujuan terukur dan ukuran keberhasilan | Ruang lingkup SRS dan penerimaan | ASSUMPTION A-08 (tidak ditanyakan) |
| G9 | Data yang dimiliki dan dibagi, retensi | Entitas SRS 5.1, kepatuhan data pribadi | ASSUMPTION A-09 (tidak ditanyakan) |
| G10 | Hosting dan lingkungan | Fondasi deploy, keamanan | ASSUMPTION A-10 (tidak ditanyakan) |
| G11 | Anggaran | Batas cakupan | ASSUMPTION A-11 (tidak ditanyakan) |
| G12 | Pemilik penerimaan (yang menyetujui rilis) | Penerimaan UAT dan Sprint Review | ASSUMPTION A-12 (tidak ditanyakan) |
| G13 | Desain layar dan identitas visual | Kebutuhan layar, estimasi frontend | ASSUMPTION A-13 (tidak ditanyakan) |
| G14 | Aturan bisnis per layanan (persyaratan, lama proses, alur status) | SRS 5.2 | ASSUMPTION A-14 (tidak ditanyakan) |
| G15 | Target non-fungsional (kinerja, ketersediaan, aksesibilitas) | SRS 4 dan pertanyaan terbuka | ASSUMPTION A-15 (tidak ditanyakan) |
| G16 | Bahasa antarmuka | Teks layar dan surel | ASSUMPTION A-16 (tidak ditanyakan) |

## Wawancara

### Ronde 1 — 2026-11-07

| # | Pertanyaan | Usulan bawaan | Jawaban |
|---|---|---|---|
| Q1 | Apakah Superapps aplikasi baru atau pengembangan sistem yang sudah ada, dan apa arti "terpadu"? | Aplikasi baru berbasis web (portal responsif untuk peramban desktop dan ponsel, ditambah API). "Terpadu" berarti satu pintu: satu akun warga dan satu katalog semua layanan publik. Layanan yang belum punya aplikasi diajukan daring lewat portal; layanan yang sudah punya aplikasi sendiri cukup ditautkan dari katalog. Aplikasi seluler native di luar rilis pertama | tidak ada jawaban — bawaan diambil |
| Q2 | Siapa penggunanya dan apa hak masing-masing? | Penyelenggara: pemerintah daerah dengan perangkat daerah sebagai unit penyedia layanan; portal dikelola dinas yang membidangi komunikasi dan informatika. Peran: (1) Pengunjung — melihat katalog tanpa akun; (2) Warga — mendaftar, mengajukan dan memantau permohonan; (3) Petugas layanan perangkat daerah — memverifikasi dan memutus permohonan layanan unitnya; (4) Admin perangkat daerah — mengelola layanan unitnya di katalog dan akun petugas unitnya; (5) Super admin pengelola portal — mengelola perangkat daerah, kategori, admin, dan melihat statistik seluruh portal | tidak ada jawaban — bawaan diambil |
| Q3 | Apa fitur inti rilis pertama? | (a) katalog layanan dengan kategori, pencarian, dan detail (persyaratan, alur, lama proses, unit penyedia, tautan bila memakai aplikasi lain); (b) pendaftaran dan masuk warga; (c) pengajuan permohonan daring dengan formulir per layanan dan unggah dokumen persyaratan; (d) pemrosesan oleh petugas: verifikasi, minta perbaikan, setujui atau tolak, unggah dokumen hasil; (e) pelacakan status dan notifikasi (di portal dan surel); (f) pengelolaan katalog, formulir, perangkat daerah, dan pengguna oleh admin; (g) dasbor statistik permohonan. Pengaduan, pembayaran daring, dan survei kepuasan di luar rilis pertama | tidak ada jawaban — bawaan diambil |
| Q4 | Integrasi apa yang dibutuhkan, dan bagaimana pengguna masuk? | Tidak ada integrasi sistem eksternal di rilis pertama. Masuk dengan surel dan kata sandi, dengan verifikasi surel. Notifikasi surel lewat server SMTP milik penyelenggara. Integrasi Dukcapil (NIK), SSO pemerintah, pembayaran, dan pertukaran data dengan aplikasi layanan lain dicatat untuk pengembangan berikutnya | tidak ada jawaban — bawaan diambil |
| Q5 | Ketentuan keamanan, data pribadi, dan regulasi apa yang berlaku? | Tunduk pada Undang-Undang Nomor 27 Tahun 2022 tentang Pelindungan Data Pribadi dan Undang-Undang Nomor 25 Tahun 2009 tentang Pelayanan Publik. Semua akses lewat HTTPS; kata sandi disimpan ter-hash; akses berbasis peran; dokumen permohonan hanya dapat dibuka pemohon, petugas dan admin unit penyedia, serta super admin; jejak audit untuk perubahan status permohonan | tidak ada jawaban — bawaan diambil |
| Q6 | Kapan tenggatnya dan siapa timnya? | Rilis pertama siap UAT dan serah terima dalam 8 minggu: 16 November 2026 – 10 Januari 2027. Tim tiga orang penuh waktu: BE-1 (backend Laravel), FE-1 (frontend portal), OPS (DevOps/CI dan pengujian) | tidak ada jawaban — bawaan diambil |

### Ronde 2

Dilewati: ronde 1 tidak mendapat jawaban (proses non-interaktif), sehingga semua bawaan diambil.

## Asumsi

| # | ASSUMPTION | Dasar | Konfirmasi dengan |
|---|---|---|---|
| A-01 | ASSUMPTION: Superapps adalah aplikasi web baru (portal responsif dan API). "Terpadu" berarti satu akun warga dan satu katalog semua layanan; layanan tanpa aplikasi diajukan daring di portal, layanan dengan aplikasi sendiri ditautkan dari katalog; aplikasi seluler native di luar rilis pertama | Bawaan Q1, tidak ada jawaban — bawaan diambil | Klien / pemilik produk |
| A-02 | ASSUMPTION: Penyelenggara pemerintah daerah; peran Pengunjung, Warga, Petugas layanan, Admin perangkat daerah, Super admin dengan hak seperti pada Q2 | Bawaan Q2, tidak ada jawaban — bawaan diambil | Klien / pemilik produk |
| A-03 | ASSUMPTION: Fitur rilis pertama (a)–(g) seperti pada Q3; pengaduan, pembayaran daring, dan survei kepuasan di luar rilis pertama | Bawaan Q3, tidak ada jawaban — bawaan diambil | Klien / pemilik produk |
| A-04 | ASSUMPTION: Tanpa integrasi eksternal di rilis pertama; masuk dengan surel dan kata sandi dengan verifikasi surel; surel lewat SMTP penyelenggara | Bawaan Q4, tidak ada jawaban — bawaan diambil | Pengelola TI penyelenggara |
| A-05 | ASSUMPTION: Berlaku UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi dan UU No. 25 Tahun 2009 tentang Pelayanan Publik; HTTPS, kata sandi ter-hash, akses berbasis peran, dokumen privat, jejak audit perubahan status | Bawaan Q5, tidak ada jawaban — bawaan diambil | Bagian hukum dan pengelola TI penyelenggara |
| A-06 | ASSUMPTION: Rilis pertama siap UAT dan serah terima dalam 8 minggu, 16 November 2026 – 10 Januari 2027 | Bawaan Q6, tidak ada jawaban — bawaan diambil | Klien / pemilik produk |
| A-07 | ASSUMPTION: Tim tiga orang penuh waktu: BE-1 (backend Laravel), FE-1 (frontend portal), OPS (DevOps/CI dan pengujian) | Bawaan Q6, tidak ada jawaban — bawaan diambil | Manajer proyek pengembang |
| A-08 | ASSUMPTION: Ukuran keberhasilan: jumlah layanan yang tersedia daring dan persentase permohonan selesai dalam lama proses yang ditetapkan; angka target ditetapkan pemilik produk | Tidak ditanyakan; usulan bawaan untuk kesenjangan G8 | Pemilik produk |
| A-09 | ASSUMPTION: Data rilis pertama: akun (nama, surel, nomor telepon), perangkat daerah, kategori, layanan, formulir, permohonan, dokumen, riwayat status, notifikasi, jejak audit; dimiliki penyelenggara; NIK tidak dikumpulkan; masa retensi perlu dikonfirmasi | Tidak ditanyakan; usulan bawaan untuk kesenjangan G9 | Pengelola data penyelenggara |
| A-10 | ASSUMPTION: Hosting di server milik penyelenggara dengan lingkungan staging (dari branch `staging`) dan produksi (dari branch `main`) | Tidak ditanyakan; usulan bawaan untuk kesenjangan G10 | Pengelola TI penyelenggara |
| A-11 | ASSUMPTION: Anggaran tidak dibahas di dokumen ini; cakupan dibatasi oleh kapasitas tim A-07 dan tenggat A-06 | Tidak ditanyakan; usulan bawaan untuk kesenjangan G11 | Klien |
| A-12 | ASSUMPTION: Kepala unit pengelola portal (dinas yang membidangi komunikasi dan informatika) menyetujui hasil UAT dan rilis | Tidak ditanyakan; usulan bawaan untuk kesenjangan G12 | Klien |
| A-13 | ASSUMPTION: Belum ada desain; tim membuat tampilan responsif sederhana mengikuti identitas visual yang akan diberikan penyelenggara | Tidak ditanyakan; usulan bawaan untuk kesenjangan G13 | Pemilik produk |
| A-14 | ASSUMPTION: Persyaratan dan lama proses tiap layanan diisi admin perangkat daerah; alur status umum Diajukan → Diverifikasi → Perlu perbaikan → Disetujui / Ditolak → Selesai | Tidak ditanyakan; usulan bawaan untuk kesenjangan G14 | Admin perangkat daerah |
| A-15 | ASSUMPTION: Target kinerja, ketersediaan, dan aksesibilitas belum ditetapkan; ditetapkan bersama pemilik produk sebelum UAT | Tidak ditanyakan; usulan bawaan untuk kesenjangan G15 | Pemilik produk |
| A-16 | ASSUMPTION: Antarmuka dan surel hanya dalam Bahasa Indonesia | Tidak ditanyakan; usulan bawaan untuk kesenjangan G16 | Pemilik produk |

## Sumber yang tidak terbaca

- Tidak ada.

Langkah berikutnya: Lanewright SRS mengubah berkas ini menjadi dokumen kebutuhan.
