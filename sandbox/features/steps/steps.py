from behave import *
from mtaf import mtaf_logging
from mtaf.user_exception import UserException as Ux
from mtaf.decorators import Trace
log = mtaf_logging.get_logger('mtaf.test')


@step("I run a step with no substeps")
def i_run_a_step_with_no_substeps(context):
    log.info("I run a step with no substeps")


@step("I run a step with a failing substep")
def i_run_a_step_with_a_failing_substep(context):
    context.run_substep("failing substep")
    # context.run_substep("and also this")


@step("I run a step with a passing substep")
def i_run_a_step_with_a_passing_substep(context):
    context.run_substep("passing substep")
    # context.run_substep("and also this")
    # assert True


@step("I run a step with a fake substep")
def i_run_a_step_with_a_fake_substep(context):
    context.run_substep("fake substep")
    # context.run_substep("and also this")
    # assert True


@step("I run a step with fake and passing substeps")
def i_run_a_step_with_a_fake_substep(context):
    context.run_substep("fake substep")
    context.run_substep("and also this")
    # assert True


@step("failing substep")
def failing_substep(context):
    assert False, "failed this one"


@step("passing substep")
def passing_substep(context):
    assert True


@step("fake substep")
def fake_substep(context):
    pass

@Trace(log)
def throw():
    raise Ux("raised User Exception")

@step("this happens")
def this_happens(context):
    log.info("nothing to see here")
    throw()


@step("and also this")
def and_also_this(context):
    log.info("nothing to see here")


@step("I run a step with failing then passing substeps")
def step_impl(context):
    context.run_substep("failing substep")
    context.run_substep("passing substep")


@step("I run a step with substeps that have substeps")
def step_impl(context):
    context.run_substep("I run a step with fake and passing substeps")
