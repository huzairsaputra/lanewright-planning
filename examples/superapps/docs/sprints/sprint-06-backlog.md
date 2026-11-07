# Sprint 06 backlog

Sprint goal: Petugas melihat antrean unitnya, warga memantau permohonannya, dan surel notifikasi terkirim saat status berubah

Period: 21 – 27 Desember 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S06-01 | Notifikasi perubahan status: di portal (API) dan surel lewat antrean | api | module-dev | 5 | F-11 AC1–AC3 (API daftar notifikasi dan jumlah belum dibaca); SMTP penyelenggara (A-04) |
| FE-1-S06-01 | Layar antrean dan detail permohonan untuk petugas | portal | module-dev | 3 | F-12 AC1–AC3 |
| FE-1-S06-02 | Layar "Permohonan Saya" dan riwayat status | portal | module-dev | 3 | F-10 AC1–AC3 |
| OPS-S06-01 | Uji fitur alur petugas, transisi status, dan jejak audit | tests | qa-test-engineer | 5 | F-12 AC1–AC3, F-13 AC1–AC5, F-09 AC1–AC2, F-14 AC1–AC3, BR-01, BR-04, BR-05, NFR-06 sebagai tes otomatis |

## Out of scope this sprint

- Layar keputusan petugas (FE-1-S07-01) — sprint 7
- API super admin (BE-1-S07-01) — sprint 7
- Pusat notifikasi di portal (F-11 AC2) — tidak muat sebelum 10 Januari 2027 (sprint 9 atau sesudahnya)

## Dependencies and risks

- FE-1-S06-01 butuh BE-1-S05-01 (sprint 5); FE-1-S06-02 butuh BE-1-S04-03 (sprint 4); OPS-S06-01 butuh BE-1-S05-01–03 (sprint 5) — selesai sebelumnya.
- Minggu libur Natal; cuti bersama tanggal perlu dikonfirmasi — bila hari kerja tinggal 3, item tetap muat karena kapasitas sudah dihitung 6 SP per orang.
