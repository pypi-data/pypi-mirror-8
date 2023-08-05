from distutils.core import setup
from distutils.core import Extension
from distutils.command.install import install
from distutils.command.build import build
from distutils.command.build_ext import build_ext

import subprocess
import shutil
import glob
import os

class build_ext_subclass( build_ext ):
    def build_extensions(self):
        print "Testing for std::tr1::shared_ptr..."
        try:
            self.compiler.compile(['test_std_tr1_shared_ptr.cpp'])
            self.compiler.define_macro("HAVE_STD_TR1_SHARED_PTR")
            print "...found"
        except:
            print " ...not found"

        print "Testing for std::shared_ptr..."
        try:
            self.compiler.compile(['test_std_shared_ptr.cpp'], extra_preargs=['-std=c++0x']),
            self.compiler.define_macro("HAVE_STD_SHARED_PTR")
            print "...found"
        except:
            print "...not found"

        build_ext.build_extensions(self)

long_description=''
with open('LICENSE') as file:
    license = file.read();

setup(name='quickfix',
      version='1.14.3',
      py_modules=['quickfix', 'quickfixt11', 'quickfix40', 'quickfix41', 'quickfix42', 'quickfix43', 'quickfix44', 'quickfix50', 'quickfix50sp1', 'quickfix50sp2'],
      data_files=[('share/quickfix', glob.glob('spec/FIX*.xml'))],
      author='Oren Miller',
      author_email='oren@quickfixengine.org',
      maintainer='Oren Miller',
      maintainer_email='oren@quickfixengine.org',
      description="FIX (Financial Information eXchange) protocol implementation",
      url='http://www.quickfixengine.org',
      download_url='http://www.quickfixengine.org',
      license=license,
      include_dirs=['C++'],
      cmdclass = {'build_ext': build_ext_subclass },
      ext_modules=[Extension('_quickfix', glob.glob('C++/*.cpp'), extra_compile_args=['-std=c++0x'])],
)
