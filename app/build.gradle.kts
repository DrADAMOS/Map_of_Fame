plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.compose.plugin)
}

import java.util.Properties

fun signingProperty(name: String): String? {
    val envName = "MAP_OF_FAME_${name.uppercase()}"
    System.getenv(envName)?.takeIf { it.isNotBlank() }?.let { return it }

    val propertiesFile = rootProject.file("keystore.properties")
    if (propertiesFile.isFile) {
        val properties = Properties().apply {
            propertiesFile.inputStream().use { load(it) }
        }
        properties.getProperty(name)?.takeIf { it.isNotBlank() }?.let { return it }
    }
    return null
}

android {
    namespace = "com.adamos.mapoffame"
    compileSdk = 37

    defaultConfig {
        applicationId = "com.adamos.mapoffame"
        minSdk = 26
        targetSdk = 36
        versionCode = 34
        versionName = "1.6.6"

        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    signingConfigs {
        create("production") {
            val storeFilePath = signingProperty("storeFile")
            val storePasswordValue = signingProperty("storePassword")
            val keyAliasValue = signingProperty("keyAlias")
            val keyPasswordValue = signingProperty("keyPassword")
            if (storeFilePath != null && storePasswordValue != null &&
                keyAliasValue != null && keyPasswordValue != null
            ) {
                storeFile = rootProject.file(storeFilePath)
                storePassword = storePasswordValue
                keyAlias = keyAliasValue
                keyPassword = keyPasswordValue
            }
        }
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            val productionSigning = signingConfigs.getByName("production")
            if (productionSigning.storeFile != null) {
                signingConfig = productionSigning
            }
            proguardFiles(getDefaultProguardFile("proguard-android-optimize.txt"), "proguard-rules.pro")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_11
        targetCompatibility = JavaVersion.VERSION_11
    }
    buildFeatures {
        compose = true
        buildConfig = true
    }
}

dependencies {
    implementation(libs.androidx.activity.ktx)
    implementation(libs.androidx.core.splashscreen)
    implementation(libs.androidx.appcompat)
    implementation(libs.androidx.constraintlayout)
    implementation(libs.androidx.core.ktx)
    implementation(libs.material)
    implementation("com.google.android.gms:play-services-ads:25.4.0")
    implementation("com.google.android.ump:user-messaging-platform:4.0.0")
    implementation("androidx.work:work-runtime:2.11.2")

    // Compose
    implementation(platform(libs.androidx.compose.bom))
    implementation(libs.androidx.compose.ui)
    implementation(libs.androidx.compose.ui.graphics)
    implementation(libs.androidx.compose.ui.tooling.preview)
    implementation(libs.androidx.compose.material3)
    implementation(libs.androidx.activity.compose)
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.browser:browser:1.8.0")
    implementation("androidx.webkit:webkit:1.14.0")

    testImplementation(libs.junit)
    androidTestImplementation(libs.androidx.espresso.core)
    androidTestImplementation(libs.androidx.junit)

    // Compose Testing
    androidTestImplementation(platform(libs.androidx.compose.bom))
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    debugImplementation("androidx.compose.ui:ui-test-manifest")

    // Android Test Core and Espresso
    androidTestImplementation("androidx.test:core:1.6.1")
    androidTestImplementation("androidx.test.ext:junit:1.2.1")
    androidTestImplementation("androidx.test:runner:1.6.2")
    androidTestImplementation("androidx.test.espresso:espresso-web:3.6.1")
    androidTestImplementation("androidx.test.espresso:espresso-core:3.6.1")
}
