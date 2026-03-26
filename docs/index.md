---
layout: home

hero:
  name: Fullstack Template
  text: Opinionated FastAPI + Vue baseline
  tagline: Contract-first, ADR-driven, observable, and strict by default.
  actions:
    - theme: brand
      text: Get Started
      link: /getting-started
    - theme: alt
      text: Template Overview
      link: /overview
    - theme: alt
      text: ADR Reading Map
      link: /adr/INDEX

features:
  - title: Contract Parity
    details: OpenAPI remains the source of truth and parity is checked across spec, backend runtime, and frontend bindings.
  - title: Strong Architecture
    details: Backend bounded contexts, frontend layered structure, import boundaries, and ADR-driven governance are enforced in automation.
  - title: Observability Baseline
    details: Backend and frontend both ship structured observability primitives instead of leaving telemetry as a future concern.
  - title: Real Developer Workflow
    details: Make targets, local hooks, Docker compose, pytest-alembic, generated frontend API, and CI symmetry already exist in the baseline.
---

## What This Site Covers

<div class="template-grid">
  <a class="template-card" href="./overview">
    <strong>Template Overview</strong>
    <span>Scope, baseline, source of truth, reference slice, and what derived projects must customize.</span>
  </a>
  <a class="template-card" href="./getting-started">
    <strong>Getting Started</strong>
    <span>Fast-path onboarding for local setup, runtime modes, checks, and bounded-context growth.</span>
  </a>
  <a class="template-card" href="./template/PHILOSOPHY">
    <strong>Template Philosophy</strong>
    <span>Why this repository is intentionally strict and why validation is treated as architecture.</span>
  </a>
  <a class="template-card" href="./frontend/ui-layer">
    <strong>Frontend UI Layer</strong>
    <span>Adapter-oriented UI boundary, migration rules, and the intended primitive discipline.</span>
  </a>
</div>

## Architecture And Governance

<div class="template-shell">
  <p class="template-eyebrow">Reading map</p>
  <h2>Every architecture decision is already documented and linked.</h2>
  <p>
    The ADR catalog is split into architecture, product-reference, and engineering
    decisions. The public entrypoint is the ADR reading map, not a loose folder of
    markdown files.
  </p>
  <div class="template-grid template-grid--tight">
    <a class="template-card" href="./adr/INDEX">
      <strong>ADR Reading Map</strong>
      <span>Mandatory entrypoint before touching architecture, runtime, contracts, CI, or governance.</span>
    </a>
    <a class="template-card" href="./adr/architecture/README">
      <strong>Architecture ADRs</strong>
      <span>Repository layout, platform runtime, testing model, observability, and dependency direction.</span>
    </a>
    <a class="template-card" href="./adr/engineering/README">
      <strong>Engineering ADRs</strong>
      <span>Template metadata, self-consistency checks, CI symmetry, and repository governance.</span>
    </a>
    <a class="template-card" href="./adr/product/README">
      <strong>Reference Product ADRs</strong>
      <span>Example domain decisions for derived projects, not a claim that this repo is already a product.</span>
    </a>
  </div>
</div>

## Baseline, Not Product

<div class="template-grid">
  <div class="template-panel">
    <p class="template-eyebrow">Already implemented</p>
    <ul>
      <li>FastAPI backend with bounded contexts, typed settings, explicit Unit of Work, Alembic, and observability.</li>
      <li>Vue frontend with app/pages/features/entities/shared structure, shell routing, and generated OpenAPI bindings.</li>
      <li>Contract parity checks, ADR validation, repository consistency checks, Docker builds, and local CI-grade hooks.</li>
      <li>One canonical cross-stack reference slice for system health.</li>
    </ul>
  </div>
  <div class="template-panel">
    <p class="template-eyebrow">Intentionally not productized</p>
    <ul>
      <li>No business-specific product surface beyond the reference slice.</li>
      <li>No pretense that the homepage or ADRs describe a fully implemented commercial platform.</li>
      <li>No relaxed validation path hidden behind convenience switches.</li>
      <li>No generated-project magic that weakens source-of-truth ownership.</li>
    </ul>
  </div>
</div>

## Primary Links

<div class="template-grid template-grid--tight">
  <a class="template-card" href="https://github.com/Mesteriis/fullstack-template">
    <strong>Repository</strong>
    <span>Browse the source, workflows, and release history on GitHub.</span>
  </a>
  <a class="template-card" href="https://github.com/Mesteriis/fullstack-template/releases/tag/v0.1.0">
    <strong>Baseline Release</strong>
    <span>The first tagged reusable baseline for derived projects.</span>
  </a>
  <a class="template-card" href="https://github.com/Mesteriis/fullstack-template/blob/main/specs/openapi/platform.openapi.yaml">
    <strong>Canonical OpenAPI</strong>
    <span>The public HTTP source of truth used for parity checks and generated frontend API bindings.</span>
  </a>
</div>
