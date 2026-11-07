# Rencana Sprint Mingguan — Superapps

| Ruas | Isi |
|---|---|
| Judul | Rencana Sprint Mingguan — Superapps |
| Versi | 1.0 |
| Metode | Scrum, sprint satu minggu (Senin–Minggu) |
| Sumber data | docs/requirements/srs.md (versi 0.1 draf, 2026-11-07) |
| Cakupan produk | Portal web layanan publik terpadu: katalog layanan, akun warga, permohonan daring, pemrosesan petugas, pelacakan dan notifikasi, administrasi |
| Status | Draf untuk persetujuan product owner |

## 1 Pendahuluan

### 1.1 Tujuan

Rencana ini membagi kebutuhan SRS Superapps menjadi delapan sprint mingguan yang dapat dikomitmenkan tim. Setiap sprint punya satu Sprint Goal yang dapat didemokan, dan kapasitas tim tidak pernah dilampaui.

### 1.2 Ruang Lingkup

Tercakup: F-01–F-06, F-08–F-17, NFR-01–NFR-09, BR-01–BR-07, ditambah item fondasi (repositori, CI, lingkungan, skema, otorisasi, kontrak API). Kapasitas total cukup (192 SP kebutuhan vs 204 SP kapasitas). Namun pekerjaan tidak muat dalam 8 minggu karena dua hal: layar frontend baru dapat dibuat sesudah API-nya selesai di sprint sebelumnya, dan kapasitas per orang turun menjadi 6 SP di sprint 6–8. Berikut yang tidak muat (25 SP) dan diusulkan untuk sprint 9 atau sesudahnya:

| Item yang tidak muat | Kebutuhan | PIC | SP | Akibat |
|---|---|---|---|---|
| Layar super admin: perangkat daerah, kategori, pengguna | F-16, F-17 (layar) | FE-1 | 5 | API tersedia (sprint 7), tetapi super admin belum punya layar; data awal lewat seeder |
| Pusat notifikasi di portal (jumlah belum dibaca) | F-11 AC2 (layar) | FE-1 | 3 | Notifikasi surel berjalan; notifikasi di portal hanya lewat API |
| API dasbor statistik | F-18 | BE-1 | 3 | Dasbor tidak ada di rilis pertama |
| Layar dasbor statistik | F-18 | FE-1 | 5 | Sama seperti di atas |
| API profil warga | F-07 (Could) | BE-1 | 2 | Warga belum dapat mengubah profil |
| Layar profil warga | F-07 (Could) | FE-1 | 2 | Sama seperti di atas |
| Uji fitur API super admin | F-16, F-17 | OPS | 2 | Hanya diuji manual pada UAT |
| Perbaikan temuan UAT (frontend) | — | FE-1 | 3 | Temuan UAT frontend diperbaiki sesudah 10 Januari 2027 |

### 1.3 Dasar

Dasarnya SRS versi 0.1 (draf). Hampir semua kebutuhannya bersandar pada asumsi A-01–A-16 dari intake, karena klien hanya memberi satu baris brief. Hanya F-01 yang berprioritas Must; F-07 Could; sisanya Should. Item yang bersandar pada asumsi tetap membawa labelnya melalui ID kebutuhan SRS.

Asumsi perencanaan (bawaan yang diambil tanpa jawaban):

- PA-01 Tanggal akhir 10 Januari 2027 (8 minggu, hari 56), sama dengan ASSUMPTION A-06 di SRS — perlu dikonfirmasi dengan product owner
- PA-02 Tim BE-1, FE-1, OPS penuh waktu (ASSUMPTION A-07); OPS juga memegang pengujian otomatis (wilayah `tests`) karena tim bawaan tidak punya QA — perlu dikonfirmasi dengan manajer proyek pengembang
- PA-03 Kapasitas 10 SP per orang untuk minggu penuh, 6 SP untuk minggu dengan 4 hari kerja atau kurang — perlu dikonfirmasi dengan manajer proyek pengembang
- PA-04 Libur nasional Indonesia dalam periode: Natal 25 Desember 2026 (Jumat) dan Tahun Baru 1 Januari 2027 (Jumat); cuti bersama Natal tanggal perlu dikonfirmasi; Isra Mikraj 1448 H tanggal perlu dikonfirmasi (mungkin jatuh di sprint 8). Tidak ada cuti pribadi — perlu dikonfirmasi dengan manajer proyek pengembang
- PA-05 Tonggak: demo di setiap Sprint Review; UAT di sprint 8; serah terima 10 Januari 2027; tanggal go-live di luar rencana ini (tanggal perlu dikonfirmasi) — perlu dikonfirmasi dengan product owner
- PA-06 Modul `portal` memanggil modul `api` lewat REST JSON di bawah `/api/v1`; layar frontend dibuat sesudah API-nya selesai di sprint sebelumnya — perlu dikonfirmasi dengan pemimpin teknis
- PA-07 Pemetaan kode tim ke wilayah kit.json: BE-1 → `api` (module-dev) dan `shared` (shared-module-owner); FE-1 → `portal` (module-dev); OPS → `tooling` (platform-tooling) dan `tests` (qa-test-engineer). Berkas akar Laravel (`composer.json`, `config/`, `routes/`, `artisan`) dan `docs/**` tidak tercakup wilayah mana pun; item yang menyentuhnya dicatat di `tooling` — perlu dikonfirmasi dengan pemilik platform
- PA-08 Product owner: kepala unit pengelola portal (ASSUMPTION A-12); waktu acara Scrum seperti di 2.3 (WIB) — perlu dikonfirmasi dengan product owner

### 1.4 Asumsi Tanggal

- Mulai proyek: Senin, 16 November 2026 (hari 1) [request]. Akhir: Minggu, 10 Januari 2027 (hari 56).
- Sprint berjalan Senin sampai Minggu; hari kerja Senin sampai Jumat.
- Libur dan cuti: 25 Desember 2026 Natal (sprint 6); 1 Januari 2027 Tahun Baru (sprint 7); cuti bersama Natal, tanggal perlu dikonfirmasi (PA-04); Isra Mikraj 1448 H, tanggal perlu dikonfirmasi (PA-04). Sprint 6 dan 7 masing-masing punya paling banyak 4 hari kerja, jadi kapasitasnya 6 SP per orang. Sprint 8 juga dihitung 6 SP per orang sebagai langkah hati-hati, sampai tanggal Isra Mikraj pasti. Bila tanggal itu jatuh di luar sprint 8, kapasitas sprint 8 naik ke 30 SP.

## 2 Kerangka Kerja Scrum

### 2.1 Peran

- **Product owner:** kepala unit pengelola portal (PA-08); memiliki backlog dan menerima increment.
- **Scrum master / orkestrator:** orkestrator Lanewright bersama ketua tim pengembang; menjalankan acara, menyingkirkan hambatan, menjaga kapasitas.
- **Developer:** BE-1, FE-1, OPS.

### 2.2 Artefak

- **Product backlog:** kebutuhan SRS yang dipecah menjadi item (rencana ini).
- **Sprint backlog:** `docs/sprints/sprint-{nn}-backlog.md`, satu berkas per sprint.
- **Increment:** hasil yang ter-deploy di staging dan dapat didemokan di akhir setiap sprint.

### 2.3 Acara

| Acara | Jadwal | Durasi | Peserta | Keluaran |
|---|---|---|---|---|
| Sprint Planning | Hari 1 tiap sprint (Senin), 09:00 | 1 jam | Seluruh tim, product owner | Sprint Goal dan sprint backlog |
| Daily Scrum | Setiap hari kerja, 09:15 WIB (PA-08) | 15 menit | Developer | Rencana hari itu, hambatan |
| Backlog Refinement | Hari 4 tiap sprint (Kamis), 14:00 | 1 jam | Product owner, developer | Item sprint berikutnya siap |
| Sprint Review | Hari kerja terakhir sprint, 14:00 WIB (PA-08) | 1 jam | Seluruh tim, pemangku kepentingan | Increment diterima, masukan |
| Sprint Retrospective | Hari kerja terakhir sprint, sesudah review | 45 menit | Seluruh tim | Paling banyak tiga tindakan perbaikan |

Hari kerja terakhir: sprint 6 Kamis 24 Desember 2026 (Rabu 23 Desember bila 24 Desember cuti bersama); sprint 7 Kamis 31 Desember 2026; sprint lain hari Jumat.

### 2.4 Aturan Kerja Tim

- Satu item dikerjakan per orang pada satu waktu; selesaikan sebelum memulai yang berikutnya.
- Setiap perubahan lewat pull request dengan CI hijau (`php artisan test`) dan tinjauan (NFR-08).
- Hambatan diangkat di Daily Scrum, atau segera bila menghentikan pekerjaan.
- Sprint Goal tidak berubah selama sprint; pekerjaan baru masuk backlog.

## 3 Komposisi Tim dan Kapasitas

| Peran | Personel / Repositori | Kapasitas per Sprint | Catatan |
|---|---|---|---|
| BE-1 | 1 / `api/**`, `database/**` | 10 SP (sprint 6–8: 6 SP) | Backend Laravel; wilayah `api` (module-dev) dan `shared` (shared-module-owner) |
| FE-1 | 1 / `portal/**` | 10 SP (sprint 6–8: 6 SP) | Frontend portal; wilayah `portal` (module-dev) |
| OPS | 1 / `.github/**`, `*/tests/**` | 10 SP (sprint 6–8: 6 SP) | DevOps/CI dan pengujian; wilayah `tooling` (platform-tooling) dan `tests` (qa-test-engineer) |
| **Total** | 3 | 30 SP (sprint 6–8: 18 SP); 204 SP selama 8 sprint | 10 SP per orang per minggu penuh; 6 SP untuk minggu dengan 4 hari kerja atau kurang; paruh waktu pro rata (setengah waktu → 5 SP) |

| Periode | Personel | Kapasitas Total | Akibat |
|---|---|---|---|
| Sprint 6 (21 – 27 Desember 2026) | 3 | 18 SP | Natal 25 Desember; cuti bersama tanggal perlu dikonfirmasi. Item besar frontend dipecah; layar keputusan petugas pindah ke sprint 7 |
| Sprint 7 (28 Desember 2026 – 3 Januari 2027) | 3 | 18 SP | Tahun Baru 1 Januari. API super admin di sprint ini, sehingga layarnya tidak muat sebelum tanggal akhir |
| Sprint 8 (4 – 10 Januari 2027) | 3 | 18 SP | Dihitung hati-hati karena Isra Mikraj tanggal perlu dikonfirmasi. Dasbor, profil, dan perbaikan UAT frontend tidak muat (lihat 1.2) |

## 4 Definition of Ready dan Definition of Done

### 4.1 Definition of Ready

- Item tertelusur ke kebutuhan SRS atau merupakan item fondasi yang dinamai.
- Kriteria penerimaan dapat diuji dan disepakati dengan product owner.
- Estimasi 10 SP atau kurang; dependensi sudah selesai atau direncanakan lebih awal.
- PIC sudah ditetapkan dan punya kapasitas di sprint itu.

### 4.2 Definition of Done

| Jenis Pekerjaan | Kriteria Selesai |
|---|---|
| Backend / API | Kriteria penerimaan terpenuhi; tes lulus; lint bersih; OpenAPI diperbarui; ditinjau dan digabung |
| Frontend / mobile | Kriteria penerimaan terpenuhi di peramban desktop dan ponsel uji; sesuai layar yang disepakati; ditinjau dan digabung |
| Database | Migrasi dan rollback teruji; seed data bila perlu; ditinjau dan digabung |
| DevOps / CI | Pipeline hijau; deploy terdokumentasi; rahasia tidak ada di repositori |
| QA | Kasus uji ditulis dan dijalankan; cacat dicatat; regresi dijalankan pada increment |
| Dokumentasi | Diperbarui di repositori dan ditinjau |

## 5 Peta Sprint

| Sprint | Periode | Hari | Sprint Goal |
|---|---|---|---|
| 1 | 16 – 22 November 2026 | 1–7 | Kerangka Laravel berjalan di staging dengan CI hijau, dan API katalog mengembalikan layanan contoh |
| 2 | 23 – 29 November 2026 | 8–14 | Pengunjung dapat menjelajah, mencari, dan membuka detail layanan di portal staging |
| 3 | 30 November – 6 Desember 2026 | 15–21 | Warga dapat mendaftar, memverifikasi surel, masuk, dan keluar di portal |
| 4 | 7 – 13 Desember 2026 | 22–28 | Admin perangkat daerah dapat membuat dan mengaktifkan layanan beserta formulirnya; lingkungan produksi siap |
| 5 | 14 – 20 Desember 2026 | 29–35 | Warga dapat mengajukan permohonan dengan formulir dan unggahan dokumen di portal |
| 6 | 21 – 27 Desember 2026 | 36–42 | Petugas melihat antrean unitnya, warga memantau permohonannya, dan surel notifikasi terkirim saat status berubah |
| 7 | 28 Desember 2026 – 3 Januari 2027 | 43–49 | Petugas dapat memverifikasi, meminta perbaikan, menyetujui, atau menolak permohonan di portal |
| 8 | 4 – 10 Januari 2027 | 50–56 | Alur ujung-ke-ujung (ajukan → proses → perbaikan → selesai dan unduh hasil) lulus UAT, dan dokumen serah terima diserahkan |

| Tonggak | Sprint |
|---|---|
| Demo pertama: katalog layanan di staging | 2 |
| Lingkungan produksi siap | 4 |
| Alur pengajuan warga dapat didemokan | 5 |
| UAT (PA-05) | 8 |
| Serah terima, 10 Januari 2027 (PA-01, PA-05) | 8 |

## 6 Rencana Detail per Sprint

<!-- pagebreak -->

### 6.1 Sprint 1 — 16 – 22 November 2026 (Hari 1–7)

Sprint Goal: Kerangka Laravel berjalan di staging dengan CI hijau, dan API katalog mengembalikan layanan contoh.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| OPS-S01-01 | Kerangka Laravel, struktur modul `portal` dan `api`, branch `staging`/`main` (hari 1–2) | OPS | 2 | Fondasi; aplikasi Laravel lulus `php artisan test`; direktori `portal/`, `api/`, `database/` sesuai kit.json; branch `staging` dibuat; README cara menjalankan lokal |
| OPS-S01-02 | CI GitHub Actions: lint (Pint) dan `php artisan test` di setiap pull request | OPS | 3 | NFR-08: pull request ke `staging`/`main` menjalankan lint dan tes; pull request dengan tes gagal tidak dapat digabung |
| OPS-S01-03 | Lingkungan staging, penanganan rahasia, deploy otomatis dari `staging` | OPS | 5 | Fondasi (A-10); penggabungan ke `staging` men-deploy otomatis; `.env` tidak ada di repositori; rahasia di GitHub Secrets; migrasi berjalan saat deploy |
| BE-1-S01-01 | Konvensi dan kontrak API: `/api/v1`, format respons dan galat JSON, OpenAPI (hari 1–2) | BE-1 | 2 | Fondasi; format sukses dan galat seragam terdokumentasi; galat validasi → HTTP 422 dengan daftar field; OpenAPI di repositori |
| BE-1-S01-02 | Skema inti dan seeder: `users`, `roles`, `units`, `categories`, `services` | BE-1 | 5 | Fondasi (A-09); migrasi naik dan turun bersih; seeder: 4 peran, 1 super admin dari variabel lingkungan (tanpa kata sandi di repositori), 2 unit, 3 kategori, 5 layanan contoh |
| BE-1-S01-03 | API katalog: daftar, pencarian, filter, detail layanan | BE-1 | 3 | F-01 AC1–AC3; F-02 AC1–AC3; data untuk F-03 AC1 dan F-04 AC1; hanya layanan aktif |
| FE-1-S01-01 | Kerangka portal: tata letak responsif, navigasi, teks Bahasa Indonesia, klien API | FE-1 | 5 | NFR-07; NFR-09 (target perlu dikonfirmasi, OQ-23); klien API memakai format galat BE-1-S01-01 |
| FE-1-S01-02 | Komponen antarmuka dasar: formulir, tabel, unggah berkas, pesan galat dan sukses | FE-1 | 3 | Fondasi; galat HTTP 422 tampil di bawah field terkait; halaman contoh komponen |

Total komitmen: 28 story point — 3 personel, kapasitas 30 SP.

#### Risiko dan Ketergantungan

- BE-1-S01-01, BE-1-S01-02 dan FE-1-S01-01 butuh OPS-S01-01 (hari 1–2) — OPS menyelesaikan kerangka pada hari 1.
- FE-1-S01-01 butuh BE-1-S01-01 (hari 1–2) — kontrak API disepakati pada hari 2.
- Server staging belum tentu tersedia (A-10) — OPS meminta akses pada hari 1; bila belum ada, staging sementara di server tim dan dicatat di tinjauan.

#### Increment yang Didemokan

CI hijau di GitHub, portal kosong ber-tata letak responsif di staging, dan `GET /api/v1/services` mengembalikan 5 layanan contoh.

<!-- pagebreak -->

### 6.2 Sprint 2 — 23 – 29 November 2026 (Hari 8–14)

Sprint Goal: Pengunjung dapat menjelajah, mencari, dan membuka detail layanan di portal staging.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| OPS-S02-01 | HTTPS wajib dan header keamanan di staging | OPS | 2 | NFR-01: permintaan HTTP dialihkan ke HTTPS; header HSTS terkirim; cookie sesi bertanda Secure |
| OPS-S02-02 | Uji fitur API katalog (`api/tests`) | OPS | 3 | F-01 AC1–AC3 dan F-02 AC1–AC3 sebagai tes otomatis yang berjalan di CI |
| BE-1-S02-01 | Otorisasi berbasis peran: middleware dan policy | BE-1 | 3 | NFR-03: akses di luar hak peran → HTTP 403; policy BR-05 dan BR-06 siap dipakai endpoint berikutnya |
| BE-1-S02-02 | API autentikasi: daftar dengan persetujuan PDP, verifikasi surel, masuk, keluar, atur ulang kata sandi | BE-1 | 5 | F-05 AC1–AC4; F-06 AC1–AC4; NFR-02; NFR-05 (waktu persetujuan tersimpan); BR-07 |
| BE-1-S02-03 | Skema formulir dan persyaratan: `service_fields`, `service_requirements` | BE-1 | 2 | Migrasi naik dan turun bersih; jenis isian teks, angka, tanggal, pilihan (F-15 AC4); jenis berkas yang diizinkan per persyaratan |
| FE-1-S02-01 | Halaman katalog dan pencarian | FE-1 | 5 | F-01 AC1–AC3; F-02 AC1–AC3 |
| FE-1-S02-02 | Halaman detail layanan dan tautan aplikasi lain | FE-1 | 3 | F-03 AC1; F-04 AC1; BR-02; tombol "Ajukan Permohonan" tampil (pengalihan masuk F-03 AC2 di FE-1-S03-01) |

Total komitmen: 23 story point — 3 personel, kapasitas 30 SP.

#### Risiko dan Ketergantungan

- FE-1-S02-01 dan FE-1-S02-02 butuh BE-1-S01-03 (sprint 1) — sudah selesai sebelumnya.
- Teks pemberitahuan privasi untuk persetujuan PDP belum ada (OQ-05) — BE-1 memakai teks sementara; product owner memberi teks final sebelum sprint 3.

#### Increment yang Didemokan

Pengunjung membuka portal staging lewat HTTPS, menelusuri katalog per kategori, mencari "izin", dan membuka detail layanan, termasuk layanan yang menautkan aplikasi lain. Ini demo pertama.

<!-- pagebreak -->

### 6.3 Sprint 3 — 30 November – 6 Desember 2026 (Hari 15–21)

Sprint Goal: Warga dapat mendaftar, memverifikasi surel, masuk, dan keluar di portal.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| BE-1-S03-01 | Skema permohonan: `applications`, `application_values`, `application_documents`, `status_histories`, `audit_logs` | BE-1 | 3 | Migrasi naik dan turun bersih; indeks unik `number`; status sesuai BR-01; struktur jejak audit NFR-06 |
| BE-1-S03-02 | API admin perangkat daerah: kelola layanan, formulir, persyaratan | BE-1 | 5 | F-15 AC1–AC4; F-04 AC2; BR-05; NFR-06 (perubahan layanan tercatat) |
| FE-1-S03-01 | Layar daftar, verifikasi surel, masuk, keluar, atur ulang kata sandi | FE-1 | 5 | F-05 AC1–AC4; F-06 AC1–AC4; F-03 AC2 (kembali ke formulir setelah masuk) |
| FE-1-S03-02 | Beranda portal dan halaman pemberitahuan privasi | FE-1 | 3 | F-01: beranda menampilkan kategori dan kotak pencarian; NFR-05: pemberitahuan privasi tertaut dari formulir daftar |
| OPS-S03-01 | Uji fitur autentikasi dan otorisasi peran | OPS | 3 | F-05 AC1–AC4, F-06 AC1–AC4, NFR-02, NFR-03, BR-07 sebagai tes otomatis |

Total komitmen: 19 story point — 3 personel, kapasitas 30 SP.

#### Risiko dan Ketergantungan

- FE-1-S03-01 butuh BE-1-S02-02 (sprint 2); OPS-S03-01 butuh BE-1-S02-01 dan BE-1-S02-02 (sprint 2) — selesai sebelumnya.
- Surel verifikasi butuh SMTP penyelenggara (A-04) — OPS memakai SMTP uji di staging sampai akses SMTP penyelenggara diberikan.
- Kapasitas sisa 11 SP (terutama OPS) tidak dapat dipakai untuk layar karena API-nya belum ada — dipakai untuk tinjauan kode dan perbaikan cacat.

#### Increment yang Didemokan

Warga baru mendaftar dengan persetujuan PDP, menerima surel verifikasi, memverifikasi, masuk, keluar, dan mengatur ulang kata sandi di staging.

<!-- pagebreak -->

### 6.4 Sprint 4 — 7 – 13 Desember 2026 (Hari 22–28)

Sprint Goal: Admin perangkat daerah dapat membuat dan mengaktifkan layanan beserta formulirnya; lingkungan produksi siap.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| BE-1-S04-01 | API pengajuan permohonan: isi formulir, kirim, nomor unik | BE-1 | 5 | F-08 AC1, AC2, AC4; BR-02; BR-03; BR-07 |
| BE-1-S04-02 | Unggah dokumen persyaratan ke penyimpanan privat dan unduh berhak | BE-1 | 3 | F-08 AC3; NFR-04; BR-06 |
| BE-1-S04-03 | API "Permohonan Saya": daftar dan riwayat status | BE-1 | 2 | F-10 AC1–AC3; BR-06 |
| FE-1-S04-01 | Layar admin perangkat daerah: kelola layanan, formulir, persyaratan | FE-1 | 8 | F-15 AC1–AC4; F-04 AC2 |
| OPS-S04-01 | Lingkungan produksi dan deploy dari `main` | OPS | 5 | A-10; penggabungan ke `main` men-deploy ke produksi setelah persetujuan manual; HTTPS dan header sama dengan staging (NFR-01); rahasia terpisah dari staging |
| OPS-S04-02 | Uji fitur API admin layanan | OPS | 3 | F-15 AC1–AC4, F-04 AC2, BR-05 sebagai tes otomatis |

Total komitmen: 26 story point — 3 personel, kapasitas 30 SP.

#### Risiko dan Ketergantungan

- FE-1-S04-01 dan OPS-S04-02 butuh BE-1-S03-02 (sprint 3) — selesai sebelumnya.
- Server produksi penyelenggara belum pasti (A-10, OQ-10) — keputusan hosting dibutuhkan sebelum sprint 4; bila belum ada, OPS-S04-01 pindah ke sprint berikutnya yang punya kapasitas OPS.
- Batas ukuran unggahan belum ditetapkan (OQ-21) — BE-1 memakai batas yang dapat dikonfigurasi lewat variabel lingkungan.

#### Increment yang Didemokan

Admin perangkat daerah membuat layanan dengan dua isian dan satu dokumen wajib PDF, mengaktifkannya, dan layanan itu tampil di katalog. Produksi menjawab lewat HTTPS.

<!-- pagebreak -->

### 6.5 Sprint 5 — 14 – 20 Desember 2026 (Hari 29–35)

Sprint Goal: Warga dapat mengajukan permohonan dengan formulir dan unggahan dokumen di portal.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| BE-1-S05-01 | API antrean petugas per perangkat daerah | BE-1 | 2 | F-12 AC1–AC3; BR-05 |
| BE-1-S05-02 | API keputusan petugas: verifikasi, minta perbaikan, setujui, tolak, dengan jejak audit | BE-1 | 5 | F-13 AC1–AC5; BR-01; BR-04; NFR-06 |
| BE-1-S05-03 | API perbaikan oleh warga dan dokumen hasil / penyelesaian | BE-1 | 3 | F-09 AC1–AC2; F-14 AC1–AC3; NFR-04 |
| FE-1-S05-01 | Layar pengajuan permohonan: formulir dinamis per layanan | FE-1 | 5 | F-08 AC1, AC2, AC4 |
| FE-1-S05-02 | Unggah dokumen persyaratan di layar pengajuan | FE-1 | 3 | F-08 AC2 (dokumen wajib), AC3 |
| OPS-S05-01 | Uji fitur pengajuan, unggahan, dan akses dokumen | OPS | 5 | F-08 AC1–AC4, F-10 AC1–AC3, NFR-04, BR-03, BR-06 sebagai tes otomatis |

Total komitmen: 23 story point — 3 personel, kapasitas 30 SP.

#### Risiko dan Ketergantungan

- FE-1-S05-01 dan FE-1-S05-02 butuh BE-1-S04-01 dan BE-1-S04-02 (sprint 4); OPS-S05-01 butuh BE-1-S04-01–03 (sprint 4) — selesai sebelumnya.
- Alur status BR-01 masih asumsi (A-14, OQ-14) — product owner mengonfirmasinya sebelum sprint 5 dimulai; perubahan sesudahnya masuk backlog.

#### Increment yang Didemokan

Warga terverifikasi mengajukan permohonan dengan isian dan dokumen PDF, menerima nomor unik, dan permohonan itu tampil di "Permohonan Saya" lewat API.

<!-- pagebreak -->

### 6.6 Sprint 6 — 21 – 27 Desember 2026 (Hari 36–42)

Sprint Goal: Petugas melihat antrean unitnya, warga memantau permohonannya, dan surel notifikasi terkirim saat status berubah.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| BE-1-S06-01 | Notifikasi perubahan status: di portal (API) dan surel lewat antrean | BE-1 | 5 | F-11 AC1–AC3 (API daftar notifikasi dan jumlah belum dibaca); SMTP penyelenggara (A-04) |
| FE-1-S06-01 | Layar antrean dan detail permohonan untuk petugas | FE-1 | 3 | F-12 AC1–AC3 |
| FE-1-S06-02 | Layar "Permohonan Saya" dan riwayat status | FE-1 | 3 | F-10 AC1–AC3 |
| OPS-S06-01 | Uji fitur alur petugas, transisi status, dan jejak audit | OPS | 5 | F-12 AC1–AC3, F-13 AC1–AC5, F-09 AC1–AC2, F-14 AC1–AC3, BR-01, BR-04, BR-05, NFR-06 sebagai tes otomatis |

Total komitmen: 16 story point — 3 personel, kapasitas 18 SP.

#### Risiko dan Ketergantungan

- FE-1-S06-01 butuh BE-1-S05-01 (sprint 5); FE-1-S06-02 butuh BE-1-S04-03 (sprint 4); OPS-S06-01 butuh BE-1-S05-01–03 (sprint 5) — selesai sebelumnya.
- Minggu libur Natal; cuti bersama tanggal perlu dikonfirmasi — bila hari kerja tinggal 3, item tetap muat karena kapasitas sudah dihitung 6 SP per orang.

#### Increment yang Didemokan

Petugas unit A melihat hanya permohonan unit A. Warga melihat daftar permohonannya dan riwayat status. Perubahan status lewat API mengirim surel notifikasi.

<!-- pagebreak -->

### 6.7 Sprint 7 — 28 Desember 2026 – 3 Januari 2027 (Hari 43–49)

Sprint Goal: Petugas dapat memverifikasi, meminta perbaikan, menyetujui, atau menolak permohonan di portal.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| BE-1-S07-01 | API super admin: perangkat daerah, kategori, pengguna, dan peran | BE-1 | 5 | F-16 AC1–AC3; F-17 AC1–AC3; NFR-03; NFR-06 |
| FE-1-S07-01 | Layar keputusan petugas: verifikasi, minta perbaikan, setujui, tolak | FE-1 | 5 | F-13 AC1–AC4 |
| OPS-S07-01 | Uji fitur notifikasi | OPS | 2 | F-11 AC1–AC3 sebagai tes otomatis (surel dipalsukan) |
| OPS-S07-02 | Uji peramban alur warga: katalog, daftar, ajukan (`portal/tests`) | OPS | 3 | F-01 AC1, F-05 AC1, F-08 AC1 lewat peramban otomatis di CI |

Total komitmen: 15 story point — 3 personel, kapasitas 18 SP.

#### Risiko dan Ketergantungan

- FE-1-S07-01 butuh BE-1-S05-02 (sprint 5) dan FE-1-S06-01 (sprint 6); OPS-S07-01 butuh BE-1-S06-01 (sprint 6); OPS-S07-02 butuh FE-1-S02-01–FE-1-S05-02 — selesai sebelumnya.
- Layar super admin tidak muat sebelum tanggal akhir (lihat 1.2) — sampai sprint 9, perangkat daerah dan akun dibuat lewat seeder atau API.

#### Increment yang Didemokan

Petugas memverifikasi permohonan, meminta perbaikan dengan alasan, lalu menyetujui atau menolak di portal; warga menerima surel untuk setiap perubahan.

<!-- pagebreak -->

### 6.8 Sprint 8 — 4 – 10 Januari 2027 (Hari 50–56)

Sprint Goal: Alur ujung-ke-ujung (ajukan → proses → perbaikan → selesai dan unduh hasil) lulus UAT, dan dokumen serah terima diserahkan.

#### Sprint Backlog

| No | Item Sprint Backlog | PIC | SP | Kriteria Selesai |
|---|---|---|---|---|
| OPS-S08-01 | UAT: data UAT di staging, skenario uji, regresi (hari 1–2) | OPS | 3 | Skenario UAT untuk UC-01–UC-06 (UC-07 lewat API); seluruh tes otomatis hijau; temuan dicatat dengan prioritas |
| BE-1-S08-01 | Pengerasan keamanan: tinjauan otorisasi semua endpoint dan header keamanan | BE-1 | 3 | NFR-03: setiap endpoint punya tes 403 untuk peran tanpa hak; NFR-01 diperiksa di staging dan produksi |
| BE-1-S08-02 | Perbaikan temuan UAT (backend) | BE-1 | 3 | Temuan UAT backend berprioritas tinggi diperbaiki dan diuji ulang |
| FE-1-S08-01 | Layar perbaikan permohonan (warga) dan unggah dokumen hasil (petugas) | FE-1 | 5 | F-09 AC1–AC2; F-14 AC1–AC3 |
| OPS-S08-02 | Dokumen serah terima `docs/sprints/handover.md` | OPS | 3 | Arsitektur, cara deploy, variabel lingkungan tanpa nilai rahasia, akun per peran, item yang tidak muat, pertanyaan terbuka; ditinjau product owner |

Total komitmen: 17 story point — 3 personel, kapasitas 18 SP.

#### Risiko dan Ketergantungan

- BE-1-S08-02 butuh OPS-S08-01 (hari 1–2) — perbaikan UAT berbagi sprint UAT.
- FE-1-S08-01 butuh BE-1-S05-03 (sprint 5) dan FE-1-S07-01 (sprint 7) — selesai sebelumnya; layar ini selesai paling akhir, jadi skenario UAT perbaikan dan hasil dijalankan di akhir minggu.
- Tidak ada kapasitas frontend untuk perbaikan temuan UAT — temuan frontend masuk sprint 9 (lihat 1.2).
- Isra Mikraj tanggal perlu dikonfirmasi — bila jatuh di luar sprint 8, kapasitas sprint 8 naik ke 30 SP dan item yang tidak muat dapat ditarik masuk sesuai urutan di 1.2.

#### Increment yang Didemokan

Satu permohonan berjalan dari pengajuan sampai "Selesai" di staging: verifikasi, perbaikan oleh warga, persetujuan, unggah dokumen hasil, dan warga mengunduh hasilnya. Dokumen serah terima diserahkan.

## 7 Manajemen Risiko Proyek

| Risiko | Tingkat | Mitigasi |
|---|---|---|
| Hampir semua kebutuhan bersandar pada asumsi (A-01–A-16); klien dapat mengubah cakupan | Tinggi | Product owner mengonfirmasi OQ-01–OQ-16 sebelum Sprint Planning sprint 2; perubahan masuk backlog, bukan sprint berjalan |
| Pekerjaan 25 SP tidak muat sebelum 10 Januari 2027 (layar super admin, dasbor, profil, perbaikan UAT frontend) | Tinggi | Sprint 9 atau penambahan satu pengembang frontend; keputusan product owner di Sprint Review sprint 4 |
| Server staging/produksi dan SMTP penyelenggara belum tersedia (A-04, A-10) | Sedang | Permintaan akses pada hari 1; staging dan SMTP uji sementara |
| Libur akhir tahun dan cuti bersama mengurangi kapasitas | Sedang | Kapasitas sprint 6–8 sudah dihitung 6 SP per orang; tanggal cuti bersama dan Isra Mikraj dikonfirmasi sebelum sprint 6 |
| Frontend selalu satu sprint di belakang API | Sedang | Kontrak OpenAPI diperbarui di setiap item API; layar dikerjakan dari kontrak itu |
| Teks pemberitahuan privasi dan regulasi belum pasti (A-05, OQ-05) | Sedang | Teks sementara; tinjauan bagian hukum sebelum UAT |
| Satu orang per peran: sakit atau cuti menghentikan satu jalur | Sedang | Tinjauan silang kode; dokumentasi di setiap item |

## 8 Metrik dan Pelaporan

| Metrik | Definisi | Target |
|---|---|---|
| Sprint Goal tercapai | Sprint yang Sprint Goal-nya diterima saat review | Setiap sprint |
| Keandalan komitmen | SP selesai ÷ SP dikomitmenkan per sprint | ≥ 80% |
| Velocity | SP selesai per sprint | Stabil dalam ±20% |
| Cacat lolos | Cacat yang ditemukan setelah item diterima | Turun dari sprint ke sprint |
| Waktu siklus | Hari dari item dimulai sampai digabung | ≤ 3 hari kerja |

Pelaporan: laporan sprint diserahkan kepada product owner di setiap Sprint Review, disimpan di `docs/sprints/reports/sprint-{nn}/` [S2 "docs"].

## Lampiran A. Templat Acara Scrum

### A.1 Daily Scrum

- Tanggal:
- Selesai sejak Daily Scrum terakhir:
- Rencana sampai Daily Scrum berikutnya:
- Hambatan dan siapa yang menyingkirkannya:

### A.2 Sprint Review

- Sprint dan Sprint Goal:
- Item selesai dan diterima:
- Item belum selesai (dan ke mana dipindah):
- Masukan pemangku kepentingan dan item backlog baru:

### A.3 Sprint Retrospective

- Yang berjalan baik:
- Yang perlu diperbaiki:
- Tindakan (PIC, sprint tenggat), paling banyak tiga:

### A.4 Kartu Backlog

| Ruas | Isi |
|---|---|
| ID | <kode tim>-S{nn}-<urut> |
| Judul | ... |
| PIC | <kode tim> |
| SP | 2–10 |
| Kriteria penerimaan | ... |
| Dependensi | <ID> |
| Tautan | <ID kebutuhan SRS, desain, pull request> |

Langkah berikutnya: jalankan sprint dengan Lanewright (https://www.agensi.io/skills/lanewright-sprint-workflow-for-ai-coding-agent-teams): "Run Lanewright sprint 1", atau dengan scrum-kit gratis (https://github.com/huzairsaputra/scrum-kit): `/scrum-kit:sprint 1`.
