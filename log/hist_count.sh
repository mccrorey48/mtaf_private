#!/bin/bash
grep callhistory-drs drs_test.log|cut --delim=" " -f 2|cut -b 2-5|sort|uniq|wc -l
