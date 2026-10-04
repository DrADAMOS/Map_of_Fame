# Production Release Signing

The release build supports signing credentials without storing secrets in source control.

## Environment variables

- `MAP_OF_FAME_STOREFILE`
- `MAP_OF_FAME_STOREPASSWORD`
- `MAP_OF_FAME_KEYALIAS`
- `MAP_OF_FAME_KEYPASSWORD`

Alternatively create a local root `keystore.properties` file (ignored by Git) with:

```properties
storeFile=path/to/release-key.jks
storePassword=***
keyAlias=***
keyPassword=***
```

Never commit the keystore or this properties file.

If no signing credentials are present, the release configuration remains unsigned so Android Studio/Gradle can use the normal local signing flow.

## Version

This release candidate uses `versionCode 30` and `versionName 1.6.2`. Before uploading to Google Play, confirm that `versionCode 30` is greater than the currently published Play version.
