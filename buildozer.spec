[app]
title = TaTask
package.name = app
package.domain = com.tatask
source.dir = .
source.include_exts = py,png,ttf,otf,kv
version = 1.0
requirements = python3,kivy==2.3.0,kivymd==1.2.0,pillow
orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24

[buildozer]
log_level = 2
warn_on_root = 1
