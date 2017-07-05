from cx_Freeze import setup,Executable
import sys
import os, shutil
os.chdir(os.path.split(sys.argv[0])[0])
if len(sys.argv)==1:
    sys.argv.append('build')

setup(name='cerutils',
    version='1.0',
    description='xmcp',
    executables=[Executable("main.pyw",base='Win32GUI')])

shutil.copy('exec.default.txt','build/exe.win32-3.4/exec.default.txt')
shutil.rmtree('build/exe.win32-3.4/tcl/tzdata')
shutil.rmtree('build/exe.win32-3.4/tcl/msgs')
shutil.rmtree('build/exe.win32-3.4/tcl/encoding')
shutil.rmtree('build/exe.win32-3.4/tk/demos')
shutil.rmtree('build/exe.win32-3.4/tk/images')
shutil.rmtree('build/exe.win32-3.4/tk/msgs')