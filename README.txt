The first release of the Mobile Test Automation Framework (MTAF) includes
the MTAF Inspector, a tool to help write automated tests that use Appium
to communicate with Android applications.

Inspector written in Python, and creates a graphical user interface (GUI) to
capture application screenshots and calculate unique partial xpaths for
displayed elements. The resulting xpaths are converted to an abbreviated format
called "zpath" to make them shorter (Android xpaths can be quite long).

The user can select elements individually with a mouse click, or click and drag
rectangles on the displayed screenshot to narrow down the list of partial zpaths
shown on the screen. Resource ID's are also displayed, but may not represent a
unique element on the screenshot. Clicking on an ID or xpath will outline the
corresponding element(s) on the screenshot, and copy the ID or zpath value to
the main GUI.

The main GUI can call use Appium to find elements matching the ID or zpath
value, and show information about the elements.

Inspector is part of an overall test automation framework that is currently
being used to test web and Android applications. This Python Page
Object Model supports unittest and BDD test case organization and
reporting of results. It is also intended to eventually support iOS
applications with some additional modules. These components will be included
once they have been refactored for general release.
