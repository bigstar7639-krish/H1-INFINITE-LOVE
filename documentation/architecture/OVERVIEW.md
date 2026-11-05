# H1 Infinite Love — Architecture Overview

## High-level design

H1 Infinite Love is built as a modular monolith on Android with a clear separation of concerns.

```
┌─────────────────────────────────────────────────────────────┐
│                        Android App                          │
│  ┌─────────────┐  ┌──────────────┐  ┌───────────────────┐  │
│  │ MainActivity│  │  Full-screen │  │ Floating Overlay  │  │
│  │  (Control)  │  │  3D World    │  │   (SYSTEM_ALERT)  │  │
│  └─────────────┘  └──────────────┘  └───────────────────┘  │
│           │                │                   │            │
│           └────────────────┼───────────────────┘            │
│                            ▼                                │
│  ┌─────────────────────────────────────────────────────┐   │
│  │              Module Bridge / Integration Layer       │   │
│  └─────────────────────────────────────────────────────┘   │
│       │         │         │         │         │            │
│       ▼         ▼         ▼         ▼         ▼            │
│  Character  Animation  Emotions   Voice     AI-Brain       │
│  Vision     Memory     Assistant  Security  Storage        │
└─────────────────────────────────────────────────────────────┘
                              │
                              ▼
                     Website (React + Three.js)
                     (optional remote control / web companion)
```

## Key principles

1. **Floating character is first-class** — real system overlay, not an in-app mini window.
2. **Emotion drives everything** — face, body, voice, conversation style, animation transitions.
3. **Modular AI** — providers can be swapped (cloud today, local later).
4. **Privacy by design** — encrypted storage, user-controlled memory, clear permission indicators.
5. **Original character** — no copyrighted designs.

## Technology choices (Phase 02)

| Layer            | Choice                          | Reason                                      |
|------------------|---------------------------------|---------------------------------------------|
| Language         | Kotlin                          | Official Android language, modern, safe     |
| UI               | Material 3 + ViewBinding        | Solid foundation, easy to evolve            |
| Overlay          | SYSTEM_ALERT_WINDOW + FGS       | Legitimate, required for true floating UX   |
| Storage (future) | Room + SQLCipher                | Structured + encrypted                      |
| 3D (future)      | GLB/VRM + Filament / custom     | Performance on mobile                       |
| Web              | React + Three.js                | Fast companion site                         |
| CI               | GitHub Actions                  | Works from Termux + Git workflow            |
