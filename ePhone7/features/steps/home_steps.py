from behave import *
from ePhone7.views import *


@step("[home] I get the logo element from the home screen")
def home__i_get_the_logo_element_from_the_home_screen(context):
    context.logo_element = home_view.get_logo_element()


@step("[home] the logo width is at least {width} pixels")
def home__the_logo_width_is_at_least_width_pixels(context, width):
    assert int(context.logo_element.size['width']) >= int(width)


