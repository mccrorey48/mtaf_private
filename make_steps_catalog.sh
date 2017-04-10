#!/bin/bash
behave --steps-catalog ePhone7/features/steps|grep Given|cut -b 7- > steps.out
