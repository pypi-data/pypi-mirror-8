from setuptools import setup

setup(
    name = 'winbrew',
    version = '1.1.0',
    author = 'Matt Fichman',
    author_email = 'matt.fichman@gmail.com',
    description = ('Native package installer for Windows'),
    license = 'MIT',
    keywords = ('installer', 'windows', 'package'),
    url = 'http://github.com/mfichman/winbrew',
    packages = ['winbrew'],
    entry_points = {
        'console_scripts': (
            'winbrew = winbrew.execute:main'
        )
    }
)
    
    
    
    
