# Sprint 04 backlog

Sprint goal: Admin perangkat daerah dapat membuat dan mengaktifkan layanan beserta formulirnya; lingkungan produksi siap

Period: 7 – 13 Desember 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S04-01 | API pengajuan permohonan: isi formulir, kirim, nomor unik | api | module-dev | 5 | F-08 AC1, AC2, AC4; BR-02; BR-03; BR-07 |
| BE-1-S04-02 | Unggah dokumen persyaratan ke penyimpanan privat dan unduh berhak | api | module-dev | 3 | F-08 AC3; NFR-04; BR-06 |
| BE-1-S04-03 | API "Permohonan Saya": daftar dan riwayat status | api | module-dev | 2 | F-10 AC1–AC3; BR-06 |
| FE-1-S04-01 | Layar admin perangkat daerah: kelola layanan, formulir, persyaratan | portal | module-dev | 8 | F-15 AC1–AC4; F-04 AC2 |
| OPS-S04-01 | Lingkungan produksi dan deploy dari `main` | tooling | platform-tooling | 5 | A-10; penggabungan ke `main` men-deploy ke produksi setelah persetujuan manual; HTTPS dan header sama dengan staging (NFR-01); rahasia terpisah dari staging |
| OPS-S04-02 | Uji fitur API admin layanan | tests | qa-test-engineer | 3 | F-15 AC1–AC4, F-04 AC2, BR-05 sebagai tes otomatis |

## Out of scope this sprint

- Layar pengajuan permohonan (FE-1-S05-01, FE-1-S05-02) — sprint 5
- API antrean, keputusan, dan perbaikan (BE-1-S05-01–BE-1-S05-03) — sprint 5

## Dependencies and risks

- FE-1-S04-01 dan OPS-S04-02 butuh BE-1-S03-02 (sprint 3) — selesai sebelumnya.
- Server produksi penyelenggara belum pasti (A-10, OQ-10) — keputusan hosting dibutuhkan sebelum sprint 4; bila belum ada, OPS-S04-01 pindah ke sprint berikutnya yang punya kapasitas OPS.
- Batas ukuran unggahan belum ditetapkan (OQ-21) — BE-1 memakai batas yang dapat dikonfigurasi lewat variabel lingkungan.
