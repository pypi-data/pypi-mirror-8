# hapi-vendor-toolkit

The HyperDNS Vendor Toolkit provides an environment for developing,
using, and managing multiple vendor drivers.  It provides a command
line utility which can let you manage multiple DNS vendors in a
consistent and robust fashion.  That same utility allows you to
create new drivers for new DNS service providers, and to extend and
enhance the facilities of your current driver suite.

## Github Pages Documentation

see http://hyperdns.github.io/hapi-vendor-toolkit for user friendly
documentation.

## Quickstart

We use python 3 and the toolkit is available on PyPI.
	
	virtualenv -p python3 .python
	. .python/bin/activate
    pip install hapi-vendor-toolkit
	nosetests
	
## Adding Vendors

You can use pip to install other hapi-vendors in your environment.
You could, for example, set up the ability manage multiple DNS vendors
from a single client system as follows:

	virtualenv -p python3 .python
	. .python/bin/activate
    pip install hapi-vendor-toolkit
	nosetests
    pip install hapi-vendor-r53
    pip install hapi-vendor-dyn
    pip install hapi-vendor-ultra


