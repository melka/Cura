Cura Makerbot Edition
====

Python
--------

brew uninstall python
brew install python --universal --framework


Virtualenv
--------

http://docs.python-guide.org/en/latest/dev/virtualenvs/

pip install virtualenv
virtualenv Cura-15.01-RC5-Makerbot
cd Cura-15.01-RC5-Makerbot
source bin/activate


Git
--------

http://stackoverflow.com/questions/791959/download-a-specific-tag-with-git
http://stackoverflow.com/questions/2411031/how-do-i-clone-into-a-non-empty-directory

git init
git remote add origin https://github.com/daid/Cura
git fetch
git checkout 15.01-RC5 -b 15.01-RC5-Makerbot


wxPython
--------

http://umforum.ultimaker.com/index.php?/topic/7577-cura-mac-os-x-sources-compil/

cd wxPython-src-3.0.1.1/wxPython
python build-wxpython.py --osx_cocoa --mac_arch=i386,x86_64 --install

Create file */Users/melka/Drive/ESAAA/Projets/Cura-15.01-RC5-Makerbot/bin/pythonw* with the following content:
    #!/bin/bash
    ENV=`python -c "import sys; print sys.prefix"`
    PYTHON=`python -c "import sys; print sys.real_prefix"`/bin/python
    export PYTHONHOME=$ENV
    exec $PYTHON "$@"

[quit terminal and reopen]

cd /Users/melka/Drive/ESAAA/Projets/Cura-15.01-RC5-Makerbot
source bin/activate

wxPython patches for Yosemite
https://github.com/KiCad/KicadOSXBuilder/issues/40


power
--------

cd power-1.3
python setup.py build
python setup.py install

"super has no attribute init" error
https://bitbucket.org/ronaldoussoren/pyobjc/issue/110/subclass-of-nsobject-super-has-no


Python packages
--------

cd /Users/melka/Drive/ESAAA/Projets/Cura-15.01-RC5-Makerbot
pip install -r requirements.txt
pip install -r requirements_darwin.txt

modulegraph error
https://bitbucket.org/jinnko/py2app/commits/dba244c843397345d2bac8cdfc92ba9d66192bfc


debug
--------

cd /Users/melka/Drive/ESAAA/Projets/Cura-15.01-RC5-Makerbot
pythonw -m Cura.cura


Package
--------

cd /Users/melka/Drive/ESAAA/Projets/Cura-15.01-RC5-Makerbot
./package.sh darwin