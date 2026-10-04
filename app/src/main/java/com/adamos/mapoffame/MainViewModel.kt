package com.adamos.mapoffame

import androidx.compose.runtime.mutableStateOf
import androidx.lifecycle.ViewModel

class MainViewModel : ViewModel() {
    var isDarkMode = mutableStateOf(true)
        private set

    var isGameLoaded = mutableStateOf(false)
        private set

    var showBanner = mutableStateOf(false)
        private set

    var selectedAgeGroup = mutableStateOf<String?>(null)
        private set

    var loadingProgress = mutableStateOf(0)
        private set

    fun toggleTheme() {
        isDarkMode.value = !isDarkMode.value
    }

    fun setTheme(dark: Boolean) {
        isDarkMode.value = dark
    }

    fun setGameLoaded(loaded: Boolean) {
        isGameLoaded.value = loaded
    }

    fun setShowBanner(show: Boolean) {
        showBanner.value = show
    }

    fun setSelectedAgeGroup(ageGroup: String?) {
        selectedAgeGroup.value = ageGroup
    }

    fun setLoadingProgress(progress: Int) {
        loadingProgress.value = progress
    }
}
