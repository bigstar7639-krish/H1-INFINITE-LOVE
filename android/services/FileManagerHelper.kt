package com.h1.infinitelove.services

import android.content.Context
import android.os.Environment
import java.io.File

/**
 * Phase 13 - File Management Helper
 * Access ONLY user-selected folders / Download / H1 folder.
 * No access to other apps private data.
 */
object FileManagerHelper {
    fun listH1Files(context: Context): List<File> {
        val dir = File(Environment.getExternalStorageDirectory(), "Download/H1-INFINITE-LOVE")
        if (!dir.exists()) return emptyList()
        return dir.listFiles()?.toList() ?: emptyList()
    }
    fun getDownloadFiles(): List<File> {
        val dir = Environment.getExternalStoragePublicDirectory(Environment.DIRECTORY_DOWNLOADS)
        return dir.listFiles()?.take(20) ?: emptyList()
    }
}
