
from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages 
import glob, os.path, sys


# Path check
def which(command):
    percorso = os.getenv("PATH")
    directories = percorso.split(os.pathsep)
    for path_dir in directories:
        real_dir = os.path.expanduser(path_dir)
        try:
            lista_dir = os.listdir(real_dir)
        except OSError:
            lista_dir = []
        if os.path.exists(real_dir) and command in lista_dir:
            return os.path.join(real_dir, command)
    return None


# Look for script files
lscr = glob.glob(os.path.join('Scripts', 'SRP*'))
lscrex = []
for i in lscr:
    if os.path.splitext(i)[1] == '':
        lscrex.append(i)



import SRP.SRPFITS
durl = 'http://www.me.oa-brera.inaf.it/utenti/covino/SRPAstro.FITS-%s.tar.gz' % SRP.SRPFITS.__version__


setup(
    name='SRPAstro.FITS',
    namespace_packages = ['SRP'],
    version=SRP.SRPFITS.__version__,
    description='Tools for handling FITS files under SRP',
    packages = find_packages('.'),
    include_package_data = False,
    long_description='Set of tools to handle FITS files.',
    author='Stefano Covino', 
    author_email='stefano.covino@brera.inaf.it', 
    url='http://www.me.oa-brera.inaf.it/utenti/covino/SRPAstro.FITS.pdf',
    download_url=durl,    
    install_requires=['SRPAstro.FITS','SRPAstro','sep'],
    scripts=lscrex,
    zip_safe = False,
    classifiers=[ 
        'Development Status :: 5 - Production/Stable', 
        'Environment :: Console', 
        'Intended Audience :: Science/Research', 
        'License :: Freely Distributable', 
        'Operating System :: MacOS :: MacOS X', 
        'Operating System :: POSIX', 
        'Programming Language :: Python :: 2', 
        'Topic :: Scientific/Engineering :: Astronomy', 
        ], 
    ) 

