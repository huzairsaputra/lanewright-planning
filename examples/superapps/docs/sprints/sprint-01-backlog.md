# Sprint 01 backlog

Sprint goal: Kerangka Laravel berjalan di staging dengan CI hijau, dan API katalog mengembalikan layanan contoh

Period: 16 – 22 November 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| OPS-S01-01 | Kerangka Laravel, struktur modul `portal` dan `api`, branch `staging`/`main` (hari 1–2) | tooling | platform-tooling | 2 | Fondasi; aplikasi Laravel lulus `php artisan test`; direktori `portal/`, `api/`, `database/` sesuai kit.json; branch `staging` dibuat; README cara menjalankan lokal |
| OPS-S01-02 | CI GitHub Actions: lint (Pint) dan `php artisan test` di setiap pull request | tooling | platform-tooling | 3 | NFR-08: pull request ke `staging`/`main` menjalankan lint dan tes; pull request dengan tes gagal tidak dapat digabung |
| OPS-S01-03 | Lingkungan staging, penanganan rahasia, deploy otomatis dari `staging` | tooling | platform-tooling | 5 | Fondasi (A-10); penggabungan ke `staging` men-deploy otomatis; `.env` tidak ada di repositori; rahasia di GitHub Secrets; migrasi berjalan saat deploy |
| BE-1-S01-01 | Konvensi dan kontrak API: `/api/v1`, format respons dan galat JSON, OpenAPI (hari 1–2) | api | module-dev | 2 | Fondasi; format sukses dan galat seragam terdokumentasi; galat validasi → HTTP 422 dengan daftar field; OpenAPI di repositori |
| BE-1-S01-02 | Skema inti dan seeder: `users`, `roles`, `units`, `categories`, `services` | shared | shared-module-owner | 5 | Fondasi (A-09); migrasi naik dan turun bersih; seeder: 4 peran, 1 super admin dari variabel lingkungan (tanpa kata sandi di repositori), 2 unit, 3 kategori, 5 layanan contoh |
| BE-1-S01-03 | API katalog: daftar, pencarian, filter, detail layanan | api | module-dev | 3 | F-01 AC1–AC3; F-02 AC1–AC3; data untuk F-03 AC1 dan F-04 AC1; hanya layanan aktif |
| FE-1-S01-01 | Kerangka portal: tata letak responsif, navigasi, teks Bahasa Indonesia, klien API | portal | module-dev | 5 | NFR-07; NFR-09 (target perlu dikonfirmasi, OQ-23); klien API memakai format galat BE-1-S01-01 |
| FE-1-S01-02 | Komponen antarmuka dasar: formulir, tabel, unggah berkas, pesan galat dan sukses | portal | module-dev | 3 | Fondasi; galat HTTP 422 tampil di bawah field terkait; halaman contoh komponen |

## Out of scope this sprint

- Layar katalog dan detail (FE-1-S02-01, FE-1-S02-02) — sprint 2, karena butuh API katalog dari sprint ini
- Otorisasi peran dan API autentikasi (BE-1-S02-01, BE-1-S02-02) — sprint 2
- HTTPS wajib di staging (OPS-S02-01) — sprint 2

## Dependencies and risks

- BE-1-S01-01, BE-1-S01-02 dan FE-1-S01-01 butuh OPS-S01-01 (hari 1–2 / day 1–2) — OPS menyelesaikan kerangka pada hari 1.
- FE-1-S01-01 butuh BE-1-S01-01 (hari 1–2 / day 1–2) — kontrak API disepakati pada hari 2.
- Server staging belum tentu tersedia (A-10) — OPS meminta akses pada hari 1; bila belum ada, staging sementara di server tim dan dicatat di tinjauan.
- OPS-S01-01 menyentuh berkas akar Laravel (`composer.json`, `config/`, `routes/`, `artisan`) yang tidak tercakup wilayah kit.json mana pun; dicatat di `tooling` (PA-07) — pemilik platform memutuskan wilayahnya sebelum sprint dimulai
