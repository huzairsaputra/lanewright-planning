# Spesifikasi Kebutuhan Perangkat Lunak — Superapps

| Butir | Isi |
|---|---|
| Dokumen | Spesifikasi Kebutuhan Perangkat Lunak (SKPL / SRS) |
| Versi | 0.1 (draf) |
| Tanggal | 2026-11-07 |
| Dasar | docs/requirements/intake.md (2 sumber) |
| Status | Draf untuk ditinjau |

## 1 Pendahuluan

### 1.1 Tujuan

Dokumen ini menetapkan kebutuhan rilis pertama Superapps, portal layanan publik digital terpadu, untuk klien, pemilik produk, dan tim pengembang. Klien hanya memberi satu baris brief [S1]. Karena itu, sebagian besar kebutuhan di sini bersandar pada asumsi berlabel (A-01–A-16) yang harus dikonfirmasi; lihat 2.4 dan 8.

### 1.2 Ruang lingkup

Superapps adalah portal web yang memadukan layanan publik dalam satu pintu [S1]. Warga menemukan semua layanan di satu katalog, mengajukan permohonan secara daring, dan memantau statusnya. Petugas perangkat daerah memproses permohonan, dan admin mengelola katalog serta pengguna (ASSUMPTION A-01, A-02, A-03). Aplikasi dibangun dengan Laravel dalam modul `portal` dan `api` [S2 "stack"; S2 "modules"].

| Dalam cakupan | Di luar cakupan |
|---|---|
| Katalog layanan terpadu, pencarian, dan detail layanan | Aplikasi seluler native (A-01) |
| Tautan ke aplikasi layanan yang sudah ada | Pertukaran data dengan aplikasi layanan lain (A-01, A-04) |
| Pendaftaran, verifikasi surel, masuk, dan profil warga | Integrasi Dukcapil (NIK), SSO pemerintah (A-04) |
| Pengajuan permohonan daring dengan unggah dokumen | Pembayaran daring (A-03, A-04) |
| Pemrosesan permohonan oleh petugas dan dokumen hasil | Pengaduan masyarakat (A-03) |
| Pelacakan status dan notifikasi (portal dan surel) | Survei kepuasan masyarakat (A-03) |
| Pengelolaan layanan, formulir, perangkat daerah, kategori, dan pengguna | Antarmuka dalam bahasa selain Bahasa Indonesia (A-16) |
| Dasbor statistik permohonan | |

### 1.3 Definisi dan singkatan

| Istilah | Arti |
|---|---|
| Superapps | Nama kerja portal layanan publik digital terpadu [S1] |
| Perangkat daerah | Unit pemerintah daerah yang menyediakan layanan (A-02) |
| Layanan "Ajukan di portal" | Layanan yang permohonannya diajukan dan diproses di Superapps |
| Layanan "Aplikasi lain" | Layanan yang sudah punya aplikasi sendiri; katalog hanya menautkannya |
| Permohonan | Pengajuan layanan oleh warga beserta isian formulir dan dokumen |
| PDP | Pelindungan Data Pribadi (UU No. 27 Tahun 2022) |
| SMTP | Protokol pengiriman surel |
| CI | Continuous integration; gerbang tes otomatis sebelum penggabungan kode |
| UAT | User acceptance testing; uji penerimaan oleh pengguna |

### 1.4 Referensi

| # | Sumber | Jenis | Tanggal |
|---|---|---|---|
| S1 | "Portal layanan publik digital terpadu (Superapps)" | brief satu baris | tidak diketahui (diterima 2026-11-07) |
| S2 | `.claude/kit.json` | konfigurasi (JSON) | tidak diketahui |

Permintaan pengguna dikutip sebagai `[request]` (tanggal mulai 16 November 2026).

## 2 Gambaran umum

### 2.1 Konteks produk

Superapps adalah aplikasi baru [S1]. Pengguna mengaksesnya lewat peramban desktop dan ponsel (A-01). Modul `portal` menyajikan antarmuka dan modul `api` menyajikan layanan data [S2 "modules"]. Layanan yang sudah punya aplikasi sendiri tetap berjalan di aplikasinya dan hanya ditautkan dari katalog (A-01). Satu-satunya sistem luar di rilis pertama adalah server surel (SMTP) penyelenggara untuk notifikasi (A-04).

### 2.2 Aktor dan kelas pengguna

| Aktor | Deskripsi | Kebutuhan utama |
|---|---|---|
| Pengunjung | Siapa pun tanpa akun (A-02) | Menemukan layanan dan persyaratannya |
| Warga | Pemohon layanan yang punya akun terverifikasi (A-02) | Mengajukan permohonan, memperbaikinya, memantau status, menerima hasil |
| Petugas layanan | Pegawai perangkat daerah penyedia layanan (A-02) | Memverifikasi dan memutus permohonan layanan unitnya |
| Admin perangkat daerah | Pengelola layanan satu perangkat daerah (A-02) | Mengelola layanan, formulir, persyaratan, dan petugas unitnya |
| Super admin | Pengelola portal di dinas yang membidangi komunikasi dan informatika (A-02) | Mengelola perangkat daerah, kategori, pengguna; melihat statistik seluruh portal |

### 2.3 Batasan

- Stack aplikasi: Laravel [S2 "stack"]
- Modul aplikasi: `portal` dan `api` [S2 "modules"]
- Branch: dasar `staging`, rilis `main`, integrasi `integration-{n}`, branch kerja `sprint-{nn}/{region}/{id}` [S2 "branch"]
- Wilayah kerja: `module` (`{module}/**` kecuali `{module}/tests/**`), `shared` (`database/**`), `tests` (`*/tests/**`), `tooling` (`.claude/**`, `.github/**`) [S2 "regions"]
- Gerbang CI: `php artisan test` [S2 "gates"]
- Forge: GitHub, proyek `example/superapps` [S2 "forge"]

### 2.4 Asumsi

- A-01 ASSUMPTION: Superapps adalah aplikasi web baru (portal responsif dan API). "Terpadu" berarti satu akun warga dan satu katalog semua layanan; layanan tanpa aplikasi diajukan daring di portal, layanan dengan aplikasi sendiri ditautkan; aplikasi seluler native di luar rilis pertama — konfirmasi dengan klien / pemilik produk
- A-02 ASSUMPTION: Penyelenggara pemerintah daerah; peran Pengunjung, Warga, Petugas layanan, Admin perangkat daerah, Super admin — konfirmasi dengan klien / pemilik produk
- A-03 ASSUMPTION: Fitur rilis pertama: katalog, akun warga, pengajuan, pemrosesan, pelacakan dan notifikasi, administrasi, dasbor; pengaduan, pembayaran daring, dan survei kepuasan di luar rilis pertama — konfirmasi dengan klien / pemilik produk
- A-04 ASSUMPTION: Tanpa integrasi eksternal di rilis pertama; masuk dengan surel dan kata sandi dengan verifikasi surel; surel lewat SMTP penyelenggara — konfirmasi dengan pengelola TI penyelenggara
- A-05 ASSUMPTION: Berlaku UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi dan UU No. 25 Tahun 2009 tentang Pelayanan Publik; HTTPS, kata sandi ter-hash, akses berbasis peran, dokumen privat, jejak audit perubahan status — konfirmasi dengan bagian hukum dan pengelola TI penyelenggara
- A-06 ASSUMPTION: Rilis pertama siap UAT dan serah terima dalam 8 minggu, 16 November 2026 – 10 Januari 2027 — konfirmasi dengan klien / pemilik produk
- A-07 ASSUMPTION: Tim tiga orang penuh waktu: BE-1, FE-1, OPS — konfirmasi dengan manajer proyek pengembang
- A-08 ASSUMPTION: Ukuran keberhasilan: jumlah layanan daring dan persentase permohonan selesai dalam lama proses; angka target dari pemilik produk — konfirmasi dengan pemilik produk
- A-09 ASSUMPTION: Data rilis pertama seperti 5.1; dimiliki penyelenggara; NIK tidak dikumpulkan; retensi perlu dikonfirmasi — konfirmasi dengan pengelola data penyelenggara
- A-10 ASSUMPTION: Hosting di server penyelenggara; staging dari branch `staging`, produksi dari branch `main` — konfirmasi dengan pengelola TI penyelenggara
- A-11 ASSUMPTION: Anggaran tidak dibahas; cakupan dibatasi kapasitas tim dan tenggat — konfirmasi dengan klien
- A-12 ASSUMPTION: Kepala unit pengelola portal menyetujui hasil UAT dan rilis — konfirmasi dengan klien
- A-13 ASSUMPTION: Belum ada desain; tampilan responsif sederhana mengikuti identitas visual penyelenggara — konfirmasi dengan pemilik produk
- A-14 ASSUMPTION: Persyaratan dan lama proses diisi admin perangkat daerah; alur status Diajukan → Diverifikasi → Perlu perbaikan → Disetujui / Ditolak → Selesai — konfirmasi dengan admin perangkat daerah
- A-15 ASSUMPTION: Target kinerja, ketersediaan, dan aksesibilitas ditetapkan bersama pemilik produk sebelum UAT — konfirmasi dengan pemilik produk
- A-16 ASSUMPTION: Antarmuka dan surel hanya dalam Bahasa Indonesia — konfirmasi dengan pemilik produk

## 3 Kebutuhan fungsional

### 3.1 Katalog layanan

#### F-01 Katalog layanan terpadu

- **Kebutuhan:** Sistem harus menampilkan katalog seluruh layanan publik berstatus aktif dari semua perangkat daerah dalam satu halaman portal, dikelompokkan per kategori.
- **Aktor:** Pengunjung, Warga
- **Prioritas:** Must (alur inti dari brief; detail mengikuti A-01, A-03)
- **Kriteria penerimaan:**
  - AC1: Diberikan 3 layanan aktif di 2 kategori dari 2 perangkat daerah, ketika pengunjung tanpa akun membuka katalog, maka ketiga layanan tampil di bawah kategorinya masing-masing beserta nama perangkat daerah penyedianya.
  - AC2: Diberikan satu layanan nonaktif, ketika katalog dibuka, maka layanan itu tidak tampil.
  - AC3: Setiap kartu layanan menampilkan nama layanan, kategori, perangkat daerah, dan jenis layanan ("Ajukan di portal" atau "Aplikasi lain").
- **Sumber:** [S1]; ASSUMPTION A-01, A-03

#### F-02 Pencarian dan filter layanan

- **Kebutuhan:** Sistem harus memungkinkan pengguna mencari layanan dengan kata kunci dan memfilternya menurut kategori dan perangkat daerah.
- **Aktor:** Pengunjung, Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan layanan "Izin Keramaian" dan "Kartu Identitas Anak", ketika pengguna mencari "izin", maka hanya "Izin Keramaian" yang tampil.
  - AC2: Ketika filter kategori X dipilih, maka hanya layanan berkategori X yang tampil.
  - AC3: Ketika tidak ada layanan yang cocok, maka tampil pesan "Layanan tidak ditemukan" dan nol hasil.
- **Sumber:** ASSUMPTION A-03

#### F-03 Detail layanan

- **Kebutuhan:** Sistem harus menampilkan halaman detail tiap layanan berisi deskripsi, dokumen persyaratan, alur, lama proses, dan perangkat daerah penyedia.
- **Aktor:** Pengunjung, Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan layanan dengan 2 dokumen persyaratan dan lama proses "5 hari kerja" yang diisi admin, ketika detail dibuka, maka kedua persyaratan dan teks "5 hari kerja" tampil.
  - AC2: Diberikan layanan "Ajukan di portal", ketika pengunjung tanpa akun menekan "Ajukan Permohonan", maka ia diarahkan ke halaman masuk dan setelah masuk kembali ke formulir layanan itu.
- **Sumber:** ASSUMPTION A-03, A-14

#### F-04 Tautan ke aplikasi layanan lain

- **Kebutuhan:** Sistem harus menampilkan tautan ke aplikasi luar untuk layanan berjenis "Aplikasi lain", tanpa formulir pengajuan di portal.
- **Aktor:** Pengunjung, Warga, Admin perangkat daerah
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan layanan "Aplikasi lain" dengan URL, ketika detail dibuka, maka tombol "Buka Aplikasi Layanan" membuka URL itu di tab baru dan tombol "Ajukan Permohonan" tidak tampil.
  - AC2: Ketika admin menyimpan layanan "Aplikasi lain" tanpa URL `https://` yang valid, maka penyimpanan ditolak dengan pesan galat.
- **Sumber:** [S1] ("terpadu"); ASSUMPTION A-01

### 3.2 Akun warga

#### F-05 Pendaftaran akun warga

- **Kebutuhan:** Sistem harus memungkinkan warga mendaftar dengan nama, surel, nomor telepon, dan kata sandi, disertai persetujuan pemrosesan data pribadi dan verifikasi surel.
- **Aktor:** Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan isian valid dan persetujuan dicentang, ketika formulir dikirim, maka akun terbentuk berstatus "belum terverifikasi" dan surel verifikasi terkirim ke alamat itu.
  - AC2: Ketika persetujuan tidak dicentang, maka pendaftaran ditolak dengan pesan.
  - AC3: Ketika surel sudah terdaftar, maka pendaftaran ditolak dengan pesan "Surel sudah terdaftar".
  - AC4: Ketika warga membuka tautan verifikasi dari surelnya, maka status akun menjadi "terverifikasi".
- **Sumber:** ASSUMPTION A-03, A-04, A-05

#### F-06 Masuk, keluar, dan atur ulang kata sandi

- **Kebutuhan:** Sistem harus memungkinkan pengguna masuk dengan surel dan kata sandi, keluar, dan mengatur ulang kata sandi lewat tautan surel.
- **Aktor:** Warga, Petugas layanan, Admin perangkat daerah, Super admin
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Ketika kredensial benar, maka pengguna masuk dan diarahkan ke halaman awal perannya (warga: Permohonan Saya; petugas: antrean; admin: kelola layanan; super admin: kelola perangkat daerah).
  - AC2: Ketika kata sandi salah, maka tampil "Surel atau kata sandi salah" tanpa menyebut bagian mana yang salah.
  - AC3: Setelah warga mengatur kata sandi baru lewat tautan surel, kata sandi lama ditolak dan yang baru diterima.
  - AC4: Setelah keluar, membuka halaman yang dilindungi mengarahkan ke halaman masuk.
- **Sumber:** ASSUMPTION A-03, A-04

#### F-07 Profil warga

- **Kebutuhan:** Sistem harus memungkinkan warga melihat dan mengubah nama dan nomor telepon di profilnya.
- **Aktor:** Warga
- **Prioritas:** Could
- **Kriteria penerimaan:**
  - AC1: Ketika warga mengubah nomor telepon dan menyimpan, maka nilai baru tampil saat profil dibuka ulang.
  - AC2: Kolom surel di profil hanya-baca.
- **Sumber:** ASSUMPTION A-09

### 3.3 Permohonan layanan

#### F-08 Pengajuan permohonan daring

- **Kebutuhan:** Sistem harus memungkinkan warga terverifikasi mengajukan permohonan untuk layanan "Ajukan di portal" dengan mengisi formulir layanan dan mengunggah dokumen persyaratan, lalu memberi nomor permohonan yang unik.
- **Aktor:** Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan formulir dengan 2 isian wajib dan 1 dokumen wajib, ketika semuanya diisi, diunggah, dan dikirim, maka permohonan berstatus "Diajukan", nomor uniknya tampil, dan permohonan muncul di "Permohonan Saya".
  - AC2: Ketika isian atau dokumen wajib belum lengkap, maka permohonan tidak dapat dikirim dan pesan menyebut butir yang kurang.
  - AC3: Ketika berkas berjenis di luar daftar yang diizinkan layanan, maka unggahan ditolak dengan pesan berisi jenis yang diizinkan.
  - AC4: Ketika akun belum terverifikasi, maka pengajuan ditolak dengan ajakan memverifikasi surel.
- **Sumber:** ASSUMPTION A-03, A-14

#### F-09 Perbaikan permohonan

- **Kebutuhan:** Sistem harus memungkinkan warga memperbaiki isian dan dokumen permohonan berstatus "Perlu perbaikan" lalu mengirimkannya kembali.
- **Aktor:** Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan permohonan "Perlu perbaikan", warga melihat alasan dari petugas; setelah mengubah dan mengirim ulang, status kembali "Diajukan" dan riwayat mencatatnya.
  - AC2: Diberikan permohonan berstatus lain, tombol ubah tidak tampil dan perubahan lewat API ditolak.
- **Sumber:** ASSUMPTION A-03, A-14

#### F-10 Pelacakan status permohonan

- **Kebutuhan:** Sistem harus menampilkan kepada warga daftar permohonannya beserta status terkini dan riwayat perubahan status.
- **Aktor:** Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan warga dengan 2 permohonan, "Permohonan Saya" menampilkan keduanya dengan nomor, layanan, status, dan tanggal pengajuan.
  - AC2: Detail permohonan menampilkan setiap perubahan status dengan tanggal-jam, dan alasan untuk "Perlu perbaikan" dan "Ditolak".
  - AC3: Ketika warga A membuka permohonan milik warga B, maka akses ditolak.
- **Sumber:** ASSUMPTION A-03

#### F-11 Notifikasi perubahan status

- **Kebutuhan:** Sistem harus mengirim notifikasi di portal dan lewat surel kepada warga setiap kali status permohonannya berubah.
- **Aktor:** Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Ketika petugas mengubah status menjadi "Perlu perbaikan", maka warga menerima notifikasi di portal dan surel berisi nomor permohonan, status baru, dan alasan.
  - AC2: Jumlah notifikasi belum dibaca tampil di portal; membuka notifikasi menandainya terbaca.
  - AC3: Ketika pengiriman surel gagal, perubahan status tetap tersimpan dan kegagalan tercatat di log.
- **Sumber:** ASSUMPTION A-03, A-04

### 3.4 Pemrosesan oleh petugas

#### F-12 Antrean permohonan petugas

- **Kebutuhan:** Sistem harus menampilkan kepada petugas daftar permohonan untuk layanan milik perangkat daerahnya, dapat difilter menurut status dan layanan.
- **Aktor:** Petugas layanan
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan permohonan untuk unit A dan unit B, petugas unit A hanya melihat permohonan unit A.
  - AC2: Ketika filter status "Diajukan" dipilih, maka hanya permohonan "Diajukan" yang tampil.
  - AC3: Daftar diurutkan dari pengajuan paling lama.
- **Sumber:** ASSUMPTION A-02, A-03

#### F-13 Verifikasi dan keputusan

- **Kebutuhan:** Sistem harus memungkinkan petugas memverifikasi permohonan lalu meminta perbaikan, menyetujui, atau menolaknya, dengan alasan wajib untuk perbaikan dan penolakan.
- **Aktor:** Petugas layanan
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Ketika petugas menekan "Verifikasi" pada permohonan "Diajukan", maka status menjadi "Diverifikasi".
  - AC2: Permintaan perbaikan tanpa alasan ditolak; dengan alasan, status menjadi "Perlu perbaikan".
  - AC3: "Setujui" menghasilkan status "Disetujui"; "Tolak" dengan alasan menghasilkan "Ditolak".
  - AC4: Transisi di luar BR-01 (misalnya "Ditolak" → "Disetujui") ditolak.
  - AC5: Setiap perubahan status tercatat dengan petugas, waktu, status lama, dan status baru.
- **Sumber:** ASSUMPTION A-03, A-14

#### F-14 Dokumen hasil dan penyelesaian

- **Kebutuhan:** Sistem harus memungkinkan petugas mengunggah dokumen hasil untuk permohonan "Disetujui" dan menandainya "Selesai" agar warga dapat mengunduh hasilnya.
- **Aktor:** Petugas layanan, Warga
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan permohonan "Disetujui", ketika petugas mengunggah dokumen hasil, maka status menjadi "Selesai" dan warga dapat mengunduhnya.
  - AC2: Permohonan tidak dapat ditandai "Selesai" tanpa dokumen hasil.
  - AC3: Dokumen hasil hanya dapat diunduh pemohon, petugas dan admin unit penyedia, serta super admin.
- **Sumber:** ASSUMPTION A-03, A-14

### 3.5 Administrasi

#### F-15 Kelola layanan, formulir, dan persyaratan

- **Kebutuhan:** Sistem harus memungkinkan admin perangkat daerah menambah, mengubah, mengaktifkan, dan menonaktifkan layanan unitnya, termasuk isian formulir, dokumen persyaratan, jenis berkas yang diizinkan, lama proses, dan jenis layanan.
- **Aktor:** Admin perangkat daerah
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Ketika admin membuat layanan dengan 2 isian (teks, tanggal) dan 1 dokumen wajib (PDF) lalu mengaktifkannya, maka layanan tampil di katalog dan formulirnya memuat kedua isian.
  - AC2: Admin unit A tidak dapat mengubah layanan unit B.
  - AC3: Ketika layanan dinonaktifkan, maka layanan hilang dari katalog dan permohonan yang sudah ada tetap dapat diproses.
  - AC4: Jenis isian yang tersedia: teks, angka, tanggal, pilihan.
- **Sumber:** ASSUMPTION A-02, A-03, A-14

#### F-16 Kelola perangkat daerah dan kategori

- **Kebutuhan:** Sistem harus memungkinkan super admin menambah, mengubah, dan menonaktifkan perangkat daerah dan kategori layanan.
- **Aktor:** Super admin
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Ketika super admin menambah perangkat daerah, maka unit itu dapat dipilih saat membuat akun admin, akun petugas, dan layanan.
  - AC2: Kategori yang masih dipakai layanan tidak dapat dihapus; tampil pesan penjelasan.
  - AC3: Pengguna selain super admin yang membuka fungsi ini ditolak.
- **Sumber:** ASSUMPTION A-02, A-03

#### F-17 Kelola pengguna dan peran

- **Kebutuhan:** Sistem harus memungkinkan super admin membuat dan menonaktifkan akun admin perangkat daerah dan petugas beserta unitnya, dan memungkinkan admin perangkat daerah mengelola akun petugas unitnya.
- **Aktor:** Super admin, Admin perangkat daerah
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Ketika super admin membuat akun petugas untuk unit A, maka petugas itu dapat masuk dan melihat antrean unit A.
  - AC2: Akun yang dinonaktifkan tidak dapat masuk.
  - AC3: Admin unit A hanya dapat membuat akun petugas untuk unit A.
- **Sumber:** ASSUMPTION A-02

### 3.6 Pelaporan

#### F-18 Dasbor statistik permohonan

- **Kebutuhan:** Sistem harus menampilkan dasbor jumlah permohonan per status, per layanan, dan per perangkat daerah untuk rentang tanggal yang dipilih.
- **Aktor:** Super admin, Admin perangkat daerah
- **Prioritas:** Should
- **Kriteria penerimaan:**
  - AC1: Diberikan 5 permohonan dalam rentang (3 "Selesai", 2 "Diajukan"), dasbor menampilkan 3 dan 2 pada status masing-masing.
  - AC2: Admin perangkat daerah hanya melihat angka unitnya; super admin melihat seluruh portal.
  - AC3: Dasbor menampilkan persentase permohonan "Selesai" dalam lama proses layanannya.
- **Sumber:** ASSUMPTION A-03, A-08

## 4 Kebutuhan non-fungsional

| ID | Kategori | Kebutuhan | Target | Sumber | ID Sumber |
|---|---|---|---|---|---|
| NFR-01 | Keamanan | Semua halaman dan endpoint hanya dilayani lewat HTTPS | Setiap permintaan HTTP dialihkan ke HTTPS; tidak ada endpoint yang menjawab lewat HTTP | ASSUMPTION A-05, A-10 | — |
| NFR-02 | Keamanan | Kata sandi disimpan sebagai hash satu arah | Tidak ada kata sandi teks polos di basis data maupun log | ASSUMPTION A-05 | — |
| NFR-03 | Keamanan | Akses berbasis peran pada setiap halaman dan endpoint | Akses di luar hak peran dijawab HTTP 403 | ASSUMPTION A-02, A-05 | — |
| NFR-04 | Privasi | Dokumen permohonan dan hasil disimpan privat | Hanya pemohon, petugas dan admin unit penyedia, serta super admin yang dapat mengunduh; URL langsung tanpa hak ditolak | ASSUMPTION A-05 | — |
| NFR-05 | Privasi | Pemrosesan data pribadi mengikuti UU No. 27 Tahun 2022 tentang Pelindungan Data Pribadi: persetujuan saat mendaftar dan pemberitahuan privasi | Target: perlu dikonfirmasi (retensi, hak subjek data) | ASSUMPTION A-05, A-09 | — |
| NFR-06 | Auditabilitas | Jejak audit atas perubahan status permohonan dan perubahan data layanan atau pengguna oleh admin | Setiap perubahan tercatat: pelaku, waktu, nilai sebelum dan sesudah | ASSUMPTION A-05 | — |
| NFR-07 | Bahasa | Antarmuka dan surel dalam Bahasa Indonesia | Semua teks antarmuka dan surel | ASSUMPTION A-16 | — |
| NFR-08 | Pemeliharaan | Setiap perubahan masuk lewat pull request yang lulus gerbang CI `php artisan test` sebelum digabung ke `staging` atau `main` | Setiap penggabungan ke `staging` dan `main` dengan CI hijau | [S2 "gates"; S2 "branch"] | — |
| NFR-09 | Kompatibilitas | Portal responsif di peramban desktop dan ponsel | Target: perlu dikonfirmasi (daftar peramban dan ukuran layar) | ASSUMPTION A-01, A-13 | — |

## 5 Entitas dan aturan bisnis

### 5.1 Entitas

| Entitas | Field utama | Catatan |
|---|---|---|
| Pengguna (`users`) | `name`, `email`, `phone`, `password`, `role`, `unit_id`, `email_verified_at`, `consent_at`, `is_active` | Data pribadi; dimiliki penyelenggara; retensi perlu dikonfirmasi (A-09) |
| Perangkat daerah (`units`) | `name`, `code`, `is_active` | Dikelola super admin (A-02) |
| Kategori (`categories`) | `name`, `slug` | Dikelola super admin |
| Layanan (`services`) | `name`, `category_id`, `unit_id`, `type`, `external_url`, `description`, `process_duration`, `is_active` | `type`: portal / tautan (A-01) |
| Isian formulir (`service_fields`) | `service_id`, `label`, `field_type`, `options`, `is_required`, `order` | `field_type`: teks, angka, tanggal, pilihan (A-14) |
| Persyaratan dokumen (`service_requirements`) | `service_id`, `name`, `allowed_types`, `is_required` | |
| Permohonan (`applications`) | `number`, `service_id`, `user_id`, `status`, `submitted_at`, `completed_at` | `number` unik; status mengikuti BR-01 |
| Nilai isian (`application_values`) | `application_id`, `service_field_id`, `value` | Dapat memuat data pribadi |
| Dokumen permohonan (`application_documents`) | `application_id`, `service_requirement_id`, `kind`, `path`, `mime_type` | Penyimpanan privat (NFR-04); `kind`: persyaratan / hasil |
| Riwayat status (`status_histories`) | `application_id`, `from_status`, `to_status`, `reason`, `user_id`, `created_at` | NFR-06 |
| Notifikasi (`notifications`) | `user_id`, `application_id`, `message`, `read_at` | |
| Jejak audit (`audit_logs`) | `user_id`, `action`, `subject_type`, `subject_id`, `before`, `after`, `created_at` | NFR-06 |

### 5.2 Aturan bisnis

| ID | Aturan | Sumber |
|---|---|---|
| BR-01 | Status permohonan hanya berpindah: Diajukan → Diverifikasi; Diverifikasi → Perlu perbaikan / Disetujui / Ditolak; Perlu perbaikan → Diajukan (setelah diperbaiki); Disetujui → Selesai (setelah dokumen hasil diunggah). Ditolak dan Selesai adalah status akhir | ASSUMPTION A-14 |
| BR-02 | Permohonan hanya dapat diajukan untuk layanan aktif berjenis "Ajukan di portal"; layanan "Aplikasi lain" hanya menampilkan tautan | ASSUMPTION A-01 |
| BR-03 | Semua isian dan dokumen wajib harus lengkap sebelum permohonan dapat dikirim | ASSUMPTION A-03, A-14 |
| BR-04 | Permintaan perbaikan dan penolakan wajib disertai alasan yang terlihat oleh warga | ASSUMPTION A-14 |
| BR-05 | Petugas dan admin perangkat daerah hanya dapat melihat dan memproses data layanan milik unitnya | ASSUMPTION A-02 |
| BR-06 | Warga hanya dapat melihat permohonan, dokumen, dan notifikasinya sendiri | ASSUMPTION A-02, A-05 |
| BR-07 | Akun warga harus terverifikasi surelnya sebelum dapat mengajukan permohonan | ASSUMPTION A-04 |

## 6 Kasus penggunaan

### UC-01 Menemukan layanan

- **Aktor:** Pengunjung, Warga
- **Prasyarat:** Ada layanan aktif di katalog.
- **Alur utama:**
  1. Pengguna membuka katalog.
  2. Pengguna mencari dengan kata kunci atau memilih kategori dan perangkat daerah.
  3. Pengguna membuka detail layanan.
  4. Untuk layanan "Aplikasi lain", pengguna membuka tautan aplikasinya.
- **Hasil:** Pengguna mengetahui persyaratan, alur, dan cara mengajukan layanan.
- **Kebutuhan:** F-01, F-02, F-03, F-04

### UC-02 Mendaftar dan masuk

- **Aktor:** Warga
- **Prasyarat:** Warga belum punya akun.
- **Alur utama:**
  1. Warga mengisi formulir daftar dan menyetujui pemrosesan data pribadi.
  2. Warga membuka tautan verifikasi dari surel.
  3. Warga masuk dengan surel dan kata sandi.
- **Hasil:** Warga masuk dengan akun terverifikasi.
- **Kebutuhan:** F-05, F-06, F-07

### UC-03 Mengajukan permohonan

- **Aktor:** Warga
- **Prasyarat:** Warga masuk dengan akun terverifikasi; layanan aktif berjenis "Ajukan di portal".
- **Alur utama:**
  1. Warga menekan "Ajukan Permohonan" di detail layanan.
  2. Warga mengisi formulir dan mengunggah dokumen persyaratan.
  3. Warga mengirim permohonan dan menerima nomor permohonan.
- **Hasil:** Permohonan berstatus "Diajukan" dan masuk antrean unit penyedia.
- **Kebutuhan:** F-08, F-11

### UC-04 Memproses permohonan

- **Aktor:** Petugas layanan
- **Prasyarat:** Ada permohonan "Diajukan" untuk layanan unit petugas.
- **Alur utama:**
  1. Petugas membuka antrean dan memilih permohonan.
  2. Petugas memeriksa isian dan dokumen, lalu memverifikasi.
  3. Petugas meminta perbaikan, menyetujui, atau menolak dengan alasan.
  4. Untuk permohonan yang disetujui, petugas mengunggah dokumen hasil.
- **Hasil:** Permohonan berstatus "Perlu perbaikan", "Ditolak", atau "Selesai"; warga diberi tahu.
- **Kebutuhan:** F-12, F-13, F-14, F-11

### UC-05 Memperbaiki dan memantau permohonan

- **Aktor:** Warga
- **Prasyarat:** Warga punya permohonan.
- **Alur utama:**
  1. Warga membuka "Permohonan Saya" dan melihat status serta riwayat.
  2. Untuk permohonan "Perlu perbaikan", warga membaca alasan, memperbaiki, dan mengirim ulang.
  3. Untuk permohonan "Selesai", warga mengunduh dokumen hasil.
- **Hasil:** Warga mengetahui status dan menerima hasil.
- **Kebutuhan:** F-09, F-10, F-11, F-14

### UC-06 Menyiapkan layanan

- **Aktor:** Admin perangkat daerah
- **Prasyarat:** Admin masuk; unitnya terdaftar.
- **Alur utama:**
  1. Admin membuat layanan, memilih jenis dan kategori.
  2. Admin menyusun isian formulir dan dokumen persyaratan.
  3. Admin mengaktifkan layanan.
- **Hasil:** Layanan tampil di katalog dan dapat diajukan.
- **Kebutuhan:** F-15, F-17

### UC-07 Mengelola portal

- **Aktor:** Super admin
- **Prasyarat:** Super admin masuk.
- **Alur utama:**
  1. Super admin mengelola perangkat daerah dan kategori.
  2. Super admin membuat akun admin dan petugas.
  3. Super admin membuka dasbor statistik.
- **Hasil:** Struktur portal dan pengguna siap; kinerja layanan terlihat.
- **Kebutuhan:** F-16, F-17, F-18

## 7 Antarmuka eksternal dan integrasi

| Sistem | Arah | Data yang dipertukarkan | Protokol / format | Sumber |
|---|---|---|---|---|
| Server surel penyelenggara | Keluar | Surel verifikasi, atur ulang kata sandi, notifikasi status | SMTP | ASSUMPTION A-04 |
| Aplikasi layanan yang sudah ada | Keluar | URL tautan saja, tanpa data | Tautan HTTPS | ASSUMPTION A-01 |
| Modul `portal` ↔ modul `api` (internal) | Dua arah | Semua data portal | Perlu dikonfirmasi (diusulkan REST JSON) | [S2 "modules"] |

## 8 Pertanyaan terbuka

| # | Pertanyaan | Bersandar pada | Berdampak pada | Pemilik |
|---|---|---|---|---|
| OQ-01 | Konfirmasi ASSUMPTION A-01: aplikasi web baru, "terpadu" = satu akun dan satu katalog, layanan lama ditautkan, tanpa aplikasi seluler native | A-01 | F-01, F-04, BR-02, NFR-09 | Klien / pemilik produk |
| OQ-02 | Konfirmasi ASSUMPTION A-02: penyelenggara dan lima peran beserta haknya | A-02 | F-12, F-15, F-16, F-17, NFR-03, BR-05, BR-06 | Klien / pemilik produk |
| OQ-03 | Konfirmasi ASSUMPTION A-03: fitur rilis pertama; pengaduan, pembayaran, survei kepuasan di luar cakupan | A-03 | F-01, F-02, F-03, F-05, F-06, F-08, F-09, F-10, F-11, F-12, F-13, F-14, F-15, F-16, F-18, BR-03 | Klien / pemilik produk |
| OQ-04 | Konfirmasi ASSUMPTION A-04: tanpa integrasi; masuk dengan surel dan kata sandi; SMTP penyelenggara | A-04 | F-05, F-06, F-11, BR-07 | Pengelola TI penyelenggara |
| OQ-05 | Konfirmasi ASSUMPTION A-05: regulasi yang berlaku dan ketentuan keamanan; siapa yang menyediakan teks pemberitahuan privasi | A-05 | F-05, NFR-01, NFR-02, NFR-03, NFR-04, NFR-05, NFR-06, BR-06 | Bagian hukum penyelenggara |
| OQ-06 | Konfirmasi ASSUMPTION A-06: siap UAT dan serah terima 10 Januari 2027 | A-06 | — (jadwal) | Klien / pemilik produk |
| OQ-07 | Konfirmasi ASSUMPTION A-07: tim BE-1, FE-1, OPS penuh waktu | A-07 | — (kapasitas) | Manajer proyek pengembang |
| OQ-08 | Konfirmasi ASSUMPTION A-08: ukuran keberhasilan dan angka targetnya | A-08 | F-18 | Pemilik produk |
| OQ-09 | Konfirmasi ASSUMPTION A-09: entitas data, tanpa NIK, dan masa retensi | A-09 | F-07, NFR-05 | Pengelola data penyelenggara |
| OQ-10 | Konfirmasi ASSUMPTION A-10: hosting di server penyelenggara, staging dan produksi | A-10 | NFR-01 | Pengelola TI penyelenggara |
| OQ-11 | Konfirmasi ASSUMPTION A-11: anggaran tidak dibahas | A-11 | — | Klien |
| OQ-12 | Konfirmasi ASSUMPTION A-12: siapa yang menyetujui UAT dan rilis | A-12 | — (penerimaan) | Klien |
| OQ-13 | Konfirmasi ASSUMPTION A-13: identitas visual dan desain layar | A-13 | NFR-09 | Pemilik produk |
| OQ-14 | Konfirmasi ASSUMPTION A-14: alur status dan siapa yang mengisi persyaratan layanan | A-14 | F-03, F-08, F-09, F-13, F-14, F-15, BR-01, BR-03, BR-04 | Admin perangkat daerah |
| OQ-15 | Konfirmasi ASSUMPTION A-15: kapan target non-fungsional ditetapkan | A-15 | OQ-17–OQ-20 | Pemilik produk |
| OQ-16 | Konfirmasi ASSUMPTION A-16: hanya Bahasa Indonesia | A-16 | NFR-07 | Pemilik produk |
| OQ-17 | Apakah dibutuhkan target kinerja (waktu respons, jumlah pengguna serentak)? Tidak ada sumber yang menyebutnya | Tidak ada di sumber | — | Pemilik produk |
| OQ-18 | Apakah dibutuhkan target ketersediaan (uptime, jendela pemeliharaan)? | Tidak ada di sumber | — | Pengelola TI penyelenggara |
| OQ-19 | Apakah dibutuhkan standar aksesibilitas (misalnya WCAG)? | Tidak ada di sumber | — | Pemilik produk |
| OQ-20 | Apakah dibutuhkan cadangan dan pemulihan (frekuensi, target pemulihan)? | Tidak ada di sumber | — | Pengelola TI penyelenggara |
| OQ-21 | Berapa batas ukuran berkas unggahan dan masa berlaku tautan verifikasi dan atur ulang kata sandi? | Tidak ada di sumber | F-05, F-06, F-08 | Pemilik produk |
| OQ-22 | Target kepatuhan NFR-05: masa retensi data dan cara warga menjalankan hak subjek data | Kesenjangan G5, G9 | NFR-05 | Bagian hukum penyelenggara |
| OQ-23 | Target NFR-09: daftar peramban dan ukuran layar yang didukung | Kesenjangan G13 | NFR-09 | Pemilik produk |

## Keterlacakan

| Kebutuhan | Sumber | ID Sumber |
|---|---|---|
| F-01 | [S1]; ASSUMPTION A-01, A-03 | — |
| F-02 | ASSUMPTION A-03 | — |
| F-03 | ASSUMPTION A-03, A-14 | — |
| F-04 | [S1]; ASSUMPTION A-01 | — |
| F-05 | ASSUMPTION A-03, A-04, A-05 | — |
| F-06 | ASSUMPTION A-03, A-04 | — |
| F-07 | ASSUMPTION A-09 | — |
| F-08 | ASSUMPTION A-03, A-14 | — |
| F-09 | ASSUMPTION A-03, A-14 | — |
| F-10 | ASSUMPTION A-03 | — |
| F-11 | ASSUMPTION A-03, A-04 | — |
| F-12 | ASSUMPTION A-02, A-03 | — |
| F-13 | ASSUMPTION A-03, A-14 | — |
| F-14 | ASSUMPTION A-03, A-14 | — |
| F-15 | ASSUMPTION A-02, A-03, A-14 | — |
| F-16 | ASSUMPTION A-02, A-03 | — |
| F-17 | ASSUMPTION A-02 | — |
| F-18 | ASSUMPTION A-03, A-08 | — |
| NFR-01 | ASSUMPTION A-05, A-10 | — |
| NFR-02 | ASSUMPTION A-05 | — |
| NFR-03 | ASSUMPTION A-02, A-05 | — |
| NFR-04 | ASSUMPTION A-05 | — |
| NFR-05 | ASSUMPTION A-05, A-09 | — |
| NFR-06 | ASSUMPTION A-05 | — |
| NFR-07 | ASSUMPTION A-16 | — |
| NFR-08 | [S2 "gates"; S2 "branch"] | — |
| NFR-09 | ASSUMPTION A-01, A-13 | — |
| BR-01 | ASSUMPTION A-14 | — |
| BR-02 | ASSUMPTION A-01 | — |
| BR-03 | ASSUMPTION A-03, A-14 | — |
| BR-04 | ASSUMPTION A-14 | — |
| BR-05 | ASSUMPTION A-02 | — |
| BR-06 | ASSUMPTION A-02, A-05 | — |
| BR-07 | ASSUMPTION A-04 | — |

Langkah berikutnya: Lanewright Sprint Planner mengubah dokumen ini menjadi rencana sprint mingguan.
