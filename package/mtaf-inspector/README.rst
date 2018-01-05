MTAF Inspector
--------------

The MTAF Inspector is part of the  Mobile Test Automation Framework (MTAF),
a package for creating regression tests that use Selenium and Appium to test
web and mobile applications. (See "Mobile Test Automation Framework", below).

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

From the main GUI, the user can query the Android device using the ID or
zpath value to get a reference to the selected elements, and then obtain
additional information about the elements such as text content, position,
size, etc.

----

Features
========
- Graphical tool to assist in designing end-to-end tests on Android devices
- Works with Android device emulators, or Android devices via USB connection
- Interactively determines valid locators for screen elements, for use with
  Appium
- When no Appium server is present, grabs screenshots and xml via ADB
- When used with Appium server, finds and manipulates visible screen
  elements
- Records Appium interactions in a log file
- Loads plugins to extend menus, zpaths and GUI elements for specific
  applications (examples to be added in future releases)

----

Running Inspector
=================

After running "pip install mtaf-inspector", the mtaf-inspector executable
Python script will be on the current path.

Before running mtaf-inspector, verify that these requirements have been met:

- adb can be found on the current path
- an Appium server is running on the local machine
- an Android device or emulator is listed in the output of "adb devices"
- the current directory is suitable for the mtaf-inspector to create folders

and write temporary files

From the command prompt, just run "mtaf-inspector". MTAF Inspector will create
several subdirectories in the current working directory:

- "xml" (for the xml file captured from the device)
- "csv" (for the csv file generated from the xml)
- "log" (for general logging)
- "tmp" (for recorded commands and a history of locators used)
- "screenshot" (for the screenshot file captured from the device)

Inspector presents a GUI with these components (from top to bottom):

- a menu bar with drop-down menus for both Appium and ADB operations
- buttons and other controls for performing various operations that require Appium
- an input field for entering arbitrary Python commands that will be run in the global context when the "exec" button is clicked
- a scrolling text window that displays captured standard output
- a scrolling text window that displays recorded commands
- a bar with "screenshot" and "quit" buttons

The buttons and controls requiring Appium, along with the Appium drop-down menu,
are disabled until Appium is started. Click "Start Appium" on the menu
bar to start the Appium client and enable the GUI elements that require Appium.

Clicking the "screenshot" button will capture a screenshot from the Android
device and display it in a new window, along with two locator columns.  The left
column will list any resource id's present in the current view. The right
column will display a minimum unique zpath for each element in the current
view.

If Appium has been started, it will be used to obtain the screenshot and xml
from the device; otherwise adb will be used.

Not all elements have resource IDs, and some resource IDs may be shared by
multiple elements. Clicking a resource id will:

- highlight any elements on the screenshot that have that resource id attribute
- load the "find element" locator field in the main GUI with the resource ID
- highlight the corresponding zpaths in the right column

By design, each element has one corresponding minimum zpath. Clicking a zpath
will:

- highlight the corresponding element on the zpath
- load the "find element" locator field in the main GUI with the zpath
- if the element has a resource ID attribute, the corresponding button in the resource ID column will be highlighted

----

Mobile Test Automation Framework
================================

The Mobile Test Automation Framework is a Python Page Object Model framework,
currently being used to test web and Android applications. It supports
unittest and BDD test case organization, with detailed logging of test
stepws and reporting of test results. It is also intended to eventually
support iOS applications with some additional modules.

The first release of the MTAF (package name: "mtaf") includes the MTAF
Inspector, described above. The rest of the framework's components will
be included once they have been refactored for general release. See
http://pypi.org/project/mtaf/ for details.

