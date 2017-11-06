@step('A fake step')
def step_impl(context):
    pass

@step('A real step')
def step_impl(context):
    x = 42

@step('A step with fake substep')
def step_impl(context):
    context.run_substep('A fake step')

@step('A step with real substep')
def step_impl(context):
    context.run_substep('A real step')
