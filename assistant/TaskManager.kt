package com.h1.infinitelove.assistant

import android.content.Context
import org.json.JSONArray

/**
 * Phase 14 - To-Do / Task Manager
 * Stored locally in SharedPreferences JSON array.
 * No cloud, no upload.
 */
class TaskManager(private val context: Context) {
    private val prefs get() = context.getSharedPreferences("h1_tasks", Context.MODE_PRIVATE)
    fun addTask(task: String) {
        val list = listTasks().toMutableList()
        list.add(task)
        prefs.edit().putString("tasks", JSONArray(list).toString()).apply()
    }
    fun listTasks(): List<String> {
        val raw = prefs.getString("tasks", "[]") ?: "[]"
        return try {
            val arr = JSONArray(raw)
            (0 until arr.length()).map { arr.getString(it) }
        } catch (e: Exception) { emptyList() }
    }
    fun clearTasks() { prefs.edit().remove("tasks").apply() }
    fun removeTask(index: Int) {
        val list = listTasks().toMutableList()
        if (index in list.indices) { list.removeAt(index); prefs.edit().putString("tasks", JSONArray(list).toString()).apply() }
    }
}
