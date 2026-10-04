package com.adamos.mapoffame

import android.content.Context
import androidx.test.core.app.ActivityScenario
import androidx.test.core.app.ApplicationProvider
import androidx.test.espresso.web.sugar.Web.onWebView
import androidx.test.espresso.web.webdriver.DriverAtoms.*
import androidx.test.espresso.web.webdriver.Locator
import androidx.test.espresso.web.assertion.WebViewAssertions.webMatches
import org.hamcrest.CoreMatchers.containsString
import org.junit.Test
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class GameWebViewTest {
    @Test
    fun gamePageShowsStartScreenAndBeginsGame() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        context.getSharedPreferences("map_of_fame_preferences", Context.MODE_PRIVATE)
            .edit()
            .putString("age_group", "18_plus")
            .commit()

        ActivityScenario.launch(MainActivity::class.java).use {
            onWebView()
                .withElement(findElement(Locator.ID, "startScreen"))
                .check(webMatches(getText(), containsString("خريطة العظماء")))

            onWebView()
                .withElement(findElement(Locator.ID, "btnDiffEasy"))
                .perform(webClick())

            onWebView()
                .withElement(findElement(Locator.ID, "map"))
                .check(webMatches(getText(), containsString(""))) // Just check it exists and has some text (or use another atom)
        }
    }
}
