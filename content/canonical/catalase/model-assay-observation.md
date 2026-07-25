---
contract: atlas-content/0.1
id: model:en:catalase-assay-observation
work: work:catalase-assay-observation
type: model
title: Catalase assay observation model
status: draft
revision: 1
created: 2026-07-26
updated: 2026-07-26
language: en
purpose: Separate catalytic activity from the signal or proxy recorded by an assay.
inputs:
  - enzyme source and amount
  - hydrogen-peroxide concentration
  - pH
  - temperature and exposure duration
  - mixing and vessel geometry
outputs:
  - measured assay signal
  - inferred activity within the calibrated range
parameters:
  - assay calibration
  - observation interval
assumptions:
  - the selected signal changes predictably with reaction progress in the stated range
  - interfering reactions are bounded or measured
validation:
  - compare against a documented calibration or reference method
failure_modes:
  - substrate depletion
  - gas escape or foam instability
  - unequal tissue surface area
  - fluorescence interference
  - temperature drift
---

The model is deliberately method-neutral. Absorbance, fluorescence, oxygen evolution, and foam height are not interchangeable without calibration and scope.
