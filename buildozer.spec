[app]
title = TaTask
package.name = app
package.domain = com.tatask
source.dir = .
source.include_exts = py,png,ttf,otf,kv
source.exclude_dirs = .git,.buildozer,build,dist,bin,Builds,export,__pycache__
source.exclude_patterns = *.spec,*.log,*.exe
version = 1.0
requirements = python3==3.11.0,kivy==2.3.0,kivymd==1.2.0,pillow
orientation = portrait
fullscreen = 0

# Android permissions
android.permissions = VIBRATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 24
android.accept_sdk_license = True
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
