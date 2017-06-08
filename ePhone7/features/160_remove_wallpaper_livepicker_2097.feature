Feature: LiveWallpaperspicker.apk should not be present on ePhone7 (R2D2-2097)

  Scenario: use the package manager to verify the LiveWallpaperspicker apk is not installed
    Given I use the spud serial interface to list the installed packages
    Then  The package com.android.wallpaper.livepicker is not listed