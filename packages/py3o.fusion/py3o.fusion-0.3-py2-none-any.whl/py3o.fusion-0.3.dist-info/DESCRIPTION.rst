Introduction
============

py3o.fusion is a web server that provides simple but important services:

  - transform your `py3o.template`_ LibreOffice templates
    into final LibreOffice documents.
  - transform OpenOffice / LibreOffice documents to any supported format

Basically you can fusion a templated OpenOffice / LibreOffice document into any
supported format (ODT, DOC, DOCX, PDF)

This is intended to avoid direct dependencies in your own applications.
This also opens up the py3o ecosystem to other programming
languages than Python.

Deployment
==========

We recommend using the docker images we created. This is by far the quickest
to get a full conversion service up and running without hassle.

Just follow the instructions from our page on the `docker hub`_

Using it
========

You can use any language.

Here is the simplest example possible::

    # import the wonderful requests lib
    # if you need to intall it just try
    # pip install --upgrade requests
    import requests

    # define where is your py3o.fusion endpoint
    url = 'http://localhost:8765/form'

    # open up the file and stuff it into a dictionary
    # tmpl_file is a required field on the form. If you don't give
    # it to the endpoint you'll receive an error back from it.
    files = {
        'tmpl_file': open('templates/simple.odt', 'rb')
    }

    # then prepare the other fields of the form
    # those 3 fields are also mandatory and failing to POST
    # one of them will get you an error back from the server
    #
    # In this example you can see we leave the datadictionary
    # and the image_mapping empty... This is because we won't
    # send a template to the server but a simple plain
    # old ODT file
    fields = {
        "targetformat": 'PDF',
        "datadict": "{}",
        "image_mapping": "{}",
    }

    # finally POST our request on the endpoint
    r = requests.post(url, data=fields, files=files)

    # don't forget to close our orginal odt file
    files['tmpl_file'].close()

    # see if it is a success or a failure
    # ATM the server only returns 400 errors... this may change
    if r.status_code == 400:
        # server says we have an error...
        # this means it properly catched the error and nicely
        # gave us some info in a JSON answer...
        # let's use this fact
        print r.json()

    else:
        # if we're here it is because we should receive a new
        # file back

        # let's stream the file back here...
        chunk_size = 1024

        # fusion server will stream an ODT file content back
        outname = 'request_out.%s' % 'pdf'
        with open(outname, 'wb') as fd:
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)

        # warn our dear user his file is ready
        print "Your file: %s is ready" % outname

grab the full `odt2pdf.py source from here`_ and the `example ODT from here`_ here is a way to do this in one step::

    $ mkdir -p templates && wget https://bitbucket.org/faide/py3o.fusion/raw/055770694c0c4c1593aed156149d2d43a6042913/py3o/fusion/static/examples/odt2pdf.py && wget https://bitbucket.org/faide/py3o.fusion/src/055770694c0c4c1593aed156149d2d43a6042913/py3o/fusion/static/examples/templates/simple.odt?at=default && mv simple.odt templates/

Here is a more complicated example that fusions a datadictionary into a templated ODT using py3o.template and gives you back the resulting PDF. You'll note you can also override an image inside the template::

    # you'll need to install requests to make this example work
    # pip install --upgrade requests
    # should do the trick
    import requests
    import json

    # point the client to your own py3o.fusion server
    url = 'http://localhost:8765/form'

    # target formats you want... can be ODT, PDF, DOC, DOCX
    targetformats = ["ODT", "PDF", "DOC", "DOCX"]


    class MyEncoder1(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Item):
                obj = obj._asdict()
            else:
                obj = super(MyEncoder1, self).default(obj)

            return obj


    class Item(object):
        def _asdict(self):
            return self.__dict__


    items = list()

    item1 = Item()
    item1.val1 = 'Item1 Value1'
    item1.val2 = 'Item1 Value2'
    item1.val3 = 'Item1 Value3'
    item1.Currency = 'EUR'
    item1.Amount = '12345.35'
    item1.InvoiceRef = '#1234'
    items.append(item1)

    for i in xrange(1000):
        item = Item()
        item.val1 = 'Item%s Value1' % i
        item.val2 = 'Item%s Value2' % i
        item.val3 = 'Item%s Value3' % i
        item.Currency = 'EUR'
        item.Amount = '6666.77'
        item.InvoiceRef = 'Reference #%04d' % i
        items.append(item)

    document = Item()
    document.total = '9999999999999.999'

    data = dict(items=items, document=document)

    data_s = json.dumps(data, cls=MyEncoder1)

    for targetformat in targetformats:
        # open the files you need
        files = {
            'tmpl_file': open('templates/py3o_example_template.odt', 'rb'),
            'img_logo': open('images/new_logo.png', 'rb'),
        }

        # fusion API needs those 3 keys
        fields = {
            "targetformat": targetformat,
            "datadict": data_s,
            "image_mapping": json.dumps({"img_logo": "logo"}),
        }

        # and it needs to receive a POST with fields and files
        r = requests.post(url, data=fields, files=files)

        # TODO: handle error codes
        if r.status_code == 400:
            # server says we have a problem...
            # let's give the info back to our human friend
            print r.json()

        else:
            chunk_size = 1024
            # fusion server will stream an ODT file content back
            ext = targetformat.lower()
            with open('request_out.%s' % ext, 'wb') as fd:
                for chunk in r.iter_content(chunk_size):
                    fd.write(chunk)

        files['tmpl_file'].close()
        files['img_logo'].close()


And voila. You have a file called out.odt that contains the final odt 
fusionned with your data dictionary.

For the full source code + template file and images just download
them from `our repo`_

If you just want to test it rapidly you can also point your browser 
to the server http://localhost:8765/form and fill the form manually.

Changelog
=========

0.3 sep. 12 2014
~~~~~~~~~~~~~~~~

  - Added examples that can be downloaded from the feature page of the server itself.

0.2 sep. 11 2014
~~~~~~~~~~~~~~~~

  - Fixed an error case when the caller specified an invalid image mapping. The error was catched on the server but not sent back the the client.

0.1 sep. 11 2014
~~~~~~~~~~~~~~~~

  - Initial release

.. _py3o.template: http://py3otemplate.readthedocs.org
.. _our repo: https://bitbucket.org/faide/py3o.fusion
.. _docker hub: https://registry.hub.docker.com/u/xcgd/py3o.fusion/
.. _odt2pdf.py source from here: https://bitbucket.org/faide/py3o.fusion/raw/055770694c0c4c1593aed156149d2d43a6042913/py3o/fusion/static/examples/odt2pdf.py
.. _example ODT from here: https://bitbucket.org/faide/py3o.fusion/src/055770694c0c4c1593aed156149d2d43a6042913/py3o/fusion/static/examples/templates/simple.odt?at=default


