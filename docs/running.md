In general, Python executable files in the Mobile Test Automation Framework
(MTAF) are intended to be run in the top level "mtaf" directory,
so they can find modules that are imported from other locations in the MTAF
directory structure.

To run tests for a particular product (CCD, ePhone7 etc.), cd to the 
mtaf top level directory and run <product name>run_features.py (for
running python behave-format ".feature" files in the <product_name>/features
directory) or <product_name>/run_tests.py (for running python unittest-format
".py" files in the <product_name>/suites directory.

So, for example, to run mtaf/ePhone7/run_features.py, 

    - cd to "mtaf"
    - type "python ePhone7/run_features.py" + any needed arguments + <Enter>

There are also utilities and library module test programs which are run 
similarly; for example,
    
    - cd to "mtaf"
    - type "python ePhone7/utils/utils_test/appium_gui.py" <Enter>