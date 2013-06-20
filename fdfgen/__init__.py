# -*- coding: utf-8 -*-
"""
Port of the PHP forge_fdf library by Sid Steward
(http://www.pdfhacks.com/forge_fdf/)

Anders Pearson <anders@columbia.edu> at Columbia Center For New Media Teaching
and Learning <http://ccnmtl.columbia.edu/>
"""

__author__ = "Anders Pearson <anders@columbia.edu>"
__credits__ = ("Sébastien Fievet <zyegfryed@gmail.com>,"
               "Brandon Rhodes <brandon@rhodesmill.org>",
               "Robert Stewart <https://github.com/rwjs>")

import codecs


def smart_encode_str(s):
    """Create a UTF-16 encoded PDF string literal for `s`."""
    utf16 = s.encode('utf_16_be')
    safe = utf16.replace('\x00)', '\x00\\)').replace('\x00(', '\x00\\(')
    return ('{0}{1}'.format(codecs.BOM_UTF16_BE, safe))


def handle_hidden(key, fields_hidden):
    if key in fields_hidden:
        return "/SetF 2"
    else:
        return "/ClrF 2"


def handle_readonly(key, fields_readonly):
    if key in fields_readonly:
        return "/SetFf 1"
    else:
        return "/ClrFf 1"


def handle_data_strings(fdf_data_strings, fields_hidden, fields_readonly):
    for (key, value) in fdf_data_strings:
        if type(value) is bool and value:
            value = 'Yes'
        elif type(value) is bool and not value:
            value = 'Off'
        else:
            value = ' ({0})'.format(value)
        yield "<<\n/V{0}\n/T ({1})\n{2}\n{3}\n>>\n".format(
            smart_encode_str(value),
            smart_encode_str(key),
            handle_hidden(key, fields_hidden),
            handle_readonly(key, fields_readonly),
        )


def handle_data_names(fdf_data_names, fields_hidden, fields_readonly):
    for (key, value) in fdf_data_names:
        yield "<<\n/V /{0}\n/T ({1})\n{2}\n{3}\n>>\n".format(
            smart_encode_str(value),
            smart_encode_str(key),
            handle_hidden(key, fields_hidden),
            handle_readonly(key, fields_readonly),
        )


def forge_fdf(pdf_form_url="", fdf_data_strings=[], fdf_data_names=[],
              fields_hidden=[], fields_readonly=[]):
    """Generates fdf string from fields specified

    pdf_form_url is just the url for the form fdf_data_strings and
    fdf_data_names are arrays of (key,value) tuples for the form fields. FDF
    just requires that string type fields be treated seperately from boolean
    checkboxes, radio buttons etc. so strings go into fdf_data_strings, and
    all the other fields go in fdf_data_names. fields_hidden is a list of
    field names that should be hidden fields_readonly is a list of field names
    that should be readonly

    The result is a string suitable for writing to a .fdf file.

    """
    fdf = ['%FDF-1.2\n%\xe2\xe3\xcf\xd3\r\n']
    fdf.append("1 0 obj\n<<\n/FDF\n")

    fdf.append("<<\n/Fields [\n")
    fdf.append(''.join(handle_data_strings(fdf_data_strings,
                                           fields_hidden, fields_readonly)))
    fdf.append(''.join(handle_data_names(fdf_data_names, fields_hidden,
                                         fields_readonly)))
    fdf.append("]\n")

    if pdf_form_url:
        fdf.append("/F (" + smart_encode_str(pdf_form_url) + ")\n")

    fdf.append(">>\n")
    fdf.append(">>\nendobj\n")
    fdf.append("trailer\n\n<<\n/Root 1 0 R\n>>\n")
    fdf.append('%%EOF\n\x0a')

    return ''.join(fdf)


if __name__ == "__main__":
    # a simple example of using fdfgen
    # this will create an FDF file suitable to fill in
    # the vacation request forms we use at work.

    # Set defaults
    from datetime import datetime
    fields = [('Name', u'Anders Pearson'),
              ('Date', datetime.now().strftime("%D")),
              ('Request_1', u'Next Monday through Friday'),
              ('Request_2', ''),
              ('Request_3', ''),
              ('Total_days', 5),
              ('emergency_phone', u'857-6309')]

    # Parse command-line arguments
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--output", "-o",
        help="FDF File to output to",
        default='vacation.fdf',
        type=argparse.FileType('w'))
    parser.add_argument(
        "--fields", "-f",
        help="Fields used in form; syntax is fieldname=fieldvalue",
        default=fields,
        nargs='*')
    args = parser.parse_args()
    if args.fields is not fields:
        for e, x in enumerate(args. fields):
            args.fields[e] = x.split('=')
            args.fields[e][1] = unicode(args.fields[e][1])

    fdf = forge_fdf(fdf_data_strings=args.fields)
    args.output.write(fdf)
    args.output.close()
