package com.adamos.mapoffame

import android.content.Context
import android.view.View
import android.view.ViewGroup
import android.webkit.WebView
import androidx.test.core.app.ActivityScenario
import androidx.test.core.app.ApplicationProvider
import androidx.test.espresso.matcher.BoundedMatcher
import androidx.test.espresso.web.sugar.Web.onWebView
import androidx.test.espresso.web.webdriver.DriverAtoms.findElement
import androidx.test.espresso.web.webdriver.DriverAtoms.webClick
import androidx.test.espresso.web.webdriver.Locator
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.hamcrest.Description
import org.hamcrest.Matcher
import org.junit.After
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Before
import org.junit.Test
import org.junit.runner.RunWith
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

@RunWith(AndroidJUnit4::class)
class ResetBehaviorTest {

    private lateinit var scenario: ActivityScenario<MainActivity>

    @Before
    fun setUp() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        context.getSharedPreferences("map_of_fame_preferences", Context.MODE_PRIVATE)
            .edit()
            .putString("age_group", "18_plus")
            .putBoolean("theme_mode", true)
            .commit()

        scenario = ActivityScenario.launch(MainActivity::class.java)
    }

    @After
    fun tearDown() {
        scenario.close()
    }

    @Test
    fun testRealUiCancelAndResetFlow() {
        Thread.sleep(3000)

        // A) Seed person_memory with real learning records & update dashboard
        runInWebView { webView ->
            webView.evaluateJavascript(
                """
                localStorage.setItem('highScore', '150');
                localStorage.setItem('achievements', JSON.stringify(['first_win']));
                localStorage.setItem('person_memory', JSON.stringify({
                    'Person1': { seen: 3, correct: 3, wrong: 0, mastery: 100, status: 'MASTERED', name: 'Person1' },
                    'Person2': { seen: 2, correct: 1, wrong: 1, mastery: 50, status: 'REVIEW', name: 'Person2' },
                    'Person3': { seen: 1, correct: 0, wrong: 1, mastery: 0, status: 'FAILED', name: 'Person3' }
                }));
                localStorage.setItem('unlocked_achievements', JSON.stringify({
                    'first_win': { unlocked: true }
                }));
                localStorage.setItem('game_stats', JSON.stringify({
                    correctAnswers: 12,
                    wrongAnswers: 3,
                    gamesPlayed: 2,
                    xp: 200,
                    level: 2
                }));
                localStorage.setItem('game_settings', JSON.stringify({
                    lang: 'ar',
                    theme: 'dark',
                    lastMode: 'all',
                    lastDiff: 'easy'
                }));
                if (typeof refreshMemoryDashboard === 'function') {
                    refreshMemoryDashboard();
                }
                """.trimIndent(),
                null
            )
        }

        Thread.sleep(500)

        // B) Verify before reset that the dashboard is non-zero
        assertWebViewValue("document.getElementById('memoryLearned').textContent", "\"3\"")
        assertWebViewValue("document.getElementById('memoryReview').textContent", "\"1\"")
        assertWebViewValue("document.getElementById('memoryFailed').textContent", "\"1\"")
        assertWebViewValue("document.getElementById('memoryMastered').textContent", "\"1\"")

        // C) Cancel test: Settings -> Reset -> Cancel
        webClickMainWebViewElement("settingsToggle")
        Thread.sleep(800)

        webClickMainWebViewElement("lblResetApp")
        Thread.sleep(800)

        webClickMainWebViewElement("btnResetNo")
        Thread.sleep(800)

        assertWebViewValue("localStorage.getItem('person_memory') !== null", "true")
        assertWebViewValue("document.getElementById('memoryLearned').textContent", "\"3\"")
        assertWebViewValue("document.getElementById('memoryReview').textContent", "\"1\"")
        assertWebViewValue("document.getElementById('memoryFailed').textContent", "\"1\"")
        assertWebViewValue("document.getElementById('memoryMastered').textContent", "\"1\"")
        assertWebViewValue("localStorage.getItem('highScore')", "\"150\"")
        assertWebViewValue("localStorage.getItem('game_stats') !== null", "true")
        assertWebViewValue("JSON.parse(localStorage.getItem('game_settings')).lang", "\"ar\"")
        assertWebViewValue("JSON.parse(localStorage.getItem('game_settings')).theme", "\"dark\"")

        // D) Settings -> Reset -> Confirm (settingsModal is already open from Cancel)
        webClickMainWebViewElement("lblResetApp")
        Thread.sleep(800)

        runInWebView { webView ->
            webView.evaluateJavascript(
                """
                if (typeof Stats !== 'undefined' && Stats.addXP) {
                    Stats.addXP(10);
                }
                """.trimIndent(),
                null
            )
        }

        webClickMainWebViewElement("btnResetYes")
        Thread.sleep(1500)

        // E) Immediately after reset, verify person_memory is null & dashboard counters are 0
        assertWebViewValue("localStorage.getItem('person_memory')", "null")
        assertWebViewValue("document.getElementById('memoryLearned').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryReview').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryFailed').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryMastered').textContent", "\"0\"")

        // F) Verify game_stats, highScore, Stats.get().xp, language, theme
        assertWebViewValue("localStorage.getItem('highScore')", "null")
        assertWebViewValue("localStorage.getItem('game_stats')", "null")
        assertWebViewValue("Stats.get().xp", "0")
        assertWebViewValue("JSON.parse(localStorage.getItem('game_settings')).lang", "\"ar\"")
        assertWebViewValue("JSON.parse(localStorage.getItem('game_settings')).theme", "\"dark\"")

        // G) Wait at least 1600 ms and re-check all four counters and storage
        Thread.sleep(1600)

        assertWebViewValue("localStorage.getItem('person_memory')", "null")
        assertWebViewValue("document.getElementById('memoryLearned').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryReview').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryFailed').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryMastered').textContent", "\"0\"")
        assertWebViewValue("localStorage.getItem('game_stats') === null && Stats.get().xp === 0", "true")

        // H) Recreate Activity and verify all four dashboard counters remain 0
        scenario.recreate()
        Thread.sleep(3000)

        assertWebViewValue("localStorage.getItem('person_memory')", "null")
        assertWebViewValue("document.getElementById('memoryLearned').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryReview').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryFailed').textContent", "\"0\"")
        assertWebViewValue("document.getElementById('memoryMastered').textContent", "\"0\"")
        assertWebViewValue("localStorage.getItem('highScore')", "null")
        assertWebViewValue("localStorage.getItem('game_stats')", "null")
        assertWebViewValue("JSON.parse(localStorage.getItem('game_settings')).lang", "\"ar\"")
        assertWebViewValue("JSON.parse(localStorage.getItem('game_settings')).theme", "\"dark\"")
    }

    private fun webClickMainWebViewElement(elementId: String) {
        onWebView(mainWebViewMatcher())
            .withElement(findElement(Locator.ID, elementId))
            .perform(webClick())
    }

    private fun mainWebViewMatcher(): Matcher<View> {
        return object : BoundedMatcher<View, WebView>(WebView::class.java) {
            override fun describeTo(description: Description) {
                description.appendText("the main application WebView")
            }

            override fun matchesSafely(webView: WebView): Boolean {
                return webView.width >= 1000 &&
                    webView.height >= 1000 &&
                    webView.id != View.NO_ID
            }
        }
    }

    private fun assertWebViewValue(
        javascript: String,
        expected: String
    ) {
        val latch = CountDownLatch(1)
        var actual: String? = null

        scenario.onActivity { activity ->
            val webView = findMainWebViewDirectly(activity.window.decorView)
            assertNotNull("Main application WebView should be present", webView)

            webView?.post {
                webView.evaluateJavascript(javascript) { result ->
                    actual = result
                    latch.countDown()
                }
            } ?: latch.countDown()
        }

        assertEquals(
            "JavaScript evaluation timed out",
            true,
            latch.await(5, TimeUnit.SECONDS)
        )
        assertEquals(
            "Unexpected JavaScript result for: $javascript",
            expected,
            actual
        )
    }

    private fun runInWebView(block: (WebView) -> Unit) {
        val latch = CountDownLatch(1)

        scenario.onActivity { activity ->
            val webView = findMainWebViewDirectly(activity.window.decorView)
            assertNotNull("Main application WebView should be present", webView)

            webView?.post {
                block(webView)
                latch.countDown()
            } ?: latch.countDown()
        }

        assertEquals(
            "WebView operation timed out",
            true,
            latch.await(5, TimeUnit.SECONDS)
        )
    }

    private fun findMainWebViewDirectly(view: View): WebView? {
        if (
            view is WebView &&
            view.width >= 1000 &&
            view.height >= 1000 &&
            view.id != View.NO_ID
        ) {
            return view
        }

        if (view is ViewGroup) {
            for (index in 0 until view.childCount) {
                val found = findMainWebViewDirectly(view.getChildAt(index))
                if (found != null) {
                    return found
                }
            }
        }

        return null
    }
}
