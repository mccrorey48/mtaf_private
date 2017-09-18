from behave import *
from lib.wrappers import fake
import lib.logging_esi as logging
from lib.user_exception import UserException as Ux
from lib.wrappers import Trace
log = logging.get_logger('esi.test')


@step("I run a step with no substeps")
def i_run_a_step_with_no_substeps(context):
    log.info("I run a step with no substeps")


@step("I run a step with a failing substep")
@fake
def i_run_a_step_with_a_failing_substep(context):
    context.run_substep("failing substep")
    # context.run_substep("and also this")


@step("I run a step with a passing substep")
@fake
def i_run_a_step_with_a_passing_substep(context):
    context.run_substep("passing substep")
    # context.run_substep("and also this")
    # assert True

@step("I run a step with a fake substep")
@fake
def i_run_a_step_with_a_fake_substep(context):
    context.run_substep("fake substep")
    # context.run_substep("and also this")
    # assert True

@step("I run a step with fake and passing substeps")
@fake
def i_run_a_step_with_a_fake_substep(context):
    context.run_substep("fake substep")
    context.run_substep("and also this")
    # assert True


@step("failing substep")
def failing_substep(context):
    assert False, "failed this one"


@step("passing substep")
@fake
def passing_substep(context):
    assert True


@step("fake substep")
def fake_substep(context):
    pass


@step("this happens")
def this_happens(context):
    log.info("nothing to see here")


@step("and also this")
def and_also_this(context):
    log.info("nothing to see here")
