---
contract: atlas-content/0.1
id: evidence:id:urutan-periodik-umpan-balik-tertunda
work: work:delayed-feedback-periodic-sequence
type: evidence
title: Urutan periodik yang dihasilkan oleh rekurensi koreksi tertunda
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: id
translation_of: evidence:en:delayed-feedback-periodic-sequence
translation:
  source_revision: 1
  method: human-assisted
staleness: current
source: src:synthetic-feedback-run-delay-one-gain-one
locator:
  kind: generated-sequence
  value: k=1; d=1; x0=1; x1=0; delapan keadaan pertama
access:
  class: open
transformation:
  procedure: model:id:rekurensi-koreksi-tertunda
  inputs:
    - x0=1
    - x1=0
    - k=1
    - d=1
  parameters:
    steps: 8
measurement:
  quantity: state-sequence
  values:
    - value: 1
      unit: unitless
    - value: 0
      unit: unitless
    - value: -1
      unit: unitless
    - value: -1
      unit: unitless
    - value: 0
      unit: unitless
    - value: 1
      unit: unitless
    - value: 1
      unit: unitless
    - value: 0
      unit: unitless
relations:
  - type: supports
    target: claim:id:rekurensi-tertunda-yang-dinyatakan-berosilasi
    note: Substitusi langsung ke rekurensi menghasilkan urutan berulang untuk parameter yang dinyatakan.
  - type: derived-from
    target: model:id:rekurensi-koreksi-tertunda
    note: Urutan dihasilkan melalui penerapan model secara berulang.
---

Terapkan `x[t+1] = x[t] - x[t-1]` berulang kali mulai dari `x0 = 1` dan `x1 = 0`. Unit test repositori menghitung ulang urutan ini secara independen.
