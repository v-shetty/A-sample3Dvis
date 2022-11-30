from cx_Freeze  import setup, Executable
from setuptools import find_namespace_packages

build_exe_options = {
      "optimize": 0,
      "packages": ["OpenGL"],
      "excludes": ["PyQt6"],
      "include_files": ["FFTwindow.npy", "BRAMData.npz", ("scipy.libs", "lib/scipy.libs")]}

pkgs = find_namespace_packages(include=["controller*", "model*", "Resources*", "view*", "Visualizer3D*", "DLL*"])

setup(name='Contrller-GUI-A',
      version='1.2.0',
      packages=pkgs,
      url='',
      license='',
      author='ScantinelPhotonics',
      author_email='',
      description='',
      install_requires=[
            'toml',
            'numpy',
            'PyQt5',
            'qdarkstyle',
            'qt_material',
            'pyqtgraph',
            'PyOpenGL',
            'matplotlib',
            'serial',
            'paramiko',
            "scipy"
      ],
      include_package_data=True,
      options={"build_exe": build_exe_options},
      executables=[Executable("Visualizer3D/main_app_single.py", base=None), Executable("app.py", base=None)])
