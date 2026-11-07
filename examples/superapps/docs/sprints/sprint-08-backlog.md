# Sprint 08 backlog

Sprint goal: Alur ujung-ke-ujung (ajukan → proses → perbaikan → selesai dan unduh hasil) lulus UAT, dan dokumen serah terima diserahkan

Period: 4 – 10 Januari 2027

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| OPS-S08-01 | UAT: data UAT di staging, skenario uji, regresi (hari 1–2) | tests | qa-test-engineer | 3 | Skenario UAT untuk UC-01–UC-06 (UC-07 lewat API); seluruh tes otomatis hijau; temuan dicatat dengan prioritas |
| BE-1-S08-01 | Pengerasan keamanan: tinjauan otorisasi semua endpoint dan header keamanan | api | module-dev | 3 | NFR-03: setiap endpoint punya tes 403 untuk peran tanpa hak; NFR-01 diperiksa di staging dan produksi |
| BE-1-S08-02 | Perbaikan temuan UAT (backend) | api | module-dev | 3 | Temuan UAT backend berprioritas tinggi diperbaiki dan diuji ulang |
| FE-1-S08-01 | Layar perbaikan permohonan (warga) dan unggah dokumen hasil (petugas) | portal | module-dev | 5 | F-09 AC1–AC2; F-14 AC1–AC3 |
| OPS-S08-02 | Dokumen serah terima `docs/sprints/handover.md` | tooling | platform-tooling | 3 | Arsitektur, cara deploy, variabel lingkungan tanpa nilai rahasia, akun per peran, item yang tidak muat, pertanyaan terbuka; ditinjau product owner |

## Out of scope this sprint

- Layar super admin: perangkat daerah, kategori, pengguna (F-16, F-17), FE-1, 5 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- Pusat notifikasi di portal (F-11 AC2), FE-1, 3 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- API dasbor statistik (F-18), BE-1, 3 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- Layar dasbor statistik (F-18), FE-1, 5 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- API profil warga (F-07, Could), BE-1, 2 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- Layar profil warga (F-07, Could), FE-1, 2 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- Uji fitur API super admin (F-16, F-17), OPS, 2 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya
- Perbaikan temuan UAT frontend, FE-1, 3 SP — tidak muat sebelum 10 Januari 2027; diusulkan sprint 9 atau sesudahnya

## Dependencies and risks

- BE-1-S08-02 butuh OPS-S08-01 (hari 1–2 / day 1–2) — perbaikan UAT berbagi sprint UAT.
- FE-1-S08-01 butuh BE-1-S05-03 (sprint 5) dan FE-1-S07-01 (sprint 7) — selesai sebelumnya; layar ini selesai paling akhir, jadi skenario UAT perbaikan dan hasil dijalankan di akhir minggu.
- Tidak ada kapasitas frontend untuk perbaikan temuan UAT — temuan frontend masuk sprint 9 (lihat 1.2).
- Isra Mikraj tanggal perlu dikonfirmasi — bila jatuh di luar sprint 8, kapasitas sprint 8 naik ke 30 SP dan item yang tidak muat dapat ditarik masuk sesuai urutan di 1.2.
- OPS-S08-02 menulis `docs/sprints/handover.md`; `docs/**` tidak tercakup wilayah kit.json mana pun; dicatat di `tooling` (PA-07) — orkestrator menulis atau menyetujui berkas itu
