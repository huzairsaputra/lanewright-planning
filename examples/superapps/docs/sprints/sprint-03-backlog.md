# Sprint 03 backlog

Sprint goal: Warga dapat mendaftar, memverifikasi surel, masuk, dan keluar di portal

Period: 30 November – 6 Desember 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S03-01 | Skema permohonan: `applications`, `application_values`, `application_documents`, `status_histories`, `audit_logs` | shared | shared-module-owner | 3 | Migrasi naik dan turun bersih; indeks unik `number`; status sesuai BR-01; struktur jejak audit NFR-06 |
| BE-1-S03-02 | API admin perangkat daerah: kelola layanan, formulir, persyaratan | api | module-dev | 5 | F-15 AC1–AC4; F-04 AC2; BR-05; NFR-06 (perubahan layanan tercatat) |
| FE-1-S03-01 | Layar daftar, verifikasi surel, masuk, keluar, atur ulang kata sandi | portal | module-dev | 5 | F-05 AC1–AC4; F-06 AC1–AC4; F-03 AC2 (kembali ke formulir setelah masuk) |
| FE-1-S03-02 | Beranda portal dan halaman pemberitahuan privasi | portal | module-dev | 3 | F-01: beranda menampilkan kategori dan kotak pencarian; NFR-05: pemberitahuan privasi tertaut dari formulir daftar |
| OPS-S03-01 | Uji fitur autentikasi dan otorisasi peran | tests | qa-test-engineer | 3 | F-05 AC1–AC4, F-06 AC1–AC4, NFR-02, NFR-03, BR-07 sebagai tes otomatis |

## Out of scope this sprint

- Layar admin layanan (FE-1-S04-01) — sprint 4
- API pengajuan permohonan (BE-1-S04-01) — sprint 4
- Lingkungan produksi (OPS-S04-01) — sprint 4

## Dependencies and risks

- FE-1-S03-01 butuh BE-1-S02-02 (sprint 2); OPS-S03-01 butuh BE-1-S02-01 dan BE-1-S02-02 (sprint 2) — selesai sebelumnya.
- Surel verifikasi butuh SMTP penyelenggara (A-04) — OPS memakai SMTP uji di staging sampai akses SMTP penyelenggara diberikan.
- Kapasitas sisa 11 SP (terutama OPS) tidak dapat dipakai untuk layar karena API-nya belum ada — dipakai untuk tinjauan kode dan perbaikan cacat.
