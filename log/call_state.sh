#!/bin/bash
grep -n Request\ msg\\\|Response\ msg\\\|RX\\\|\\\.name\\\|calling\\\|_on_state:\ \<sip\\\|_on_state:\ sip\\\|new\ call_status\\\|ending\ call esi_debug.log |cut -b 1-250
