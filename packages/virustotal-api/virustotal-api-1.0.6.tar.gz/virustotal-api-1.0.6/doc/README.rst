.. image:: https://raw.githubusercontent.com/blacktop/virustotal-api/master/doc/logo.png

virustotal-api
==============

.. image:: https://travis-ci.org/blacktop/virustotal-api.svg?branch=master
    :target: https://travis-ci.org/blacktop/virustotal-api

.. image:: https://badge.fury.io/py/virustotal-api.png
    :target: http://badge.fury.io/py/virustotal-api

.. image:: https://pypip.in/d/virustotal-api/badge.png
        :target: https://crate.io/virustotal-api/requests/

.. image:: https://img.shields.io/gittip/blacktop.svg
        :target: https://www.gittip.com/blacktop/

Virus Total Public/Private/Intel API

- https://www.virustotal.com/en/documentation/public-api/
- https://www.virustotal.com/en/documentation/private-api/
- https://www.virustotal.com/intelligence/help/automation/

Installation
------------

.. code-block:: bash

    $ pip install virustotal-api


Usage
-----
.. code-block:: python

    import json
    import hashlib
    from virus_total_apis import PublicApi as VirusTotalPublicApi

    API_KEY = 'Sign-Up for API Key at virustotal.com'

    EICAR = "X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*"
    EICAR_MD5 = hashlib.md5(EICAR).hexdigest()

    vt = VirusTotalPublicApi(API_KEY)

    response =  vt.get_file_report(EICAR_MD5)
    print json.dumps(response, sort_keys=False, indent=4)


Output:
-------
.. code-block:: json

    {
        "response_code": 200,
        "results": {
            "scan_id": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f-1397510237",
            "sha1": "3395856ce81f2b7382dee72602f798b642f14140",
            "resource": "44d88612fea8a8f36de82e1278abb02f",
            "response_code": 1,
            "scan_date": "2014-04-14 21:17:17",
            "permalink": "https://www.virustotal.com/file/275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f/analysis/1397510237/",
            "verbose_msg": "Scan finished, scan information embedded in this object",
            "sha256": "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f",
            "positives": 49,
            "total": 51,
            "md5": "44d88612fea8a8f36de82e1278abb02f",
            "scans": {
                "Bkav": {
                    "detected": true,
                    "version": "1.3.0.4959",
                    "result": "DOS.EiracA.Trojan",
                    "update": "20140412"
                },
                "MicroWorld-eScan": {
                    "detected": true,
                    "version": "12.0.250.0",
                    "result": "EICAR-Test-File",
                    "update": "20140414"
                },
                "nProtect": {
                    "detected": true,
                    "version": "2014-04-14.02",
                    "result": "EICAR-Test-File",
                    "update": "20140414"
                },
                ...<snip>...
                "AVG": {
                    "detected": true,
                    "version": "13.0.0.3169",
                    "result": "EICAR_Test",
                    "update": "20140414"
                },
                "Panda": {
                    "detected": true,
                    "version": "10.0.3.5",
                    "result": "EICAR-AV-TEST-FILE",
                    "update": "20140414"
                },
                "Qihoo-360": {
                    "detected": true,
                    "version": "1.0.0.1015",
                    "result": "Trojan.Generic",
                    "update": "20140414"
                }
            }
        }
    }

Testing
-------

To run the tests:

    $ ./tests

Documentation
-------------

Documentation is comming soon.

Contributing
------------

1. Fork it.
2. Create a branch (`git checkout -b my_virus_total_api`)
3. Commit your changes (`git commit -am "Added Something Cool"`)
4. Push to the branch (`git push origin my_virus_total_api`)
5. Open a [Pull Request](https://github.com/blacktop/virustotal-api/pulls)
6. Wait for me to figure out what the heck a pull request is...
