#from distutils.core import setup
#from distutils.extension import Extension
#from distutils.command.sdist import sdist as _sdist

from setuptools import setup
from setuptools import Extension
from setuptools.command.sdist import sdist as _sdist

from MUS import util

#borrowed from online code: http://stackoverflow.com/questions/4505747/how-should-i-structure-a-python-package-that-contains-cython-code
try:
    from Cython.Distutils import build_ext
except ImportError:
    useCython = False
else:
    useCython = True

import numpy as np

cmdClass = {}
extModules = []

if useCython:
    extModules += [Extension('MUSCython.BasicBWT', ['MUSCython/BasicBWT.pyx'], include_dirs=['.']),
                   Extension('MUSCython.ByteBWTCython', ['MUSCython/ByteBWTCython.pyx'], include_dirs=['.']),
                   Extension('MUSCython.GenericMerge', ['MUSCython/GenericMerge.pyx'], include_dirs=['.']),
                   Extension('MUSCython.LZW_BWTCython', ['MUSCython/LZW_BWTCython.pyx'], include_dirs=['.']),
                   Extension('MUSCython.MSBWTCompGenCython', ['MUSCython/MSBWTCompGenCython.pyx'], include_dirs=['.']),
                   Extension('MUSCython.MSBWTGenCython', ['MUSCython/MSBWTGenCython.pyx'], include_dirs=['.']),
                   Extension('MUSCython.MultimergeCython', ['MUSCython/MultimergeCython.pyx'], include_dirs=['.']),
                   Extension('MUSCython.MultiStringBWTCython', ['MUSCython/MultiStringBWTCython.pyx'], include_dirs=['.']),
                   Extension('MUSCython.RLE_BWTCython', ['MUSCython/RLE_BWTCython.pyx'], include_dirs=['.'])]
    cmdClass.update({'build_ext':build_ext})
    
    #this is also from the stackoverflow link above, used to auto-compile when you do the sdist command
    class sdist(_sdist):
        def run(self):
            # Make sure the compiled Cython files in the distribution are up-to-date
            from Cython.Build import cythonize
            cythonize('MUSCython/BasicBWT.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/ByteBWTCython.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/GenericMerge.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/LZW_BWTCython.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/MSBWTCompGenCython.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/MSBWTGenCython.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/MultimergeCython.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/MultiStringBWTCython.pyx', include_path=[np.get_include()])
            cythonize('MUSCython/RLE_BWTCython.pyx', include_path=[np.get_include()])
            _sdist.run(self)
    cmdClass['sdist'] = sdist
    
else:
    extModules += [Extension('MUSCython.BasicBWT', ['MUSCython/BasicBWT.c'], include_dirs=['.']),
                   Extension('MUSCython.ByteBWTCython', ['MUSCython/ByteBWTCython.c'], include_dirs=['.']),
                   Extension('MUSCython.GenericMerge', ['MUSCython/GenericMerge.c'], include_dirs=['.']),
                   Extension('MUSCython.LZW_BWTCython', ['MUSCython/LZW_BWTCython.c'], include_dirs=['.']),
                   Extension('MUSCython.MSBWTCompGenCython', ['MUSCython/MSBWTCompGenCython.c'], include_dirs=['.']),
                   Extension('MUSCython.MSBWTGenCython', ['MUSCython/MSBWTGenCython.c'], include_dirs=['.']),
                   Extension('MUSCython.MultimergeCython', ['MUSCython/MultimergeCython.c'], include_dirs=['.']),
                   Extension('MUSCython.MultiStringBWTCython', ['MUSCython/MultiStringBWTCython.c'], include_dirs=['.']),
                   Extension('MUSCython.RLE_BWTCython', ['MUSCython/RLE_BWTCython.c'], include_dirs=['.'])]

setup(name='msbwt',
      version=util.VERSION,
      description='Allows for merging and querying of multi-string BWTs for genomic strings',
      url='http://code.google.com/p/msbwt',
      author='James Holt',
      author_email='holtjma@cs.unc.edu',
      license='MIT',
      packages=['MUS', 'MUSCython'],
      install_requires=['pysam', 'numpy'],
      scripts=['bin/msbwt'],
      zip_safe=False,
      include_dirs=[np.get_include()],
      ext_modules=extModules,
      cmdclass = cmdClass)