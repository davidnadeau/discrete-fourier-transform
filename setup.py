from distutils.core import setup, Extension
setup(name='fouriertransform', version='1.0',  \
      ext_modules=[Extension('fouriertransform', ['fouriertransform.c'])])
