---
contract: atlas-content/0.1
id: model:id:rekurensi-koreksi-tertunda
work: work:delayed-correction-recurrence
type: model
title: Rekurensi koreksi tertunda
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: id
translation_of: model:en:delayed-correction-recurrence
translation:
  source_revision: 1
  method: human-assisted
staleness: current
purpose: Menunjukkan bagaimana penundaan satu langkah mengubah rekurensi umpan balik korektif sederhana.
formal_structure: x[t+1] = x[t] - k*x[t-d]
inputs:
  - riwayat keadaan
outputs:
  - keadaan berikutnya
parameters:
  - penguatan k
  - penundaan d
assumptions:
  - waktu diskret
  - keadaan skalar
  - koreksi linear
  - penguatan dan penundaan tetap
  - aritmetika eksak
  - tanpa noise, saturasi, atau masukan eksternal
validation:
  - perhitungan manual dan unit test untuk k=1, d=1, x0=1, x1=0
failure_modes:
  - dinamika nonlinear atau multidimensi
  - parameter berubah
  - saturasi atau kontrol terbatas
  - penundaan pengukuran berbeda dari penundaan aktuasi
  - masukan eksternal atau noise
---

Model ini sengaja cukup sederhana untuk dihitung ulang secara manual. Model menunjukkan satu mekanisme, bukan hukum umum semua sistem tertunda.
