from setuptools import setup

setup(
    name='taskwarrior-hook-time-tracking',
    version='0.1.1',
    url='https://github.com/coddingtonbear/taskwarrior-hook-time-tracking',
    description=(
        'Track your time in a UDA in taskwarrior'
    ),
    author='Adam Coddington',
    author_email='me@adamcoddington.net',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages=['time_tracking_hook'],
    entry_points={
        'console_scripts': [
            'taskwarrior_timetracking = time_tracking_hook:cmdline'
        ],
    },
)
