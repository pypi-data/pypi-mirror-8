Pydouble
========

Description
-----------

Pydouble lets you search for duplicates on a local disk or on a network share. Duplicates are moved to a folder selected.

Pydouble can hash files md5 or sha1, identify duplicates and delete files based on their extension.

If only the source folder is selected, the program hash files only.

If the source folder and file duplicates are selected, the hash program and identifies duplicates. It moves duplicates in the selected folder.

If the source folder, the duplicates and remove extensions are selected then the hash program, identifies and removes duplicate files. Deleted files are permanently deleted.

Extensions must be in this form (separated by a space) in the field:

	jpg txt db gif tga

![](screenshot.png)

Installation
------------

**Windows**

You must install Python 2.7 and PySide 1.2.2 for Windows.

You can download packages at [http://www.lfd.uci.edu/~gohlke/pythonlibs/](http://www.lfd.uci.edu/~gohlke/pythonlibs/)

[Download egg file on pypi](https://pypi.python.org/pypi/pydouble)

And install

	python setup.py install

Or

	pip install -U pydouble

Finally you can download binary distribution [Exe (9MB)](http://shoota.org/pydouble/pydouble-1.4.zip).

**Linux**

Install source (quickly method)
	
	sudo apt-get install python-pyside
	git clone https://github.com/jhautefeuille/pydouble
	cd pydouble
	sudo python setup.py install

Install with pip (if PySide is not installed, it will be compiled and installed, require more time)

	sudo pip install -U pydouble



