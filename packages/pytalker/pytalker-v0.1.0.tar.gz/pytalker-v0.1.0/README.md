	============================================================
	pytalker  Copyright (C) 2014  F. Brezo and Y. Rubio, i3visio
	============================================================

Description:
============
pytalker is a python module designed to wrap the TTS capabilities of the Google's TTS
service. It easily implements a wrapper for the Google TTS service.

License: GPLv3
==============

This is free software, and you are welcome to redistribute it under certain conditions.

	This program is free software: you can redistribute it and/or modify
	it under the terms of the GNU General Public License as published by
	the Free Software Foundation, either version 3 of the License, or
	(at your option) any later version.

	This program is distributed in the hope that it will be useful,
	but WITHOUT ANY WARRANTY; without even the implied warranty of
	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	GNU General Public License for more details.

	You should have received a copy of the GNU General Public License
	along with this program.  If not, see <http://www.gnu.org/licenses/>.


For more details on this issue, run:
```
	python pytalker-launcher.py --license
```

Installation:
=============
It requires the installation of gst libraries. You can check if you have the 
library installed by typing:
```
python -c "import gst"
```
If no errors where shown, you can go on with this tutorial. In any other case,
try to install this module manually. In Debian-like Linux distributions as 
follows:
```
sudo apt-get install python-gst0.1
```

The installation under Python 2.7 for the development package is as follows having
git installed:
```
git clone http://github.com/i3visio/pytalker
cd pytalker
sudo python setup.py build
sudo python setup.py install
```
or
```
wget http://github.com/i3visio/pytalker/archive/master.zip
unzip pytalker-master.zip
cd pytalker-master
sudo python setup.py build
sudo python setup.py install
```
Superuser privileges are required so as to complete the installation. Afterwards, 
the module will be importable from any python code. You can check this by typing:
```
python -c "import pytalker"
```
If no error is displayed, the installation would have been performed correctly.

Usage:
======
So as to run the program, navigate to pytalker-master/pytalker and run:
```
python pytalker-launcher.py -h
```
The usage is described as follows:
```
usage: pytalker-launcher.py [-h] -l <language> [<language> ...]
                            [-o <path_to_output_folder>] -t <text>
                            [<text> ...] (-d | -s) [--version]
```

The functionalities are described as follows:
```
optional arguments:
  -h, --help            show this help message and exit
  -d, --download        Downloading and playing the sound.
  -s, --say             Playing the input text.

Processing arguments:
  Configuring the processing parameters.

  -l <language> [<language> ...], --languages <language> [<language> ...]
                        list of languages to be used. E. g.: en, es, fr, etc.
  -o <path_to_output_folder>, --output_folder <path_to_output_folder>
                        path to the output folder where the results will be
                        stored.
  -t <text> [<text> ...], --text <text> [<text> ...]
                        text to be played between commas.

About arguments:
  Showing additional information about this program.

  --version             shows the version of the program and exists.

Note that the gst library should be installed on your system. In Debian-like
OS try: sudo apt-get install python-gst0.10
```
