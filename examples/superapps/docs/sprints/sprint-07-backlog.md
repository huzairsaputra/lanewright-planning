# Sprint 07 backlog

Sprint goal: Petugas dapat memverifikasi, meminta perbaikan, menyetujui, atau menolak permohonan di portal

Period: 28 Desember 2026 – 3 Januari 2027

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S07-01 | API super admin: perangkat daerah, kategori, pengguna, dan peran | api | module-dev | 5 | F-16 AC1–AC3; F-17 AC1–AC3; NFR-03; NFR-06 |
| FE-1-S07-01 | Layar keputusan petugas: verifikasi, minta perbaikan, setujui, tolak | portal | module-dev | 5 | F-13 AC1–AC4 |
| OPS-S07-01 | Uji fitur notifikasi | tests | qa-test-engineer | 2 | F-11 AC1–AC3 sebagai tes otomatis (surel dipalsukan) |
| OPS-S07-02 | Uji peramban alur warga: katalog, daftar, ajukan (`portal/tests`) | tests | qa-test-engineer | 3 | F-01 AC1, F-05 AC1, F-08 AC1 lewat peramban otomatis di CI |

## Out of scope this sprint

- Layar perbaikan permohonan dan dokumen hasil (FE-1-S08-01) — sprint 8
- Layar super admin (F-16, F-17) — tidak muat sebelum 10 Januari 2027 (sprint 9 atau sesudahnya)

## Dependencies and risks

- FE-1-S07-01 butuh BE-1-S05-02 (sprint 5) dan FE-1-S06-01 (sprint 6); OPS-S07-01 butuh BE-1-S06-01 (sprint 6); OPS-S07-02 butuh FE-1-S02-01–FE-1-S05-02 — selesai sebelumnya.
- Layar super admin tidak muat sebelum tanggal akhir (lihat 1.2) — sampai sprint 9, perangkat daerah dan akun dibuat lewat seeder atau API.
