from setuptools import setup
from sys import platform


REQUIREMENTS = []

if platform.startswith('darwin'):
    REQUIREMENTS.append('pyobjc-core >= 2.5')


setup(
    name='nativeconfig',
    version='1.0.0',
    py_modules=['nativeconfig'],
    url='https://github.com/GreatFruitOmsk/nativeconfig',
    license='MIT License',
    author='Ilya Kulakov',
    author_email='kulakov.ilya@gmail.com',
    description="Cross-platform python module to store application config via"
                "native subsystems such as Windows Registry or NSUserDefaults.",
    platforms=["Mac OS X 10.6+", "Windows XP+", "Linux 2.6+"],
    keywords='config',
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
    ],
    install_requires=REQUIREMENTS,
    test_suite='tests'
)
