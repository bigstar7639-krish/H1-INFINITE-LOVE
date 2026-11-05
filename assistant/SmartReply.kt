package com.h1.infinitelove.assistant

/** Phase 14 - Assistant replies - Tamil+English mix, warm */
object SmartReply {
    fun taskAdded(task: String) = "Okay! '$task' nu to-do la add panniten. Marakka maaten!"
    fun unknown() = "Hmm, athu enaku puriyala. 'Reminder vei', 'Meeting add pannu', 'Amma ku call pannu' nu try pannu - naa help pannuven!"
    fun reminderSet(title: String) = "Reminder set panniten: $title. Time aachu na naan nyabagam paduthuven!"
    fun permissionNeeded(what: String) = "$what ku permission illa. Settings la permission kudutha naan panniduven!"
}
