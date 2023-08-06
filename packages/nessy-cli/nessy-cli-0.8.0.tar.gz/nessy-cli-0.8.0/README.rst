Nessy CLI
=========

Simple command line interface to the Nessy locking system.

Installation
------------

It is simplest to install via PyPI using:

::

    pip install nessy-cli

Usage
-----

For convenience, you should set the nessy server claims URL in your environment:

::

    export NESSY_CLAIMS_URL=http://nessy.example.com/v1/claims

If `NESSY_CLAIMS_URL` or `GENOME_NESSY_SERVER` are set in your environment,
then those will be used; otherwise, you will need to specify the URL on the
command line with the `--url` option.

To list active claims:

::

    nessy list --status active


To revoke claims matching a filter:

::

    nessy revoke --status active --min-active-duration 100000

To avoid a race condition while trying to revoke a specific claim on a
resource, you should add a filter on the active duration:

::

    nessy revoke --status active --min-active-duration 100000 --resource <RESOURCE>
