# Map of Fame release R8 rules.

# Keep the native JavaScript bridge and all annotated methods.
-keep class com.adamos.mapoffame.MainActivity$WebAppInterface {
    *;
}
-keepclassmembers class * {
    @android.webkit.JavascriptInterface <methods>;
}

# Keep app JSON/reflection fields if native model classes are introduced or used
# by reflection in future releases. The current game JSON is parsed in JavaScript,
# so no Gson/Kotlinx Serialization model keep rules are required today.
-keepclassmembers class com.adamos.mapoffame.** {
    <fields>;
}
