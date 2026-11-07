# Sprint 02 backlog

Sprint goal: Pengunjung dapat menjelajah, mencari, dan membuka detail layanan di portal staging

Period: 23 – 29 November 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| OPS-S02-01 | HTTPS wajib dan header keamanan di staging | tooling | platform-tooling | 2 | NFR-01: permintaan HTTP dialihkan ke HTTPS; header HSTS terkirim; cookie sesi bertanda Secure |
| OPS-S02-02 | Uji fitur API katalog (`api/tests`) | tests | qa-test-engineer | 3 | F-01 AC1–AC3 dan F-02 AC1–AC3 sebagai tes otomatis yang berjalan di CI |
| BE-1-S02-01 | Otorisasi berbasis peran: middleware dan policy | api | module-dev | 3 | NFR-03: akses di luar hak peran → HTTP 403; policy BR-05 dan BR-06 siap dipakai endpoint berikutnya |
| BE-1-S02-02 | API autentikasi: daftar dengan persetujuan PDP, verifikasi surel, masuk, keluar, atur ulang kata sandi | api | module-dev | 5 | F-05 AC1–AC4; F-06 AC1–AC4; NFR-02; NFR-05 (waktu persetujuan tersimpan); BR-07 |
| BE-1-S02-03 | Skema formulir dan persyaratan: `service_fields`, `service_requirements` | shared | shared-module-owner | 2 | Migrasi naik dan turun bersih; jenis isian teks, angka, tanggal, pilihan (F-15 AC4); jenis berkas yang diizinkan per persyaratan |
| FE-1-S02-01 | Halaman katalog dan pencarian | portal | module-dev | 5 | F-01 AC1–AC3; F-02 AC1–AC3 |
| FE-1-S02-02 | Halaman detail layanan dan tautan aplikasi lain | portal | module-dev | 3 | F-03 AC1; F-04 AC1; BR-02; tombol "Ajukan Permohonan" tampil (pengalihan masuk F-03 AC2 di FE-1-S03-01) |

## Out of scope this sprint

- Layar daftar, masuk, dan atur ulang kata sandi (FE-1-S03-01) — sprint 3
- API admin layanan (BE-1-S03-02) — sprint 3

## Dependencies and risks

- FE-1-S02-01 dan FE-1-S02-02 butuh BE-1-S01-03 (sprint 1) — sudah selesai sebelumnya.
- Teks pemberitahuan privasi untuk persetujuan PDP belum ada (OQ-05) — BE-1 memakai teks sementara; product owner memberi teks final sebelum sprint 3.
