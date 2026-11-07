# Sprint 05 backlog

Sprint goal: Warga dapat mengajukan permohonan dengan formulir dan unggahan dokumen di portal

Period: 14 – 20 Desember 2026

| ID | Item | Region / module | Owner | SP | Acceptance criteria |
|---|---|---|---|---|---|
| BE-1-S05-01 | API antrean petugas per perangkat daerah | api | module-dev | 2 | F-12 AC1–AC3; BR-05 |
| BE-1-S05-02 | API keputusan petugas: verifikasi, minta perbaikan, setujui, tolak, dengan jejak audit | api | module-dev | 5 | F-13 AC1–AC5; BR-01; BR-04; NFR-06 |
| BE-1-S05-03 | API perbaikan oleh warga dan dokumen hasil / penyelesaian | api | module-dev | 3 | F-09 AC1–AC2; F-14 AC1–AC3; NFR-04 |
| FE-1-S05-01 | Layar pengajuan permohonan: formulir dinamis per layanan | portal | module-dev | 5 | F-08 AC1, AC2, AC4 |
| FE-1-S05-02 | Unggah dokumen persyaratan di layar pengajuan | portal | module-dev | 3 | F-08 AC2 (dokumen wajib), AC3 |
| OPS-S05-01 | Uji fitur pengajuan, unggahan, dan akses dokumen | tests | qa-test-engineer | 5 | F-08 AC1–AC4, F-10 AC1–AC3, NFR-04, BR-03, BR-06 sebagai tes otomatis |

## Out of scope this sprint

- Layar antrean petugas dan "Permohonan Saya" (FE-1-S06-01, FE-1-S06-02) — sprint 6
- Notifikasi perubahan status (BE-1-S06-01) — sprint 6

## Dependencies and risks

- FE-1-S05-01 dan FE-1-S05-02 butuh BE-1-S04-01 dan BE-1-S04-02 (sprint 4); OPS-S05-01 butuh BE-1-S04-01–03 (sprint 4) — selesai sebelumnya.
- Alur status BR-01 masih asumsi (A-14, OQ-14) — product owner mengonfirmasinya sebelum sprint 5 dimulai; perubahan sesudahnya masuk backlog.
