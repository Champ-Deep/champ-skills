---
name: android-twa-packaging
description: "Package a web app or PWA into an installable Android APK."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [android, apk, twa, bubblewrap, pwa, packaging]
    category: engineering
    related_skills: [live-deployment-discovery]
---

# Android TWA packaging (web app → installable APK)

Use when the deliverable is an app a human installs on a phone and the product
already runs as a web app. The packaging wraps the live site in a Trusted Web
Activity: one build, and every later deploy of the site updates the installed
app with no rebuild.

**Deep's standing ask: an APK, not a Play Store listing.** He sideloads. Give him
the signed `.apk` as a `MEDIA:/absolute/path` card, not a path to copy, and say
which side-load setting he has to enable.

## When to Use

Any "give me an APK", "I want to install this on my phone", "package the site
as an Android app", or "make this installable" request against an app that
already runs on the web. Not for Play Store submission (that needs an `.aab`
plus store-side signing) and not for building a native app from scratch.

## Procedure

1. **Confirm the web app actually works before packaging it.** A TWA only wraps
   what is deployed: verify the live URL, then read its manifest and `start_url`
   (the packaged app opens exactly that page).
2. **Toolchain (macOS, once):**
   ```bash
   brew install openjdk@17
   brew install --cask android-commandlinetools
   cd /opt/homebrew/share/android-commandlinetools
   ln -sfn cmdline-tools/latest/bin bin
   ln -sfn cmdline-tools/latest/lib lib
   npm i -g @bubblewrap/cli
   ```
   The `bin`/`lib` symlinks are mandatory: Bubblewrap's `validatePath` requires
   `<sdk>/bin/sdkmanager`, but Homebrew lays the tools out under
   `cmdline-tools/latest/`, so without them it reports `The provided androidSdk
   isn't correct.` for a perfectly good install.
3. **Bubblewrap config (`~/.bubblewrap/config.json`) — raw POSIX paths, no
   backslashes:**
   ```json
   {"jdkPath":"/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk",
    "androidSdkPath":"/opt/homebrew/share/android-commandlinetools"}
   ```
   `jdkPath` points at the `.jdk` bundle, NOT `.../Contents/Home`. On macOS
   Bubblewrap appends `Contents/Home` itself; supply it and JAVA_HOME becomes
   `.../Contents/Home/Contents/Home/`, which the JDK rejects as invalid.
4. **Author `twa-manifest.json` by hand instead of running `bubblewrap init`.**
   The wizard is interactive and stalls in a non-TTY shell. Copy
   `templates/twa-manifest.json`, set `packageId`, `host`, `name`,
   `launcherName`, `themeColor`/`backgroundColor` (match the site),
   `display: "standalone"`, `iconUrl`/`splashScreenUrl` (absolute https URLs the
   build can fetch), and **`minSdkVersion: 24`**.
   - 21 is Bubblewrap's default and fails the manifest merger against
     `com.google.androidbrowserhelper` (which declares 24): `Manifest merger
     failed : uses-sdk:minSdkVersion 21 cannot be smaller than version 24`.
     Raise the manifest, do not patch the Gradle build.
5. **Generate a keystore once, then never again:**
   ```bash
   keytool -genkeypair -v -keystore android.keystore -alias myapp \
     -keyalg RSA -keysize 2048 -validity 10000
   ```
   Bubblewrap stores the passphrase in `~/.bubblewrap/<alias>.keypass`; export
   both `BUBBLEWRAP_KEYSTORE_PASSWORD` and `BUBBLEWRAP_KEY_PASSWORD` from it
   before building. `bubblewrap build` writes `.apk` (sideload) and `.aab`
   (Play Store) next to the project.
6. **Verify the artifact, don't assume success:**
   ```bash
   BT=/opt/homebrew/share/android-commandlinetools/build-tools/<v>
   $BT/apksigner verify --print-certs app-release-signed.apk   # signature + SHA-256
   $BT/aapt dump badging app-release-signed.apk                # package, minSdk, activity
   ```
   Then copy it to a stable name (`~/Downloads/<App>-v1.apk`) and hand it over
   as `MEDIA:`.
7. **Digital Asset Links for fullscreen.** Put `.well-known/assetlinks.json` at
   the site root (package name + the SHA-256 digest from `apksigner verify`,
   colon-separated). Once deployed the app drops the Chrome URL bar; until then
   it runs as a Custom Tab. **A missing assetlinks.json is not a failure**: the
   app still opens, still has camera/JS/network, only the bar shows. Report it
   as degraded, never as broken.
8. **Keep signing material out of git.** `.gitignore` the keystore, `*.apk`,
   `*.aab`, and `app/`/`.gradle/` build output; commit the manifest and
   `assetlinks.json` only. Pushing is the user's call: say what is staged and
   what deploying it would change.

## Pitfalls

- Verify with `apksigner`, never `ls -la`: a file named `*-signed.apk` that
  failed verification still sits on disk and would be handed over as working.
- Read `badging` before shipping: it confirms the package id, `minSdkVersion`,
  and launchable activity you intended. A wrong `minSdkVersion` installs fine
  and then crashes on the oldest devices.
- Losing the keystore means no future update can ship under the same package
  name (the signature check fails), so say where it lives and where the
  password is stored the first time you hand over a build.
- Feed passwords through env vars read from the keypass file, never typed into
  the command line or repeated in chat.
- After editing `twa-manifest.json`, run
  `bubblewrap update --skipVersionUpgrade` to regenerate the Gradle project;
  editing the manifest alone changes nothing.
- The app is a wrapper: features that work in mobile Chrome work, features that
  need native plugins (offline storage, push, background sensors) do not. Check
  the feature class you are packaging is web-native before promising it.
- Bubblewrap signs with its own key, so the result is a debug-signed
  distribution build: fine for sideloading, not for store review.
