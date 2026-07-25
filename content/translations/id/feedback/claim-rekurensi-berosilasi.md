---
contract: atlas-content/0.1
id: claim:id:rekurensi-tertunda-yang-dinyatakan-berosilasi
work: work:stated-delayed-recurrence-oscillates
type: claim
title: Rekurensi tertunda yang dinyatakan memiliki urutan berosilasi
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: id
translation_of: claim:en:stated-delayed-recurrence-oscillates
translation:
  source_revision: 1
  method: human-assisted
staleness: current
claim:
  kind: model-derived
  statement: Untuk x[t+1] = x[t] - x[t-1] dengan x0 = 1 dan x1 = 0, keadaan awal membentuk urutan berulang 1, 0, -1, -1, 0, 1, 1, 0.
  scope:
    model: model:id:rekurensi-koreksi-tertunda
    gain: 1
    delay_steps: 1
    initial_state:
      x0: 1
      x1: 0
  confidence: strongly-supported
model: model:id:rekurensi-koreksi-tertunda
confidence_rationale: Hasil mengikuti aritmetika langsung dan dihitung ulang oleh unit test validator.
limitations:
  - keyakinan hanya berlaku untuk rekurensi, parameter, nilai awal, dan aritmetika eksak yang dinyatakan
---

Klaim ini bersifat formal dan dapat direproduksi. Klaim ini bukan bukti empiris bahwa suatu sistem nyata berosilasi.
