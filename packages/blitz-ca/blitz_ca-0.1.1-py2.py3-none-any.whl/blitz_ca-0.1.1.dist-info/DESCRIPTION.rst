Blitz CA
========
A tool for managing the signing and generation of CSRs as well as the creation of certificate Authorities

Features
---------
* Its not the openssl command
* Sane flags
* Its not the openssl command
* internal API to leverage in your own apps
* Its not the openssl command
* Single File Certificate store based off sqlite makes backups easy
* Human readable times that become more accurate as the appointed time gets closer
  eg '3 days from now' to '3 hours from now' to '03:14'
* Ability to add comments to certificates, keys and requests
* Generate CRLs'
* Webserver to provision new certificates to bearers of a valid (but soon to 
  expire) certificate allowing automatic update of certificates via a cronjob

Installation
-------------
To create a virtual environment use the following commands

    pyvenv-3.4 --system-site-packages venv
    . bin/venv/activate
    pip install blitz-ca

to activate the environment in another terminal repeat the activate step as shown below

    . bin/venv/activate

as this is an argparse based program, comprehensive help is available by specifying '-h' or '--help'
to receive help on a sub command, use '-h' as above after the sub command itself

At this time there is no other documentation avalible but those who have 
created certificates and CSRs with the openssl command should be fammilar 
enough with the terminolgy and process to use the program.

What Works
-----------
* Key Generation
* Cert Generation
* Request Generation
* Request Signing
* Arbitrary x509 extensions
* Subject alternative names
* Key usage
* RSA and DSA keys of arbitrary bit length

What does not Work
-------------------
* Tracking of issued certs
* CRL Generation
* Auto Enrolment webserver
* Confirmation before signing a request
* Elliptic Curve keys

Notes
------
* If you do not specify a key then one will be created for you automaticly as 
  part of the CSR or certificate generation. if you are having trouble matching a 
  CSR up to a private key at generation time, consider using the '-C' flag to add 
  a comment to both the private key and CSR

* Signing a request will copy extensions from the request into the certificate
  however there is currently no way to audit the request before signing and approve 
  extensions

* Certificates are backdated by 1 hour to help prevent issues with clients/servers 
  with clock drift (if you have 1 hour of clock drift you ahve bigger issues but
  daylight savigns may cause issues)


.. :changelog:

Release History
---------------

0.1.1 (2014-11-05)
++++++++++++++++

- Re-release to fix upload

0.1 (2014-11-05)
++++++++++++++++

- Initial Release
- Key generation
- Cert generation
- Request generation
- Request signing




