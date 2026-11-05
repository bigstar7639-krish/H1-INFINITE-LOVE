package com.h1.infinitelove.assistant

import android.content.Context
import android.provider.ContactsContract

/**
 * Phase 14 - Contacts Helper
 * Search only, never upload contacts.
 * Needs READ_CONTACTS permission.
 */
data class ContactInfo(val name: String, val phone: String)

class ContactsHelper(private val context: Context) {
    fun searchByName(query: String): ContactInfo? {
        return try {
            val uri = ContactsContract.CommonDataKinds.Phone.CONTENT_URI
            val projection = arrayOf(
                ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME,
                ContactsContract.CommonDataKinds.Phone.NUMBER
            )
            val selection = "${ContactsContract.CommonDataKinds.Phone.DISPLAY_NAME} LIKE ?"
            val args = arrayOf("%$query%")
            val cursor = context.contentResolver.query(uri, projection, selection, args, null) ?: return null
            cursor.use {
                if (it.moveToFirst()) {
                    val name = it.getString(0) ?: return null
                    val phone = it.getString(1) ?: ""
                    return ContactInfo(name, phone)
                }
            }
            null
        } catch (e: Exception) { null }
    }
}
