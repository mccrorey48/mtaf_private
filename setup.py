from setuptools import setup, find_packages
setup(
    name='mtaf',
    packages=find_packages(),
    author='Martin McCrorey',
    version='1.0.2',
    url='https://github.com/mccrorey48/mtaf',
    description='Mobile Test Automation Framework',
    author_email = 'martin.mccrorey@verizon.net',
    keywords=['python', 'android', 'appium', 'selenium', 'adb', 'uiautomator', 'viewer', 'inspector', 'gui', 'locator', 'screenshot',
              'xpath', 'resource_id', 'page object model'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
    ],
    install_requires=[
        'Appium-Python-Client==0.25',
        'olefile==0.44',
        'Pillow==4.3.0',
        'selenium==3.8.0'
    ],
    long_description="""
Mobile Test Automation Framework (MTAF)
---------------------------------------

**Provides:**
    **Inspector**
        - Graphical tool to assist in designing end-to-end tests on Android devices
        - Works with Android device emulators, or Android devices via USB connection
        - Interactively determines valid locators for screen elements, for use with Appium
        - When no Appium server is present, grabs screenshots and xml via ADB
        - When used with Appium server, finds and manipulates visible screen elements
        - Records Appium interactions in a log file
        - Loads plugins to extend menus, zpaths and GUI elements for specific applications
    
    **MTAF Library Modules (Python):**
        - ADB
            For using ADB from Python, the pyand (https://github.com/ardevd/pyand) ADB module is included
            (which avoids the problem of "pip install" not recognizing modules hosted on github)
        - selenium_actions
            Defines SeleniumActions class for using Selenium methods
        - android_actions
            Defines AndroidActions class for using Appium Python Client methods
        - ios_actions (future)
            Defines IosActions class for using Appium Python Client methods
        - android_zpath
            Defines abbreviations used to convert Android xpaths (which can be quite long) to zpaths, a short 
            format that makes working with locators a lot easier
        - ios_zpath (future)
            Defines abbreviations used to convert iOS xpaths to zpaths
        - filters.py
            Filter functions used to narrow down lists of screen elements returned by the Appium Python Client 
            search methods
        - mtaf_logging
            Wrapper for Python logging
        - prune_logs
            Utility to limit number and/or age of timestamped logs retained
        - trace
            Decorators for logging method calls and return values
        - user_exception
            Defines UserException class for graceful exception handling in test code
        - softphone (future)
            Creates and manages SIP softphones to make and receive calls for testing devices that support voice calls
            
    **Page Object Model (future):**
        - Each visible view (called a "page") displayed by an application under test has a Python class
          which contains locators for that page, and methods to be called while that page is displayed
        - Locators for visible elements on the page are given names that convey the element's function
        - Each page class represents a separate namespace for locator names, so that names can be 
          re-used on other pages without conflict
        - Test steps are generally implemented by calling methods belonging to the current page's class,
          and these methods obtain locators from the locator namespace belonging to their class
        - Pages can inherit from a common base page class when they share common elements and functionality,
          in which case methods and locators are inherited from the base class unless overridden in the
          current page class
          
    **Python Unit Test (future):**
        - Test suite classes are structured using the Python unittest module conventions
        - Custom logging and tracing
        - Supports end-to-end testing of Web and Mobile applications
        
    **Python Feature Test (future):**
        - Tests are written in Gherkin language (feature/scenario/step format)
        - Uses the Python "behave" framework
        - Saves data in a MongoDB database to facilitate reporting test results using a web server
        - Supports end-to-end testing of Web and Mobile applications
        
    **Report Single Page Application (future):**
        - AngularJS application displays test results saved by Python Feature Test

""",
    zip_safe=False,
)
