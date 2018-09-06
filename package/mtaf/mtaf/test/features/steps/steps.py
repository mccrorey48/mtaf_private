from behave import *


@step('A fake step')
def step_impl(context):
    """a triple-quoted docstring of one line"""
    pass


@step('A real step')
def step_impl(context):
    """ a triple-quoted docstring
    of two lines """
    x = 42


@step('A step with a {parameter} in the name')
def step_impl(context, parameter):
    """ a triple-quoted docstring
    of two lines """
    y = 11
    z = 22


@step('A step with a "{quoted_parameter}" in the name')
def step_impl(context, quoted_parameter):
    """ a triple-quoted docstring
    of two lines """
    y = 33
    z = 44


@step('Another real step')
def step_impl(context):
    """ a triple-quoted docstring
    of two lines """
    y = 99
    z = 100


@step('A step with a fake substep')
# a comment before the def
def step_impl(context):
    context.run_substep('A fake step')  # a comment at the end of the line


@step('A step with a real substep')
def step_impl(context):
    # a comment after the def
    context.run_substep('A real step')
    context.run_substep('Another step with a fake substep')


@step('Another step with a fake substep')
def step_impl(context):
    context.run_substep('A fake step')  # a comment at the end of the line

