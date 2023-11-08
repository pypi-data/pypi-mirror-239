from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'Geolocator using Photon API'
LONG_DESCRIPTION = 'Uses the photon api to get geolocation services'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="flu_geolocator", 
        version=VERSION,
        author="Adrian Fluturel",
        author_email="<adrian.fluturel@protonmail.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=["requests"], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'geolocation', 'photon', 'flu'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 3",
            "Operating System :: Microsoft :: Windows",
        ]
)