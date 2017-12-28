from setuptools import setup, find_packages
setup(
    name='mtaf',
    author='Martin McCrorey',
    version='1.0',
    description='Mobile Test Automation Framework',
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    keywords='android appium selenium adb uiautomator viewer gui'
)
