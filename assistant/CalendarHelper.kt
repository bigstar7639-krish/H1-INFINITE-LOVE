package com.h1.infinitelove.assistant

import android.content.ContentValues
import android.content.Context
import android.provider.CalendarContract

/**
 * Phase 14 - Calendar Helper
 * Requires READ_CALENDAR + WRITE_CALENDAR runtime permission.
 * If permission denied -> return false, UI says "Permission illa".
 * Never silently fake success.
 */
class CalendarHelper(private val context: Context) {

    fun addEvent(title: String, startMillis: Long, endMillis: Long, description: String = ""): Boolean {
        return try {
            val values = ContentValues().apply {
                put(CalendarContract.Events.TITLE, title)
                put(CalendarContract.Events.DTSTART, startMillis)
                put(CalendarContract.Events.DTEND, endMillis)
                put(CalendarContract.Events.DESCRIPTION, description)
                put(CalendarContract.Events.CALENDAR_ID, 1)
                put(CalendarContract.Events.EVENT_TIMEZONE, java.util.TimeZone.getDefault().id)
            }
            val uri = context.contentResolver.insert(CalendarContract.Events.CONTENT_URI, values)
            uri != null
        } catch (e: SecurityException) { false }
        catch (e: Exception) { false }
    }

    fun listUpcoming(limit: Int = 5): List<String> {
        // Real query needs permission - return empty if fails, never fake
        return try {
            val projection = arrayOf(CalendarContract.Events.TITLE, CalendarContract.Events.DTSTART)
            val cursor = context.contentResolver.query(
                CalendarContract.Events.CONTENT_URI, projection, null, null,
                "${CalendarContract.Events.DTSTART} ASC"
            ) ?: return emptyList()
            val list = mutableListOf<String>()
            cursor.use {
                val titleIdx = it.getColumnIndex(CalendarContract.Events.TITLE)
                while (it.moveToNext() && list.size < limit) {
                    list.add(it.getString(titleIdx) ?: "Untitled")
                }
            }
            list
        } catch (e: Exception) { emptyList() }
    }
}
