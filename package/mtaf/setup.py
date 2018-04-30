from setuptools import setup, find_packages
from glob import glob


def readme():
    with open('README.rst') as f:
        return f.read()



setup(
    name='mtaf',
    packages=find_packages(),
    author='Martin McCrorey',
    version='1.0.42',
    license='MIT',
    url='https://github.com/mccrorey48/mtaf',
    description='Mobile Test Automation Framework with Appium Inspector GUI for Android Applications',
    author_email = 'martin.mccrorey@verizon.net',
    entry_points={
        'console_scripts': [
            'mtaf-inspector=mtaf:start_inspector',
        ],
    },
    keywords=['python', 'android', 'appium', 'selenium', 'adb', 'uiautomator', 'viewer', 'inspector', 'gui', 'locator', 'screenshot',
              'xpath', 'resource_id', 'page object model'],
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Natural Language :: English',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Testing',
        'Topic :: Software Development :: Quality Assurance',
    ],
    install_requires=[
        'Appium-Python-Client==0.25',
        'behave==1.2.6',
        'olefile==0.44',
        'requests==2.18.4',
        'Pillow==4.3.0',
        'pymongo==3.3.1',
        'pyserial==3.3',
        'PyYAML==3.12',
        'selenium==3.8.0',
        'six==1.11.0',
        'spur==0.3.20'
    ],
    long_description=readme(),
    zip_safe=False,
    data_files=[
        ('mtaf/wav', glob('wav/*.wav'))
    ],
)
