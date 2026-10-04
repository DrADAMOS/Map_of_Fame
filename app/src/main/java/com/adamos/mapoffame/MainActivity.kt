package com.adamos.mapoffame

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.net.Uri
import android.graphics.Bitmap
import android.os.Build
import android.os.Bundle
import android.util.Log
import org.json.JSONObject
import android.widget.Toast
import android.os.VibrationEffect
import android.os.Vibrator
import android.os.VibratorManager
import android.webkit.JavascriptInterface
import android.webkit.WebChromeClient
import android.webkit.WebResourceError
import android.webkit.WebResourceRequest
import android.webkit.WebSettings
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.webkit.WebViewAssetLoader
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.compose.setContent
import androidx.activity.viewModels
import com.google.android.gms.ads.AdListener
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AgeRestrictedTreatment
import com.google.android.gms.ads.AdSize
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.FullScreenContentCallback
import com.google.android.gms.ads.LoadAdError
import com.google.android.gms.ads.MobileAds
import com.google.android.gms.ads.RequestConfiguration
import com.google.android.gms.ads.interstitial.InterstitialAd
import com.google.android.gms.ads.interstitial.InterstitialAdLoadCallback
import com.google.android.gms.ads.rewarded.RewardedAd
import com.google.android.gms.ads.rewarded.RewardedAdLoadCallback
import com.google.android.ump.ConsentInformation
import com.google.android.ump.ConsentRequestParameters
import com.google.android.ump.UserMessagingPlatform
import androidx.activity.enableEdgeToEdge
import androidx.compose.animation.AnimatedVisibility
import androidx.compose.animation.core.*
import androidx.compose.animation.fadeIn
import androidx.compose.animation.fadeOut
import androidx.compose.foundation.BorderStroke
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.graphics.toArgb
import androidx.compose.ui.res.colorResource
import androidx.compose.ui.res.stringResource
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.compose.ui.platform.testTag
import android.view.View
import android.webkit.ConsoleMessage
import kotlin.math.roundToInt
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat
import androidx.core.view.ViewCompat
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.EmojiEvents
import androidx.browser.customtabs.CustomTabsIntent
import androidx.browser.customtabs.CustomTabColorSchemeParams
import androidx.browser.customtabs.CustomTabsClient
import androidx.browser.customtabs.CustomTabsServiceConnection
import androidx.browser.customtabs.CustomTabsSession
import android.content.ComponentName
import android.graphics.Color as AndroidColor

class MainActivity : ComponentActivity() {

    companion object {
        private const val TAG = "MapOfFameAds"
        private const val BANNER_AD_UNIT_ID = "ca-app-pub-3676225489502432/3534688342"
        private const val INTERSTITIAL_AD_UNIT_ID = "ca-app-pub-3676225489502432/2593925587"
        private const val REWARDED_AD_UNIT_ID = "ca-app-pub-3676225489502432/4544517681"
        // Test ad units are used only for debug builds; release uses production units.
        private const val FORCE_TEST_ADS = false
        private const val TEST_BANNER_AD_UNIT_ID = "ca-app-pub-3940256099942544/9214589741"
        private const val TEST_INTERSTITIAL_AD_UNIT_ID = "ca-app-pub-3940256099942544/1033173712"
        private const val TEST_REWARDED_AD_UNIT_ID = "ca-app-pub-3940256099942544/5224354917"
        private const val PREFS_NAME = "map_of_fame_preferences"
        private const val KEY_AGE_GROUP = "age_group"
        private const val KEY_THEME_MODE = "theme_mode"
        private const val PRIVACY_POLICY_URL = "https://dradamos.github.io/privacy-policy.html"
        private val VALID_AGE_GROUPS = setOf("under_13", "13_17", "18_plus")
        private val WIKIPEDIA_LANGUAGES = setOf(
            "ar", "en", "es", "fr", "de", "pt", "it", "tr",
            "ru", "ja", "zh", "hi", "id", "fa"
        )
        private val useTestAds: Boolean
            get() = BuildConfig.DEBUG || FORCE_TEST_ADS
    }

    private var webView: WebView? = null
    private val viewModel: MainViewModel by viewModels()
    private var customTabsClient: CustomTabsClient? = null
    private var customTabsSession: CustomTabsSession? = null

    private val customTabsConnection = object : CustomTabsServiceConnection() {
        override fun onCustomTabsServiceConnected(name: ComponentName, client: CustomTabsClient) {
            customTabsClient = client
            client.warmup(0L)
            customTabsSession = client.newSession(null)
        }
        override fun onServiceDisconnected(name: ComponentName?) {
            customTabsClient = null
            customTabsSession = null
        }
    }

    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()
        super.onCreate(savedInstanceState)
        
        viewModel.setSelectedAgeGroup(loadSavedAgeGroup())
        
        val prefs = getSharedPreferences(PREFS_NAME, MODE_PRIVATE)
        if (!prefs.contains(KEY_THEME_MODE)) {
            // Production first-launch default: always start in dark mode.
            // The user's saved preference takes precedence on every later launch.
            viewModel.setTheme(true)
        } else {
            viewModel.setTheme(prefs.getBoolean(KEY_THEME_MODE, true))
        }
        
        try {
            val packageName = CustomTabsClient.getPackageName(this, null)
            if (packageName != null) {
                CustomTabsClient.bindCustomTabsService(this, packageName, customTabsConnection)
            }
        } catch (e: Exception) {
            Log.e(TAG, "Custom Tabs bind failed: ${e.message}")
        }

        enableEdgeToEdge()
        hideSystemUI()

        setContent {
            val isDark by viewModel.isDarkMode
            val backgroundColor = colorResource(if (isDark) R.color.primary_dark else R.color.primary_light)

            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = backgroundColor
                ) {
                    if (viewModel.selectedAgeGroup.value == null) {
                        AgeGateScreen()
                    } else {
                        GameScreen()
                    }
                }
            }
        }

        viewModel.selectedAgeGroup.value?.let { startAdsForAgeGroup(it) }

        onBackPressedDispatcher.addCallback(this, object : OnBackPressedCallback(true) {
            override fun handleOnBackPressed() {
                if (webView?.canGoBack() == true) {
                    webView?.goBack()
                } else {
                    finish()
                }
            }
        })
    }

    override fun onDestroy() {
        bannerAdView?.destroy()
        bannerAdView = null
        interstitialAd = null
        rewardedAd = null
        webView?.destroy()
        webView = null
        try {
            unbindService(customTabsConnection)
        } catch (_: Exception) {}
        super.onDestroy()
    }

    private fun hideSystemUI() {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        WindowInsetsControllerCompat(window, window.decorView).let { controller ->
            controller.hide(WindowInsetsCompat.Type.systemBars())
            controller.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        }
    }

    @Composable
    private fun AgeGateScreen() {
        val isDark by viewModel.isDarkMode
        Surface(
            modifier = Modifier.fillMaxSize(),
            color = colorResource(if (isDark) R.color.primary_dark else R.color.primary_light)
        ) {
            Box(modifier = Modifier.fillMaxSize().padding(24.dp), contentAlignment = Alignment.Center) {
                ThemeToggle(modifier = Modifier.align(Alignment.TopEnd).padding(top = 45.dp, end = 40.dp))
                Column(modifier = Modifier.fillMaxWidth().padding(top = 40.dp), horizontalAlignment = Alignment.CenterHorizontally) {
                    Text(text = stringResource(R.string.app_name), color = colorResource(if (isDark) R.color.gold else R.color.gold_dark), style = MaterialTheme.typography.headlineLarge)
                    Spacer(Modifier.height(10.dp))
                    Text(text = stringResource(R.string.choose_age_group), color = if (isDark) Color.White else colorResource(R.color.text_primary_light), style = MaterialTheme.typography.titleMedium)
                    Spacer(Modifier.height(8.dp))
                    Text(text = stringResource(R.string.age_group_desc), color = colorResource(if (isDark) R.color.text_secondary else R.color.text_secondary_light), style = MaterialTheme.typography.bodyMedium)
                    Spacer(Modifier.height(28.dp))
                    AgeChoiceButton(stringResource(R.string.under_13), "under_13")
                    Spacer(Modifier.height(12.dp))
                    AgeChoiceButton(stringResource(R.string.age_13_17), "13_17")
                    Spacer(Modifier.height(12.dp))
                    AgeChoiceButton(stringResource(R.string.age_18_plus), "18_plus")
                    Spacer(Modifier.height(24.dp))
                    TextButton(onClick = { openPrivacyPolicy() }) {
                        Text(text = stringResource(R.string.privacy_policy), color = colorResource(R.color.link_blue))
                    }
                }
            }
        }
    }

    @Composable
    private fun AgeChoiceButton(label: String, ageGroup: String) {
        val isDark by viewModel.isDarkMode
        Button(
            onClick = { selectAgeGroup(ageGroup) },
            modifier = Modifier.fillMaxWidth().height(54.dp),
            colors = ButtonDefaults.buttonColors(
                containerColor = colorResource(if (isDark) R.color.button_bg_dark else R.color.button_bg_light),
                contentColor = if (isDark) Color.White else colorResource(R.color.text_primary_light)
            ),
            border = if (!isDark) BorderStroke(1.dp, Color(0xFFE2E8F0)) else null,
            elevation = ButtonDefaults.buttonElevation(defaultElevation = if (isDark) 0.dp else 2.dp)
        ) {
            Text(label, style = MaterialTheme.typography.titleMedium)
        }
    }

    @Composable
    private fun ThemeToggle(modifier: Modifier = Modifier) {
        val isDark by viewModel.isDarkMode
        IconButton(onClick = { toggleAppTheme() }, modifier = modifier.size(48.dp).padding(8.dp)) {
            Icon(
                imageVector = Icons.Filled.EmojiEvents,
                contentDescription = stringResource(R.string.toggle_theme),
                tint = colorResource(if (isDark) R.color.gold else R.color.gold_dark)
            )
        }
    }

    private fun toggleAppTheme() {
        viewModel.toggleTheme()
        getSharedPreferences(PREFS_NAME, MODE_PRIVATE).edit().putBoolean(KEY_THEME_MODE, viewModel.isDarkMode.value).apply()
        setWebViewTheme(viewModel.isDarkMode.value)
    }

    private fun setWebViewTheme(isDark: Boolean) {
        val mode = if (isDark) "dark" else "light"
        webView?.post { webView?.evaluateJavascript("if(window.setAppTheme) window.setAppTheme('$mode');", null) }
    }

    private fun loadSavedAgeGroup(): String? {
        val saved = getSharedPreferences(PREFS_NAME, MODE_PRIVATE).getString(KEY_AGE_GROUP, null)
        return saved?.takeIf { it in VALID_AGE_GROUPS }
    }

    private fun selectAgeGroup(ageGroup: String) {
        if (ageGroup !in VALID_AGE_GROUPS) {
            Log.w(TAG, "Ignoring invalid age group: $ageGroup")
            return
        }
        getSharedPreferences(PREFS_NAME, MODE_PRIVATE).edit().putString(KEY_AGE_GROUP, ageGroup).apply()
        viewModel.setSelectedAgeGroup(ageGroup)
        startAdsForAgeGroup(ageGroup)
    }

    private fun openPrivacyPolicy() {
        startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(PRIVACY_POLICY_URL)))
    }

    private fun openWiki(url: String) {
        val uri = runCatching { Uri.parse(url) }.getOrNull()
        if (!isAllowedWikipediaUri(uri)) {
            Log.w(TAG, "Blocked non-Wikipedia URL: $url")
            return
        }
        try {
            val builder = CustomTabsIntent.Builder(customTabsSession)
            builder.setShowTitle(true)
            val color = if (viewModel.isDarkMode.value) AndroidColor.parseColor("#080B12") else AndroidColor.WHITE
            val params = CustomTabColorSchemeParams.Builder().setToolbarColor(color).build()
            builder.setDefaultColorSchemeParams(params)
            builder.build().launchUrl(this, Uri.parse(url))
        } catch (e: Exception) {
            Log.e(TAG, "Error opening Wiki in Custom Tab: ${e.message}")
            try { startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url))) } catch (ex: Exception) {}
        }
    }

    private fun isAllowedWikipediaUri(uri: Uri?): Boolean {
        if (uri == null || uri.toString().length > 2_048) return false
        if (uri.scheme != "https") return false
        val host = uri.host?.lowercase() ?: return false
        val parts = host.split('.')
        if (parts.size != 3 && parts.size != 4) return false
        val language = parts.firstOrNull() ?: return false
        if (language !in WIKIPEDIA_LANGUAGES) return false
        return host == "$language.wikipedia.org" || host == "$language.m.wikipedia.org"
    }

    private fun isAllowedExternalUri(uri: Uri?): Boolean {
        if (uri == null || uri.toString().length > 2_048) return false
        if (uri.scheme != "https") return false
        if (uri.userInfo != null || uri.port != -1) return false
        return uri.host?.lowercase() == "play.google.com"
    }

    private fun isAllowedGameAssetUri(uri: Uri): Boolean {
        return uri.scheme == "https" &&
            uri.host?.lowercase() == "appassets.androidplatform.net" &&
            uri.userInfo == null &&
            uri.port == -1 &&
            uri.path?.startsWith("/assets/") == true
    }

    @SuppressLint("SetJavaScriptEnabled")
    private fun configureGameWebView(webView: WebView) {
        WebView.setWebContentsDebuggingEnabled(BuildConfig.DEBUG)
        webView.apply {
            // Leave default hardware acceleration.
            setLayerType(View.LAYER_TYPE_NONE, null)
            setBackgroundColor(0) // Transparent
            overScrollMode = View.OVER_SCROLL_NEVER
            isVerticalScrollBarEnabled = false
            isHorizontalScrollBarEnabled = false
            importantForAccessibility = View.IMPORTANT_FOR_ACCESSIBILITY_YES

            settings.apply {
                javaScriptEnabled = true
                domStorageEnabled = true
                @Suppress("DEPRECATION")
                databaseEnabled = false
                // The game is served through WebViewAssetLoader, so direct file/content
                // access is not required and remains disabled for defense in depth.
                allowFileAccess = false
                allowContentAccess = false
                @Suppress("DEPRECATION")
                allowFileAccessFromFileURLs = false
                @Suppress("DEPRECATION")
                allowUniversalAccessFromFileURLs = false
                safeBrowsingEnabled = true
                mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
                cacheMode = WebSettings.LOAD_DEFAULT
                useWideViewPort = true
                loadWithOverviewMode = false
                builtInZoomControls = false
                displayZoomControls = false
                setSupportZoom(false)
                mediaPlaybackRequiresUserGesture = false
                @Suppress("DEPRECATION")
                offscreenPreRaster = false
            }
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    @Composable
    fun GameScreen() {
        var hasError by remember { mutableStateOf(false) }
        val isDark by viewModel.isDarkMode
        val backgroundColor = colorResource(if (isDark) R.color.primary_dark else R.color.primary_light)
        val assetLoader = remember {
            WebViewAssetLoader.Builder()
                .addPathHandler("/assets/", WebViewAssetLoader.AssetsPathHandler(this@MainActivity))
                .build()
        }
        Box(modifier = Modifier.fillMaxSize().background(backgroundColor)) {
            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { context ->
                    WebView(context).apply {
                        id = View.generateViewId()
                        configureGameWebView(this)
                        webView = this
                        addJavascriptInterface(WebAppInterface(context), "Android")
                        webChromeClient = object : WebChromeClient() {
                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                viewModel.setLoadingProgress(newProgress)
                            }
                            override fun onConsoleMessage(message: ConsoleMessage): Boolean {
                                if (BuildConfig.DEBUG && message.messageLevel() == ConsoleMessage.MessageLevel.ERROR) {
                                    Log.e("MapOfFameWeb", "JS error at ${message.sourceId()}:${message.lineNumber()}")
                                }
                                return true
                            }
                        }
                        webViewClient = object : WebViewClient() {
                            override fun shouldInterceptRequest(
                                view: WebView?,
                                request: WebResourceRequest?
                            ): android.webkit.WebResourceResponse? {
                                val url = request?.url ?: return null
                                return assetLoader.shouldInterceptRequest(url)
                            }

                            override fun shouldOverrideUrlLoading(view: WebView?, request: WebResourceRequest?): Boolean {
                                // Only the bundled asset origin is allowed inside the WebView.
                                // External destinations must go through an explicit native bridge method.
                                val uri = request?.url ?: return true
                                return !isAllowedGameAssetUri(uri)
                            }

                            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                                super.onPageStarted(view, url, favicon)
                                hasError = false
                            }
                            override fun onPageFinished(view: WebView?, url: String?) {
                                super.onPageFinished(view, url)
                                if (url == "https://appassets.androidplatform.net/assets/game.html") {
                                    runOnUiThread { viewModel.setGameLoaded(true) }
                                }
                            }
                            override fun onReceivedError(view: WebView?, request: WebResourceRequest?, error: WebResourceError?) {
                                super.onReceivedError(view, request, error)
                                if (request?.isForMainFrame == true) hasError = true
                            }
                        }
                        loadUrl("https://appassets.androidplatform.net/assets/game.html")
                    }
                },
                update = { view ->
                    val color = backgroundColor.toArgb()
                    if (view.getTag(-1) as? Int != color) {
                        view.setBackgroundColor(color)
                        view.setTag(-1, color)
                    }
                    // Ensure the banner visibility class is synced ONLY when it changes
                    val showBanner = viewModel.showBanner.value
                    if (view.getTag(-2) as? Boolean != showBanner) {
                        view.post {
                            view.evaluateJavascript("if(window.setBannerVisible) window.setBannerVisible($showBanner);", null)
                        }
                        view.setTag(-2, showBanner)
                    }
                }
            )
            LoadingOverlay(hasError) { hasError = false; webView?.reload() }
            BannerAdOverlay(hasError)
        }
    }

    @Composable
    private fun LoadingOverlay(hasError: Boolean, onRetry: () -> Unit) {
        val isGameLoaded by viewModel.isGameLoaded
        val progress by viewModel.loadingProgress
        val isDark by viewModel.isDarkMode
        val animatedProgress by animateFloatAsState(targetValue = progress / 100f, animationSpec = if (progress == 100) tween(500) else spring(), label = "Progress")

        val loadingText = when {
            progress < 30 -> stringResource(R.string.loading_decrypting)
            progress < 60 -> stringResource(R.string.loading_drawing)
            progress < 90 -> stringResource(R.string.loading_locating)
            else -> stringResource(R.string.loading_ready)
        }

        AnimatedVisibility(visible = !isGameLoaded && !hasError, enter = fadeIn(), exit = fadeOut(tween(250))) {
            Surface(
                modifier = Modifier
                    .fillMaxSize()
                    .testTag("loading_overlay"),
                color = colorResource(if (isDark) R.color.primary_dark else R.color.primary_light)
            ) {
                Box(contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(
                            text = loadingText,
                            color = colorResource(if (isDark) R.color.gold else R.color.gold_dark),
                            style = MaterialTheme.typography.headlineSmall,
                            modifier = Modifier.padding(bottom = 24.dp)
                        )
                        LinearProgressIndicator(
                            progress = { animatedProgress },
                            modifier = Modifier.fillMaxWidth(0.6f).height(8.dp),
                            color = colorResource(if (isDark) R.color.gold else R.color.gold_dark),
                            trackColor = colorResource(if (isDark) R.color.button_bg_dark else R.color.button_bg_light),
                            strokeCap = StrokeCap.Round
                        )
                    }
                }
            }
        }
        if (hasError) {
            Surface(modifier = Modifier.fillMaxSize(), color = colorResource(if (isDark) R.color.primary_dark else R.color.primary_light)) {
                Box(contentAlignment = Alignment.Center) {
                    Column(horizontalAlignment = Alignment.CenterHorizontally) {
                        Text(text = stringResource(R.string.error_loading_game), color = if (isDark) Color.White else colorResource(R.color.text_primary_light), style = MaterialTheme.typography.headlineMedium)
                        Button(onClick = onRetry, modifier = Modifier.padding(top = 24.dp), colors = ButtonDefaults.buttonColors(containerColor = colorResource(R.color.gold))) { Text(stringResource(R.string.retry), color = Color.Black) }
                    }
                }
            }
        }
    }

    @Composable
    private fun BoxScope.BannerAdOverlay(hasError: Boolean) {
        val showBanner by viewModel.showBanner
        val isGameLoaded by viewModel.isGameLoaded
        val isDark by viewModel.isDarkMode
        val bannerBgColor = colorResource(if (isDark) R.color.primary_dark else R.color.primary_light).toArgb()

        if (showBanner && isGameLoaded && !hasError && adsInitialized) {
            Column(
                modifier = Modifier
                    .fillMaxWidth()
                    .wrapContentHeight()
                    .align(Alignment.BottomCenter)
                    .background(colorResource(if (isDark) R.color.primary_dark else R.color.primary_light)),
                horizontalAlignment = Alignment.CenterHorizontally
            ) {
                Text(
                    text = "Ad · إعلان",
                    color = Color.Gray,
                    fontSize = 10.sp,
                    modifier = Modifier.padding(top = 2.dp, bottom = 1.dp)
                )
                AndroidView(
                    modifier = Modifier
                        .fillMaxWidth()
                        .wrapContentHeight(),
                    factory = { context ->
                        AdView(context).apply {
                            bannerAdView = this
                            setBackgroundColor(bannerBgColor)
                            adUnitId = if (useTestAds) TEST_BANNER_AD_UNIT_ID else BANNER_AD_UNIT_ID
                            val widthDp = (resources.displayMetrics.widthPixels / resources.displayMetrics.density).roundToInt()
                            setAdSize(AdSize.getCurrentOrientationAnchoredAdaptiveBannerAdSize(context, widthDp))
                            adListener = object : AdListener() {
                                override fun onAdLoaded() { Log.i(TAG, "Banner loaded successfully") }
                                override fun onAdFailedToLoad(error: LoadAdError) { Log.e(TAG, "Banner failed: ${error.message}") }
                            }
                            loadAd(AdRequest.Builder().build())
                        }
                    },
                    update = { bannerAdView = it }
                )
            }
        }
    }

    // region Ad Logic
    private var consentInformation: ConsentInformation? = null
    private var adsInitialized by mutableStateOf(false)
    private var interstitialAd: InterstitialAd? = null
    private var rewardedAd: RewardedAd? = null
    private var rewardedAdLoading = false
    private var isHintPending = false
    private var bannerAdView: AdView? = null

    private fun showPrivacyOptions() {
        val info = consentInformation ?: return
        if (info.privacyOptionsRequirementStatus == ConsentInformation.PrivacyOptionsRequirementStatus.REQUIRED) {
            UserMessagingPlatform.showPrivacyOptionsForm(this) { formError ->
                if (formError != null) {
                    Log.w(TAG, "Privacy options form error: ${formError.message}")
                }
                updatePrivacyOptionsButtonVisibility()
            }
        }
    }

    private fun updatePrivacyOptionsButtonVisibility() {
        val required = consentInformation?.privacyOptionsRequirementStatus == ConsentInformation.PrivacyOptionsRequirementStatus.REQUIRED
        webView?.post { webView?.evaluateJavascript("if (typeof setPrivacyChoicesVisible === 'function') { setPrivacyChoicesVisible($required); }", null) }
    }

    private fun startAdsForAgeGroup(ageGroup: String) {
        val treatment = when (ageGroup) {
            "under_13" -> AgeRestrictedTreatment.CHILD
            "13_17" -> AgeRestrictedTreatment.TEEN
            else -> AgeRestrictedTreatment.UNSPECIFIED
        }
        MobileAds.setRequestConfiguration(
            RequestConfiguration.Builder()
                .setMaxAdContentRating(RequestConfiguration.MAX_AD_CONTENT_RATING_G)
                .setAgeRestrictedTreatment(treatment)
                .build()
        )

        val params = ConsentRequestParameters.Builder()
            .setTagForUnderAgeOfConsent(ageGroup == "under_13")
            .build()
        val info = UserMessagingPlatform.getConsentInformation(this)
        consentInformation = info
        info.requestConsentInfoUpdate(this, params, {
            updatePrivacyOptionsButtonVisibility()
            UserMessagingPlatform.loadAndShowConsentFormIfRequired(this) { formError ->
                updatePrivacyOptionsButtonVisibility()
                if (formError == null && info.canRequestAds()) {
                    initializeAds()
                }
            }
        }, { updateError ->
            Log.w(TAG, "Consent update failed: ${updateError.message}")
            updatePrivacyOptionsButtonVisibility()
            if (info.canRequestAds()) {
                initializeAds()
            }
        })
    }

    private fun initializeAds() {
        if (adsInitialized) return
        MobileAds.initialize(this) { initializationStatus ->
            Log.d(TAG, "MobileAds initialized: $initializationStatus")
            adsInitialized = true
            loadInterstitialAd()
            loadRewardedAd()
        }
    }

    private fun loadInterstitialAd() {
        InterstitialAd.load(
            this,
            if (useTestAds) TEST_INTERSTITIAL_AD_UNIT_ID else INTERSTITIAL_AD_UNIT_ID,
            AdRequest.Builder().build(),
            object : InterstitialAdLoadCallback() {
                override fun onAdLoaded(ad: InterstitialAd) {
                    interstitialAd = ad
                    ad.fullScreenContentCallback = object : FullScreenContentCallback() {
                        override fun onAdDismissedFullScreenContent() {
                            interstitialAd = null
                            loadInterstitialAd()
                        }

                        override fun onAdFailedToShowFullScreenContent(error: com.google.android.gms.ads.AdError) {
                            Log.e(TAG, "Interstitial show failed: ${error.message}")
                            interstitialAd = null
                            loadInterstitialAd()
                        }
                    }
                }

                override fun onAdFailedToLoad(error: LoadAdError) {
                    Log.e(TAG, "Interstitial failed to load: ${error.message}")
                    interstitialAd = null
                }
            })
    }

    private fun showInterstitial() { interstitialAd?.show(this) ?: loadInterstitialAd() }

    private fun loadRewardedAd() {
        if (rewardedAd != null || rewardedAdLoading || !adsInitialized) return
        rewardedAdLoading = true
        RewardedAd.load(
            this,
            if (useTestAds) TEST_REWARDED_AD_UNIT_ID else REWARDED_AD_UNIT_ID,
            AdRequest.Builder().build(),
            object : RewardedAdLoadCallback() {
                override fun onAdLoaded(ad: RewardedAd) {
                    rewardedAdLoading = false
                    rewardedAd = ad
                    if (isHintPending) {
                        isHintPending = false
                        showRewardedHint()
                    }
                    ad.fullScreenContentCallback = object : FullScreenContentCallback() {
                        override fun onAdDismissedFullScreenContent() {
                            rewardedAd = null
                            loadRewardedAd()
                        }

                        override fun onAdFailedToShowFullScreenContent(error: com.google.android.gms.ads.AdError) {
                            Log.e(TAG, "Rewarded show failed: ${error.message}")
                            rewardedAd = null
                            loadRewardedAd()
                        }
                    }
                }

                override fun onAdFailedToLoad(error: LoadAdError) {
                    Log.e(TAG, "Rewarded failed to load: ${error.message}")
                    rewardedAdLoading = false
                    rewardedAd = null
                }
            })
    }

    private fun showRewardedHint() {
        if (!adsInitialized) {
            Log.w(TAG, "Ads not initialized, granting free hint.")
            grantHintInWebView()
            return
        }
        val ad = rewardedAd
        if (ad == null) {
            isHintPending = true; loadRewardedAd()
            if (rewardedAd == null && !rewardedAdLoading) grantHintInWebView()
            else Toast.makeText(this, "Loading reward...", Toast.LENGTH_SHORT).show()
            return
        }
        var rewardEarned = false
        ad.fullScreenContentCallback = object : FullScreenContentCallback() {
            override fun onAdDismissedFullScreenContent() { if (!rewardEarned) resetHintButtonInWebView(); rewardedAd = null; loadRewardedAd() }
            override fun onAdFailedToShowFullScreenContent(e: com.google.android.gms.ads.AdError) { grantHintInWebView(); rewardedAd = null; loadRewardedAd() }
        }
        ad.show(this) { rewardEarned = true; grantHintInWebView() }
    }

    private fun grantHintInWebView() { runOnUiThread { webView?.evaluateJavascript("if(window.onRewardedHintGranted) window.onRewardedHintGranted();", null) } }
    private fun resetHintButtonInWebView() { runOnUiThread { webView?.evaluateJavascript("if(window.onRewardedHintUnavailable) window.onRewardedHintUnavailable();", null) } }
    // endregion

    inner class WebAppInterface(private val mContext: Context) {
        @JavascriptInterface fun gameReady() { runOnUiThread { viewModel.setGameLoaded(true); updatePrivacyOptionsButtonVisibility(); setWebViewTheme(viewModel.isDarkMode.value) } }
        @JavascriptInterface fun vibrate(duration: Long) {
            val safeDuration = duration.coerceIn(1L, 2_000L)
            val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val manager = mContext.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager
                manager.defaultVibrator
            } else {
                @Suppress("DEPRECATION")
                mContext.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
            }
            vibrator.vibrate(VibrationEffect.createOneShot(safeDuration, VibrationEffect.DEFAULT_AMPLITUDE))
        }
        @JavascriptInterface fun openPrivacyPolicy() { runOnUiThread { this@MainActivity.openPrivacyPolicy() } }
        @JavascriptInterface fun openWiki(url: String) {
            val candidate = url.trim()
            if (candidate.isEmpty() || candidate.length > 2_048 || candidate.any(Char::isISOControl)) {
                Log.w(TAG, "Blocked invalid JavaScript Wikipedia URL")
                return
            }
            val uri = runCatching { Uri.parse(candidate) }.getOrNull()
            if (!isAllowedWikipediaUri(uri)) {
                Log.w(TAG, "Blocked JavaScript Wikipedia URL: $url")
                return
            }
            runOnUiThread { this@MainActivity.openWiki(candidate) }
        }
        @JavascriptInterface fun getAppVersion(): String = BuildConfig.VERSION_NAME

        @JavascriptInterface fun getDisplayMetrics(): String {
            val density = resources.displayMetrics.density
            val insets = ViewCompat.getRootWindowInsets(window.decorView)
                ?.getInsets(WindowInsetsCompat.Type.systemBars())
            return JSONObject().apply {
                put("density", density.toDouble())
                put("safeTop", insets?.top ?: 0)
                put("safeBottom", insets?.bottom ?: 0)
            }.toString()
        }
        @JavascriptInterface fun openExternalUrl(url: String) {
            val candidate = url.trim()
            if (candidate.isEmpty() || candidate.length > 2_048 || candidate.any(Char::isISOControl)) {
                Log.w(TAG, "Blocked invalid JavaScript external URL")
                return
            }
            val uri = runCatching { Uri.parse(candidate) }.getOrNull()
            if (!isAllowedExternalUri(uri)) {
                Log.w(TAG, "Blocked JavaScript external URL: $url")
                return
            }
            runOnUiThread {
                try {
                    mContext.startActivity(Intent(Intent.ACTION_VIEW, uri))
                } catch (e: Exception) {
                    Log.e(TAG, "Error opening external URL: ${e.message}")
                }
            }
        }
        @JavascriptInterface fun toggleTheme() { runOnUiThread { this@MainActivity.toggleAppTheme() } }
        @JavascriptInterface fun showPrivacyOptions() { runOnUiThread { this@MainActivity.showPrivacyOptions() } }
        @JavascriptInterface fun share(text: String) {
            val safeText = text.trim().takeIf { it.isNotEmpty() }?.take(4_000) ?: return
            runOnUiThread {
                val intent = Intent(Intent.ACTION_SEND).apply {
                    putExtra(Intent.EXTRA_TEXT, safeText)
                    type = "text/plain"
                }
                runCatching { mContext.startActivity(Intent.createChooser(intent, null)) }
                    .onFailure { Log.e(TAG, "Unable to share content", it) }
            }
        }
        @JavascriptInterface fun showBanner() {
            runOnUiThread {
                viewModel.setShowBanner(true)
                webView?.evaluateJavascript("if(window.setBannerVisible) window.setBannerVisible(true);", null)
            }
        }
        @JavascriptInterface fun hideBanner() {
            runOnUiThread {
                viewModel.setShowBanner(false)
                webView?.evaluateJavascript("if(window.setBannerVisible) window.setBannerVisible(false);", null)
            }
        }
        @JavascriptInterface fun showInterstitial() { runOnUiThread { this@MainActivity.showInterstitial() } }
        @JavascriptInterface fun showRewardedHint() { runOnUiThread { this@MainActivity.showRewardedHint() } }
        @JavascriptInterface fun getAppTheme(): String = if (viewModel.isDarkMode.value) "dark" else "light"
    }
}
