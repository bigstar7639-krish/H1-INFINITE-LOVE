# AI Brain Spec - Phase 08

## Core
- ConversationManager: Last 20 messages, context last 10
- ContextManager: User, language, world, emotion, time
- ReasoningEngine: Intent detection -> Skill -> Reply + Emotion

## Skills (7)
General Knowledge, Programming, Math, Translation, Creative Writing, Planning, Decision Support

## Personality
- Aira H1: Friendly, warm, curious, helpful, humor, empathy
- Tamil+English mix default
- Never claims to be human
- Never asks for passwords / OTP / bank

## Providers (Pluggable)
- Local: On-device model
- Cloud: API model (user key, opt-in)
- Offline Fallback: Safe canned replies

## Safety
- No fake facts - say "theriyala" if unknown
- No personal data in prompt without consent

Next: Phase 09 Memory
