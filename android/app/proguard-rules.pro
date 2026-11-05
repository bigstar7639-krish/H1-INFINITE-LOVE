# H1 Infinite Love — ProGuard / R8 rules
# Keep foundation classes during early development

-keep class com.h1infinitelove.** { *; }

# Future: tighten rules once release builds are stable
