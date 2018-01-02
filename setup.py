from setuptools import setup, find_packages
setup(
    name='mtaf',
    author='Martin McCrorey',
    version='1.0',
    description='Mobile Test Automation Framework',
    packages=find_packages(),
    dependency_links=[
        'git+https://github.com/ardevd/pyand.git#egg=pyand'
    ],
    install_requires=[
        'Appium-Python-Client==0.25',
        'olefile==0.44',
        'Pillow==4.3.0',
        'selenium==3.8.0',
        'pyand'
    ],
    zip_safe=False,
    classifiers=[
        'Programming Language :: Python :: 2.7'
    ],
    keywords='android appium selenium adb uiautomator viewer gui'
)
