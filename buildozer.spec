[app]
title = Tactocraft Mobile
package.name = tactocraftmobile
package.domain = com.mrjacobnjr
source.dir = .
source.include_exts = py,png,jpg,jpeg,ogg,wav,json,txt,md
version = 8.8.8

requirements = python3,pygame
orientation = landscape
fullscreen = 1

android.permissions = INTERNET
android.api = 35
android.minapi = 23
android.ndk_api = 23
android.archs = arm64-v8a
android.allow_backup = False
android.accept_sdk_license = True
android.build_tools_version = 35.0.0

[buildozer]
log_level = 2
warn_on_root = 1
