[app]

# (str) Title of your application
title = 优必选小微控制

# (str) Package name
package.name = ubtech_robot_control

# (str) Package domain (needed for android/ios packaging)
package.domain = org.ubtech

# (str) Source files where the main.py reside
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,json

# (list) List of inclusions using pattern matching
#source.include_patterns = assets/*,images/*.png

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec,pyc

# (str) Application versioning (method 1)
version = 1.0.0

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,kivymd,pyjnius,android,plyer,requests

# (str) Presplash of the application
presplash.filename = %(source.dir)s/assets/presplash.png

# (str) Icon of the application
icon.filename = %(source.dir)s/assets/icon.png

# (str) Supported orientation (one of 'landscape', 'portrait' or 'sensor')
orientation = portrait

# (list) List of service to declare
#services = NAME:ENTRYPOINT_TO_PY,service2:ENTRYPOINT2_TO_PY

#
# Android specific
#

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (string) Presplash background color (for android toolchain)
# Supported formats are: #RRGGBB #AARRGGBB or one of the following names:
# red, blue, green, black, white, gray, cyan, magenta, yellow, lightgray,
# darkgray, lightgrey, darkgrey, aquamarine, fuchsia, lime, maroon, navy,
# olive, purple, silver, teal.
android.presplash_color = #2C3E50

# (list) Permissions
android.permissions = BLUETOOTH, BLUETOOTH_ADMIN, BLUETOOTH_SCAN, BLUETOOTH_CONNECT, INTERNET, RECORD_AUDIO, ACCESS_NETWORK_STATE, ACCESS_WIFI_STATE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (int) Android NDK version to use
android.ndk = 25b

# (int) Android SDK version to use
android.sdk = 33

# (str) Android NDK directory (if empty, it will be automatically downloaded.)
#android.ndk =

# (str) Android SDK directory (if empty, it will be automatically downloaded.)
#android.sdk =

# (str) Android entry point, default is ok for Kivy-based app
android.entrypoint = org.kivy.android.PythonActivity

# (str) Android apptheme, is available only when android.new_architecture is set to true
# android.apptheme = "@android:style/Theme.NoTitleBar"

# (list) Android architecture(s)
android.archs = arm64-v8a,armeabi-v7a

# (bool) Enables Android NDK's NEON.
android.neon = 1

# (bool) Indicates whether the screen should stay on
# Don't forget to add the WAKE_LOCK permission if this is True
android.wakelock = 0

# (list) Android additional meta-data to add to <application> tag of AndroidManifest.xml
#android.meta_data =

# (list) Android additional libraries to unpack to libs
android.android_additional_libs =

# (bool) Indicate whether the screen should be kept on, so the backlight does not turn off
android.keep_native_orientation_on = 0

# (str) Path to a custom whitelist file
android.whitelist =

# (str) Path to a custom blacklist file
android.blacklist =

# (list) List of Android .gradle dependencies to add (using full jar path with a : followed by version)
#android.gradle_dependencies =

# (bool) Enable AndroidX support. Enable when using AndroidX libraries
android.enable_androidx = 1

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) overrides automatic version_code computation with a numeric value
android.numeric_version = 100

# (bool) indicates if the application should be compiled with .so files included
android.use_shared_libs = 1

#
# Python for android configuration
#

# (str) The android NDK version to use
p4a.bootstrap = sdl2

# (int) Number of worker threads to use while compiling. Use 'auto' to auto-detect.
p4a.num_jobs = auto

# (str) python-for-android fork to use
#p4a.fork =

# (str) python-for-android branch to use, defaults to master
#p4a.branch =

# (str) python-for-android specific commit to use, defaults to HEAD, must be within p4a.branch
#p4a.commit =

# (str) Extra recipes to pass through to python-for-android
#p4a.recipes =

# (str) Extra patches to apply to python-for-android modules
#p4a.patch =

# (list) python-for-android arguments to use for compiling
p4a.args =

# (str) Additional parameters to pass to p4a recipes
#p4a.extra_args =

# (str) Additional p4a arguments
#p4a.extra_args =

# (str) Custom recipe folders to include
#p4a.recipes_dir =

# (str) Python version to use
python.version = 3.9

# (str) Android entry point, default is ok for Kivy-based app
#android.entrypoint = org.kivy.android.PythonActivity

#
# Buildozer configuration
#

# (str) Path to buildozer spec file
#buildozer.spec =

# (str) Build output directory
buildozer.output_dir = ./bin

# (str) Build output filename
#buildozer.output_filename =

# (bool) If True, then buildozer will compile the debug version
buildozer.debug = 0

# (bool) If True, then buildozer will compile the release version
buildozer.release = 1

# (bool) If True, then buildozer will create a signed APK
buildozer.sign = 0

# (str) Path to keystore file
buildozer.keystore =

# (str) Keystore password
buildozer.keystore_password =

# (str) Key alias
buildozer.key_alias =

# (str) Key password
buildozer.key_password =
