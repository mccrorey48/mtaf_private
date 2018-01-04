Mobile Test Automation Framework (MTAF)
---------------------------------------

The first release of the Mobile Test Automation Framework (MTAF) includes
the MTAF Inspector, a tool to help write automated tests that use Appium
to communicate with Android applications.

MTAF Inspector creates a graphical user interface (GUI) to capture application
screenshots and calculate unique partial xpaths for displayed elements. The
resulting xpaths are converted to an abbreviated format called "zpath" to make
them shorter (Android xpaths can be quite long).

The user can select elements individually with a mouse click, or click and
drag a selection rectangle on the displayed screenshot to narrow down the
list of partial zpaths shown on the screen. Resource ID's are also displayed,
but some elements won't have one, and a resource ID may not represent a unique
element on the screenshot.

Clicking on an ID or xpath will outline the corresponding element(s) on the
screenshot, and copy the ID or zpath value to the main GUI.

The main GUI can call use Appium to find elements matching the ID or zpath
value, and show information about the elements.

Inspector is part of an overall test automation framework that is currently
being used to test web and Android applications. This Python Page
Object Model supports unittest and BDD test case organization and
reporting of results. It is also intended to eventually support iOS
applications with some additional modules. These components will be included
once they have been refactored for general release.

----

Features
========
**MTAF Inspector:**
    - Graphical tool to assist in designing end-to-end tests on Android devices
    - Works with Android device emulators, or Android devices via USB connection
    - Interactively determines valid locators for screen elements, for use with
      Appium
    - When no Appium server is present, grabs screenshots and xml via ADB
    - When used with Appium server, finds and manipulates visible screen
      elements
    - Records Appium interactions in a log file
    - Loads plugins to extend menus, zpaths and GUI elements for specific
      applications

**MTAF Library Modules (Python):**
    - ADB
        For using ADB from Python, the pyand (https://github.com/ardevd/pyand)
        ADB module is included (which avoids the problem of "pip install" not
        recognizing modules hosted on github)
    - selenium_actions
        Defines SeleniumActions class for using Selenium methods
    - android_actions
        Defines AndroidActions class for using Appium Python Client methods
    - ios_actions (future)
        Defines IosActions class for using Appium Python Client methods
    - android_zpath
        Defines abbreviations used to convert Android xpaths (which can be quite
        long) to zpaths, a short format that makes working with locators a lot
        easier
    - ios_zpath (future)
        Defines abbreviations used to convert iOS xpaths to zpaths
    - filters.py
        Filter functions used to narrow down lists of screen elements returned
        by the Appium Python Client search methods
    - mtaf_logging
        Wrapper for Python logging
    - prune_logs
        Utility to limit number and/or age of timestamped logs retained
    - trace
        Decorators for logging method calls and return values
    - user_exception
        Defines UserException class for graceful exception handling in test code
    - softphone (future)
        Creates and manages SIP softphones to make and receive calls for testing
        devices that support voice calls

**Page Object Model (future):**
    - Each visible view (called a "page") displayed by an application under test
      has a Python class which contains locators for that page, and methods to
      be called while that page is displayed
    - Locators for visible elements on the page are given names that convey the
      element's function
    - Each page class represents a separate namespace for locator names, so that
      names can be re-used on other pages without conflict
    - Test steps are generally implemented by calling methods belonging to the
      current page's class, and these methods obtain locators from the locator
      namespace belonging to their class
    - Pages can inherit from a common base page class when they share common
      elements and functionality, in which case methods and locators are
      inherited from the base class unless overridden in the current page class

**Python Unit Test (future):**
    - Test suite classes are structured using the Python unittest module
      conventions
    - Custom logging and tracing
    - Supports end-to-end testing of Web and Mobile applications

**Python Feature Test (future):**
    - Tests are written in Gherkin language (feature/scenario/step format)
    - Uses the Python "behave" framework
    - Saves data in a MongoDB database to facilitate reporting test results
      using a web server
    - Supports end-to-end testing of Web and Mobile applications

**Report Single Page Application (future):**
    - AngularJS application displays test results saved by Python Feature Test

----

Running Inspector
=================

Once mtaf has been installed, inspector can be run from a script if the
following requirements are met:

- adb can be found on the current path
- an Appium server is running on the local machine (optional)
- the script has permission to write in the current working directory

Inspector can be started with these two Python script lines::

    from mtaf.inspector import start
    start()

Inspector will create several subdirectories in the current working directory:
- "xml" (for the xml file captured from the device)
- "csv" (for the csv file generated from the xml)
- "log" (for general logging)
- "tmp" (for recorded commands and a history of locators used)
- "screenshot" (for the screenshot file captured from the device)

Inspector presents a GUI with these components (from top to bottom):
- a menu bar with drop-down menus for both Appium and ADB operations
- buttons and other controls for performing various operations that
require Appium
- a input field for entering arbitrary Python commands that will be run in
the global context when the "exec" button is clicked
- a scrolling text window that displays captured standard output
- a scrolling text window that displays recorded commands
- a bar with "screenshot" and "quit" buttons

The buttons and controls requiring Appium, along with the Appium drop-down menu,
are disabled until Appium is started. With an Appium server
instance running on the local machine, click "Start Appium" on the menu
bar.

Click the "screenshot" button wil capture a screenshot and display unique zpaths
for each element on the display. Some elements may have resource id's,
displayed in a separate column. Clicking a resource id will highlight one or
more elements on the screenshot (preloading the "find element" locator field in
the main GUI), and corresponding zpaths will be highlighted. Clicking a zpath
will highlight one element (highlighting the corresponding resource ID if the
element has one) and preload the zpath into the "find element" locator field.
