---
contract: atlas-content/0.1
id: synthesis:id:umpan-balik-tertunda-dan-osilasi
work: work:delayed-feedback-and-oscillation
type: synthesis
title: Rekurensi korektif tertunda dapat berosilasi dalam asumsi yang dinyatakan
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: id
translation_of: synthesis:en:delayed-feedback-and-oscillation
translation:
  source_revision: 1
  method: human-assisted
staleness: current
question: question:id:kapan-koreksi-tertunda-dapat-berosilasi
claims:
  - claim:id:rekurensi-tertunda-yang-dinyatakan-berosilasi
  - claim:id:osilasi-model-tidak-membuktikan-osilasi-sistem-nyata
models:
  - model:id:rekurensi-koreksi-tertunda
evidence_selection: Gunakan referensi umpan balik untuk istilah dan urutan hasil model yang dapat direproduksi untuk rekurensi eksak; jangan memperlakukan keluaran model sebagai observasi empiris.
conclusion: Rekurensi korektif tertunda satu langkah yang dinyatakan menghasilkan urutan berulang untuk penguatan dan nilai awal yang ditentukan. Hasil ini menunjukkan satu mekanisme yang dapat menghasilkan perilaku berosilasi, tetapi penerapannya pada sistem nyata memerlukan bukti terpisah tentang kecocokan model.
confidence: well-supported
confidence_rationale: Urutan formal dapat dihitung ulang secara tepat, sedangkan interpretasi yang lebih luas dibatasi sebagai aturan metodologis.
disagreements:
  - penguatan, penundaan, nonlinearity, dan definisi stabilitas lain dapat menghasilkan perilaku berbeda
open_questions:
  - apakah ekspresi formal memerlukan subtipe kontrak tersendiri?
  - definisi stabilitas mana yang sesuai untuk tiap kelas model?
revision_triggers:
  - fixture aritmetika berubah
  - rekurensi atau asumsi berubah
  - kontrak ekspresi formal diperkenalkan
---

## Jalur provenance

Pertanyaan → sumber synthetic run → evidence urutan periodik → claim turunan model → model dan concept → synthesis ini.

## Batas inferensi

Urutan eksak bukan bukti bahwa penundaan selalu membuat umpan balik tidak stabil atau bahwa setiap osilasi dunia nyata memiliki mekanisme ini.
