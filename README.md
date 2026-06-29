# Tactocraft Mobile

Tactocraft Mobile is a clean Android APK-ready Python/Pygame project.

## What is included

- `main.py` - playable mobile game prototype
- `buildozer.spec` - Android APK build configuration
- `.github/workflows/build-apk.yml` - GitHub Actions APK builder
- `scripts/cloudshell_build.sh` - Google Cloud Shell build helper
- `config/game_settings.json` - project settings
- `assets/` - placeholder folders for future music, sounds and images

## Build APK on GitHub

Open the repository, then:

`Actions` -> `Build Tactocraft APK` -> `Run workflow`

When the build is green, download the APK from `Artifacts`.

## Build APK on Google Cloud Shell

```bash
bash scripts/cloudshell_build.sh
```

APK output:

```text
bin/*.apk
```

## Local Pydroid test

Open `main.py` in Pydroid 3 and run it.
