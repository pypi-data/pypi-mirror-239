from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'For tracking time'
LONG_DESCRIPTION = 'All the things you need to easily track your time.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="time_stuff", 
        version=VERSION,
        author="Hayo Ottens",
        author_email="<hayo.ottens@gmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'time', 'time tracking'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)