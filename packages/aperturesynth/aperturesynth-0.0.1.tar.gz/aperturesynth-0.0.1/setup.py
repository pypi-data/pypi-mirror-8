from setuptools import setup

setup(
    name='aperturesynth',
    version='0.0.1',

    packages=['aperturesynth'],

    license='MIT',

    description='A tool for registering and combining series of handheld photographs',

    author='Sam Hames',
    author_email='samuel.hames@uqconnect.edu.au',
    url='https://github.com/SamHames/aperturesynth',

    install_requires=['scikit-image',
                    'matplotlib',
                    'numpy',
                    'docopt'],

    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: End Users/Desktop',
        'Topic :: Multimedia :: Graphics',
        'Topic :: Artistic Software',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        ],

    keywords='photography processing synthesis',

    entry_points={'console_scripts':['aperturesynth=aperturesynth.synthesise:main']}
                  )
