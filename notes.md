# Notes on MTAF framework

Sometimes errors in running Python's "behave" module don't get reported by the run_features.py mechanism. It can be useful to run the regression test (or run with the wip tag on a problematic scenario) using the behave framework without the run_features wrapper.

- To run from the command line, 
  - Make sure the right virtualenv is active
  - cd to the mtaf directory 
  - run: 
      ```bash
	 behave -D ota_server=alpha --tags=regression --stop -k -f plain ePhone7/features
      ```
- To set up a "behave" run configuration in Pycharm, 
  - Open the Run-->Edit Configurations dialog
  - Click Behave in the left column. 
  - Then enter, 
    > features directory "<user home>/mtaf/ePhone7/features"
    > working directory "<user home>/mtaf"
    > params "-D ota_server=alpha --tags=regression --stop -k"
