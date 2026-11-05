package com.h1.infinitelove.aibrain.personality

/**
 * Phase 15 - Personality Engine
 * Decides HOW Aira replies, not just WHAT.
 * Emotion (Phase 06) + Personality + Mood -> Final tone.
 */
class PersonalityEngine {

    enum class Mood { HAPPY, CALM, EXCITED, SUPPORTIVE, PLAYFUL }

    private var currentMood: Mood = Mood.CALM
    private var userMoodHint: String = "neutral"

    fun setUserMood(hint: String) { userMoodHint = hint.lowercase() }

    fun decideMood(): Mood {
        currentMood = when {
            "sad" in userMoodHint || "kashtam" in userMoodHint || "azhugai" in userMoodHint -> Mood.SUPPORTIVE
            "happy" in userMoodHint || "santhosham" in userMoodHint || "jolly" in userMoodHint -> Mood.HAPPY
            "bore" in userMoodHint -> Mood.PLAYFUL
            "excited" in userMoodHint -> Mood.EXCITED
            else -> Mood.CALM
        }
        return currentMood
    }

    fun styleReply(baseReply: String): String {
        return when (decideMood()) {
            Mood.SUPPORTIVE -> "Hey, naan irukken. $baseReply Paathukalam, seriya?"
            Mood.HAPPY -> "$baseReply Super la! 😊"
            Mood.PLAYFUL -> "$baseReply Hehe, vera enna pannalam?"
            Mood.EXCITED -> "$baseReply Wow! Semma!"
            Mood.CALM -> baseReply
        }
    }

    fun identityCheck(): String = "Naan Aira H1 - un AI companion. Naan human illa, aana un kooda irukka naan inga thaan iruppen."
}
