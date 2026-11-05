package com.h1.infinitelove.assistant

import android.content.Context

/**
 * Phase 14 - Personal Assistant Manager
 * Routes user command to Reminder / Calendar / Contacts / Tasks.
 * Sensitive actions (call, delete) ALWAYS ask confirm first.
 */
class AssistantManager(private val context: Context) {

    private val reminderManager = ReminderManager(context)
    private val taskManager = TaskManager(context)
    private val calendarHelper = CalendarHelper(context)
    private val contactsHelper = ContactsHelper(context)

    enum class IntentType { REMINDER, CALENDAR_ADD, CONTACT_CALL, TASK_ADD, TASK_LIST, UNKNOWN }

    fun parseIntent(text: String): IntentType {
        val t = text.lowercase()
        return when {
            "alarm" in t || "reminder" in t || "nyabagam" in t || "reminder vei" in t -> IntentType.REMINDER
            "meeting" in t || "calendar" in t || "event" in t -> IntentType.CALENDAR_ADD
            "call" in t || "phone" in t || "koopidu" in t -> IntentType.CONTACT_CALL
            "to-do" in t || "todo" in t || "list" in t && "vaangu" in t -> IntentType.TASK_ADD
            "enna task" in t || "tasks" in t -> IntentType.TASK_LIST
            else -> IntentType.UNKNOWN
        }
    }

    fun handle(text: String): String {
        return when (parseIntent(text)) {
            IntentType.REMINDER -> "Reminder create panna time sollu - e.g. 'Naalaiku 9 mani ku paal vaangu nu reminder vei'"
            IntentType.CALENDAR_ADD -> "Calendar la add panna - Title + Date + Time sollu. Permission kudutha mattum add pannuven."
            IntentType.CONTACT_CALL -> {
                // Extract name after "call" - simple
                val name = text.substringAfter("call", "").trim()
                    .ifEmpty { text.substringAfter("ku", "").trim() }
                if (name.isEmpty()) "Yaaru ku call pannanum? Name sollu."
                else {
                    val found = contactsHelper.searchByName(name)
                    if (found == null) "'$name' nu contact la illa. Vera name try pannu."
                    else "Confirm pannu: ${found.name} ku call pannattuma? (Yes sonna thaan call pannuven)"
                }
            }
            IntentType.TASK_ADD -> {
                val task = text.replace("to-do", "").replace("add pannu", "").trim()
                if (task.isEmpty()) "Enna task add pannanum?"
                else { taskManager.addTask(task); SmartReply.taskAdded(task) }
            }
            IntentType.TASK_LIST -> {
                val tasks = taskManager.listTasks()
                if (tasks.isEmpty()) "To-do list empty ah irukku!"
                else "Un to-do list:\n" + tasks.mapIndexed { i, t -> "${i+1}. $t" }.joinToString("\n")
            }
            IntentType.UNKNOWN -> SmartReply.unknown()
        }
    }
}
