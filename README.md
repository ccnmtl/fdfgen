# fdfgen

[![Build Status](https://travis-ci.org/ccnmtl/fdfgen.svg?branch=master)](https://travis-ci.org/ccnmtl/fdfgen)

Python port of the PHP [forge_fdf](http://www.pdfhacks.com/forge_fdf/) library by Sid Steward

PDF forms work with FDF data. I ported a PHP FDF library to Python a while back when I had to do this and released it as fdfgen. I use that to generate an fdf file with the data for the form, then use [`pdftk`](http://www.pdflabs.com/tools/pdftk-server/) to push the fdf into a PDF form and generate the output.

## QUICK INSTALL

    pip install fdfgen

## HOW IT WORKS

1. You (or a designer) design the `form.pdf` in Acrobat.
2. Mark the form fields and take note of the field names. This can be done either through Acrobat or by installing pdftk and entering the command line

        pdftk [pdf name] dump_data_fields

3. Let's say your form has fields "name" and "telephone".

    Use fdfgen to create a FDF file:

        #!/usr/bin/env python
        from fdfgen import forge_fdf
        
        fields = [('name', 'John Smith'), ('telephone', '555-1234')]
        fdf = forge_fdf("",fields,[],[],[])
        
        with open("data.fdf", "wb") as fdf_file:
            fdf_file.write(fdf)

4. Then you run pdftk to merge and flatten:

       pdftk form.pdf fill_form data.fdf output output.pdf flatten

    and a filled out, flattened (meaning that there are no longer editable form fields) pdf will be in `output.pdf`.

## CHANGELOG

* 0.16.1 -- 2017-11-21 -- Fix `TypeError` in python 3.6 by Tom Grundy (@caver456)
* 0.16.0 -- 2017-02-22 -- Allow for different values for each checkbox by <bil.bagpuss@gmail.com>
* 0.15.0 -- 2016-09-23 -- Encode field names as UTF-16 fix by Andreas Pelme <andreas@pelme.se>
* 0.14.0 -- 2016-08-09 -- Adobe FDF Compatibility added by Cooper Stimson (@6C1)
* 0.13.0 -- 2016-04-22 -- python 3 bugfix from Julien Enselme <julien.enselme@ioda.net>
* 0.12.1 -- 2015-11-01 -- handle alternative checkbox values fix from Bil Bas <https://github.com/Spooner>
* 0.12.0 -- 2015-07-29 -- python 3 bugfixes
* 0.11.0 -- 2013-12-07 -- python 3 port from Evan Fredericksen
* 0.10.2 -- 2013-06-16 -- minor code refactor and added command line options from Robert Stewart <https://github.com/rwjs>
* 0.10.1 -- 2013-04-22 -- unbalanced paren bugfix from Brandon Rhodes <brandon@rhodesmill.org>
* 0.10.0 -- 2012-06-14 -- support checkbox fields and parenthesis in strings from Guangcong Luo <zarelsl@gmail.com>
* 0.9.2  -- 2011-01-12 -- merged unicode fix from Sébastien Fievet <zyegfryed@gmail.com>

## RUNNING TESTS:

* Create a virtual environment
* tox is required to run the tests. You can install the correct version with
  `pip install -r requirements-tests.txt`
* Run `tox` to run tests for all Python versions.
* To run a specific test and specific Python versions, you may use `tox -e py27
  -- tests/test_encoding.py`
