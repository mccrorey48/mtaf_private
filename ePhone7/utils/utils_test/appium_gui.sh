#!/usr/bin/env bash
. ~/virtualenv/mtaf_2_7/bin/activate
cd $MTAF_PATH
export PYTHONPATH=$MTAF_PATH
/usr/bin/env python $MTAF_PATH/ePhone7/utils/utils_test/appium_gui.py
