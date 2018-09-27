from setuptools import setup, find_packages
from glob import glob


def readme():
    with open('README.rst') as f:
        return f.read()



setup(
    name='mtaf',
    packages=find_packages(),
    author='Martin McCrorey',
    version='1.0.48',
    license='MIT',
    url='https://github.com/mccrorey48/mtaf',
    description='Mobile Test Automation Framework with Appium Inspector GUI for Android Applications',
    author_email = 'martin.mccrorey@verizon.net',
    entry_points={
        'console_scripts': [
            'mtaf-inspector=mtaf:start_inspector',
            'mtaf-web-inspector=mtaf:start_web_inspector',
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
        'babel==2.6.0',
        'beautifulsoup4==4.6.1',
        'behave==1.2.6',
        'behave2cucumber==1.0.3',
        'ipaddress==1.0.22',
        'olefile==0.44',
        'requests==2.18.4',
        'Pillow==4.3.0',
        'psutil==5.4.6',
        'pymongo==3.3.1',
        'pyserial==3.3',
        'PyYAML==3.12',
        'selenium==3.8.0',
        'six==1.11.0',
        'spur==0.3.20',
        'spur==0.3.20',
        'tkfilebrowser==2.2.2'
    ],
    long_description=readme(),
    zip_safe=False,
    data_files=[
        ('mtaf/wav', glob('wav/*.wav'))
    ],
)
