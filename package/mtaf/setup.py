from setuptools import setup, find_packages
from docutils.core import publish_cmdline
from glob import glob


def readme():
    with open('README.rst') as f:
        return f.read()


publish_cmdline(writer_name='html', argv=['README.rst', 'README.html'])

setup(
    name='mtaf',
    packages=find_packages(),
    author='Martin McCrorey',
    version='1.0.38',
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
        'olefile==0.44',
        'Pillow==4.3.0',
        'pymongo==3.3.1',
        'selenium==3.8.0',
        'PyYAML==3.12',
        'six==1.11.0',
        'requests==2.18.4',
        'pyserial==3.3',
        'spur==0.3.20'
    ],
    long_description=readme(),
    zip_safe=False,
    data_files=[
        ('mtaf/wav', glob('wav/*.wav'))
    ],
)
