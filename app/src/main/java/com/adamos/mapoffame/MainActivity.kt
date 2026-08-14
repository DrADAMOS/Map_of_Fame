package com.adamos.mapoffame

import android.annotation.SuppressLint
import android.content.Context
import android.content.Intent
import android.graphics.Bitmap
import android.os.Build
import android.os.Bundle
import android.util.Log
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
import androidx.activity.ComponentActivity
import androidx.activity.OnBackPressedCallback
import androidx.activity.compose.setContent
import com.google.android.gms.ads.AdListener
import com.google.android.gms.ads.AdRequest
import com.google.android.gms.ads.AdSize
import com.google.android.gms.ads.AdView
import com.google.android.gms.ads.FullScreenContentCallback
import com.google.android.gms.ads.LoadAdError
import com.google.android.gms.ads.MobileAds
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
import androidx.compose.animation.scaleOut
import androidx.compose.foundation.layout.*
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.scale
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.graphics.StrokeCap
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.unit.dp
import kotlin.math.roundToInt
import androidx.compose.ui.viewinterop.AndroidView
import androidx.core.splashscreen.SplashScreen.Companion.installSplashScreen
import androidx.core.view.WindowCompat
import androidx.core.view.WindowInsetsCompat
import androidx.core.view.WindowInsetsControllerCompat

class MainActivity : ComponentActivity() {

    companion object {
        private const val TAG = "MapOfFameAds"
        private const val BANNER_AD_UNIT_ID = "ca-app-pub-3676225489502432/3534688342"
        private const val INTERSTITIAL_AD_UNIT_ID = "ca-app-pub-3676225489502432/2593925587"
        private const val REWARDED_AD_UNIT_ID = "ca-app-pub-3676225489502432/4544517681"
        // Development flag: keep true while testing. Set false only for the final production build.
        private const val USE_TEST_ADS = false
        private const val TEST_BANNER_AD_UNIT_ID = "ca-app-pub-3940256099942544/9214589741"
        private const val TEST_INTERSTITIAL_AD_UNIT_ID = "ca-app-pub-3940256099942544/1033173712"
        private const val TEST_REWARDED_AD_UNIT_ID = "ca-app-pub-3940256099942544/5224354917"
    }

    private var webView: WebView? = null
    private val isGameLoaded = mutableStateOf(false)
    private var consentInformation: ConsentInformation? = null
    private var adsInitialized = false
    private var interstitialAd: InterstitialAd? = null
    private var rewardedAd: RewardedAd? = null
    private var rewardedAdLoading = false
    private var bannerAdView: AdView? = null
    private var showBanner = mutableStateOf(false)

    override fun onCreate(savedInstanceState: Bundle?) {
        installSplashScreen()
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        
        hideSystemUI()
        requestAdConsentAndInitialize()

        setContent {
            MaterialTheme {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xFF080B12)
                ) {
                    GameScreen()
                }
            }
        }

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
        super.onDestroy()
    }

    private fun hideSystemUI() {
        WindowCompat.setDecorFitsSystemWindows(window, false)
        WindowInsetsControllerCompat(window, window.decorView).let { controller ->
            controller.hide(WindowInsetsCompat.Type.systemBars())
            controller.systemBarsBehavior = WindowInsetsControllerCompat.BEHAVIOR_SHOW_TRANSIENT_BARS_BY_SWIPE
        }
    }

    @SuppressLint("SetJavaScriptEnabled")
    @Composable
    fun GameScreen() {
        var progress by remember { mutableIntStateOf(0) }
        var hasError by remember { mutableStateOf(false) }
        var loadingText by remember { mutableStateOf("Initializing...") }

        val animatedProgress by animateFloatAsState(
            targetValue = progress / 100f,
            animationSpec = if (progress == 100) tween(500) else spring(dampingRatio = Spring.DampingRatioLowBouncy),
            label = "Progress"
        )

        Box(modifier = Modifier.fillMaxSize()) {
            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { context ->
                    WebView(context).apply {
                        webView = this
                        addJavascriptInterface(WebAppInterface(context), "Android")
                        
                        webChromeClient = object : WebChromeClient() {
                            override fun onProgressChanged(view: WebView?, newProgress: Int) {
                                progress = newProgress
                                loadingText = when {
                                    newProgress < 30 -> "Decrypting History..."
                                    newProgress < 60 -> "Drawing Borders..."
                                    newProgress < 90 -> "Locating Legends..."
                                    else -> "Ready to Start!"
                                }
                            }
                        }

                        webViewClient = object : WebViewClient() {
                            override fun onPageStarted(view: WebView?, url: String?, favicon: Bitmap?) {
                                super.onPageStarted(view, url, favicon)
                                hasError = false
                            }

                            override fun onReceivedError(
                                view: WebView?,
                                request: WebResourceRequest?,
                                error: WebResourceError?
                            ) {
                                super.onReceivedError(view, request, error)
                                if (request?.isForMainFrame == true) {
                                    hasError = true
                                }
                            }
                        }

                        settings.apply {
                            javaScriptEnabled = true
                            domStorageEnabled = true
                            loadWithOverviewMode = true
                            useWideViewPort = true
                            allowFileAccess = true
                            mediaPlaybackRequiresUserGesture = false
                            mixedContentMode = WebSettings.MIXED_CONTENT_NEVER_ALLOW
                        }
                        
                        loadUrl("file:///android_asset/game.html")
                    }
                }
            )

            // Enhanced Professional Splash Overlay
            AnimatedVisibility(
                visible = !isGameLoaded.value && !hasError,
                enter = fadeIn(),
                exit = fadeOut(animationSpec = tween(800)) + scaleOut(targetScale = 1.5f, animationSpec = tween(800))
            ) {
                Surface(
                    modifier = Modifier.fillMaxSize(),
                    color = Color(0xFF080B12)
                ) {
                    Box(contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(
                                text = loadingText,
                                color = Color(0xFFF0A500),
                                style = MaterialTheme.typography.headlineSmall,
                                modifier = Modifier.padding(bottom = 24.dp)
                            )
                            
                            LinearProgressIndicator(
                                progress = { animatedProgress },
                                modifier = Modifier
                                    .fillMaxWidth(0.6f)
                                    .height(8.dp),
                                color = Color(0xFFF0A500),
                                trackColor = Color(0xFF1A2235),
                                strokeCap = StrokeCap.Round
                            )
                        }
                    }
                }
            }

            if (hasError) {
                Surface(modifier = Modifier.fillMaxSize(), color = Color(0xFF080B12)) {
                    Box(contentAlignment = Alignment.Center) {
                        Column(horizontalAlignment = Alignment.CenterHorizontally) {
                            Text(text = "Unable to load game", color = Color.White, style = MaterialTheme.typography.headlineMedium)
                            Button(
                                onClick = {
                                    hasError = false
                                    webView?.reload()
                                },
                                modifier = Modifier.padding(top = 24.dp),
                                colors = ButtonDefaults.buttonColors(containerColor = Color(0xFFF0A500))
                            ) {
                                Text("Retry", color = Color.Black)
                            }
                        }
                    }
                }
            }

            if (showBanner.value && isGameLoaded.value && !hasError) {
                AndroidView(
                    modifier = Modifier
                        .fillMaxWidth()
                        .wrapContentHeight()
                        .align(Alignment.BottomCenter),
                    factory = { context ->
                        AdView(context).apply {
                            bannerAdView = this
                            adUnitId = if (USE_TEST_ADS) TEST_BANNER_AD_UNIT_ID else BANNER_AD_UNIT_ID
                            val widthDp = (resources.displayMetrics.widthPixels / resources.displayMetrics.density).roundToInt()
                            setAdSize(AdSize.getLargeAnchoredAdaptiveBannerAdSize(context, widthDp))
                            adListener = object : AdListener() {
                                override fun onAdFailedToLoad(error: LoadAdError) {
                                    Log.w(TAG, "Banner failed: ${error.message}")
                                }
                            }
                            loadAd(AdRequest.Builder().build())
                        }
                    },
                    update = { bannerAdView = it }
                )
            }
        }
    }

    private fun requestAdConsentAndInitialize() {
        val params = ConsentRequestParameters.Builder().build()
        val info = UserMessagingPlatform.getConsentInformation(this)
        consentInformation = info
        info.requestConsentInfoUpdate(
            this,
            params,
            {
                UserMessagingPlatform.loadAndShowConsentFormIfRequired(this) { formError ->
                    if (formError != null) {
                        Log.w(TAG, "Consent form: ${formError.message}")
                    }
                    if (info.canRequestAds()) initializeAds()
                }
            },
            { error ->
                Log.w(TAG, "Consent update: ${error.message}")
                if (info.canRequestAds()) initializeAds()
            }
        )
        if (info.canRequestAds()) initializeAds()
    }

    private fun initializeAds() {
        if (adsInitialized) return
        adsInitialized = true
        MobileAds.initialize(this) {
            loadInterstitialAd()
            loadRewardedAd()
        }
    }

    private fun loadInterstitialAd() {
        InterstitialAd.load(
            this,
            if (USE_TEST_ADS) TEST_INTERSTITIAL_AD_UNIT_ID else INTERSTITIAL_AD_UNIT_ID,
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
                            interstitialAd = null
                            loadInterstitialAd()
                        }
                    }
                }

                override fun onAdFailedToLoad(error: LoadAdError) {
                    interstitialAd = null
                    Log.w(TAG, "Interstitial failed: ${error.message}")
                }
            }
        )
    }

    private fun showInterstitial() {
        val ad = interstitialAd
        if (ad == null) {
            loadInterstitialAd()
            return
        }
        ad.show(this)
    }

    private fun loadRewardedAd() {
        if (rewardedAd != null || rewardedAdLoading || !adsInitialized) return
        rewardedAdLoading = true
        RewardedAd.load(
            this,
            if (USE_TEST_ADS) TEST_REWARDED_AD_UNIT_ID else REWARDED_AD_UNIT_ID,
            AdRequest.Builder().build(),
            object : RewardedAdLoadCallback() {
                override fun onAdLoaded(ad: RewardedAd) {
                    rewardedAdLoading = false
                    rewardedAd = ad
                    ad.fullScreenContentCallback = object : FullScreenContentCallback() {
                        override fun onAdDismissedFullScreenContent() {
                            rewardedAd = null
                            loadRewardedAd()
                        }

                        override fun onAdFailedToShowFullScreenContent(error: com.google.android.gms.ads.AdError) {
                            Log.w(TAG, "Rewarded failed to show: ${error.message}")
                            rewardedAd = null
                            grantHintInWebView()
                            loadRewardedAd()
                        }
                    }
                }

                override fun onAdFailedToLoad(error: LoadAdError) {
                    rewardedAdLoading = false
                    rewardedAd = null
                    Log.w(TAG, "Rewarded failed: ${error.message}")
                }
            }
        )
    }

    private fun showRewardedHint() {
        val ad = rewardedAd
        if (ad == null) {
            loadRewardedAd()
            grantHintInWebView()
            return
        }

        var rewardEarned = false
        ad.fullScreenContentCallback = object : FullScreenContentCallback() {
            override fun onAdDismissedFullScreenContent() {
                rewardedAd = null
                if (!rewardEarned) resetHintButtonInWebView()
                loadRewardedAd()
            }

            override fun onAdFailedToShowFullScreenContent(error: com.google.android.gms.ads.AdError) {
                Log.w(TAG, "Rewarded failed to show: ${error.message}")
                rewardedAd = null
                if (!rewardEarned) grantHintInWebView()
                loadRewardedAd()
            }
        }
        ad.show(this) {
            rewardEarned = true
            grantHintInWebView()
        }
    }

    private fun grantHintInWebView() {
        runOnUiThread {
            webView?.evaluateJavascript(
                "window.onRewardedHintGranted && window.onRewardedHintGranted();",
                null
            )
        }
    }

    private fun resetHintButtonInWebView() {
        runOnUiThread {
            webView?.evaluateJavascript(
                "window.onRewardedHintUnavailable && window.onRewardedHintUnavailable();",
                null
            )
        }
    }

    inner class WebAppInterface(private val mContext: Context) {
        @JavascriptInterface
        fun gameReady() {
            runOnUiThread {
                isGameLoaded.value = true
            }
        }

        @JavascriptInterface
        fun vibrate(duration: Long) {
            val vibrator = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
                val vibratorManager = mContext.getSystemService(Context.VIBRATOR_MANAGER_SERVICE) as VibratorManager
                vibratorManager.defaultVibrator
            } else {
                @Suppress("DEPRECATION")
                mContext.getSystemService(Context.VIBRATOR_SERVICE) as Vibrator
            }

            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                vibrator.vibrate(VibrationEffect.createOneShot(duration, VibrationEffect.DEFAULT_AMPLITUDE))
            } else {
                @Suppress("DEPRECATION")
                vibrator.vibrate(duration)
            }
        }

        @JavascriptInterface
        fun share(text: String) {
            val sendIntent: Intent = Intent().apply {
                action = Intent.ACTION_SEND
                putExtra(Intent.EXTRA_TEXT, text)
                type = "text/plain"
            }
            val shareIntent = Intent.createChooser(sendIntent, null)
            mContext.startActivity(shareIntent)
        }

        @JavascriptInterface
        fun showBanner() {
            runOnUiThread { showBanner.value = true }
        }

        @JavascriptInterface
        fun hideBanner() {
            runOnUiThread { showBanner.value = false }
        }

        @JavascriptInterface
        fun showInterstitial() {
            runOnUiThread { this@MainActivity.showInterstitial() }
        }

        @JavascriptInterface
        fun showRewardedHint() {
            runOnUiThread { this@MainActivity.showRewardedHint() }
        }
    }
}
