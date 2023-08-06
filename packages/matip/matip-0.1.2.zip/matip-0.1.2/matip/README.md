Matip is an open source,test automation tool for native and hybrid apps,
tested on emulators and real devices.

Supported Python Versions
=========================
        
 * Python 2.6, 2.7
 * Python 3.2, 3.3

Installing
==========
        
If you have `pip <http://www.pip-installer.org>`_ on your system, you can simply install or upgrade the Python bindings::
        
	pip install -U matip
        
Alternately, you can download the source distribution from `PyPI <http://pypi.python.org/pypi/matip>`,unarchive it, and run::
        
	python setup.py install
        
Note: both of the methods described above install `matip` as a system-wide package  That will require administrative/root access to ther machine.  You may consider using a `virtualenv <http://www.virtualenv.org/>`_ to create isolated Python environments instead.
        
Example :
==========

* open a native apps

::

    from matip import driver

    capabilities = {}
    capabilities["app"] = "c:/selendroid-test-app.apk"
    capabilities["device"] = "0123456789ABCDEF"
    capabilities["model"] = "native"

    driver = driver.MobileDriver(capabilities)

    ...
    
    driver.quit()
