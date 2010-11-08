""" port of the PHP forge_fdf library by Sid Steward (http://www.pdfhacks.com/forge_fdf/)

by Anders Pearson <anders@columbia.edu>
   at the Columbia Center For New Media Teaching and Learning
          <http://ccnmtl.columbia.edu/>
"""

def escape_pdf_string(ss):
    ss_esc = []
    for c in ss:
        if (ord(c) == 0x28 or
            ord(c) == 0x29 or
            ord(c) == 0x5c):
            ss_esc.append(chr(0x5c) + c)
        elif (ord(c) < 32) or (126 < ord(c)):
            ss_esc.append("%03o" % ord(c))
        else:
            ss_esc.append(c)
    return ''.join(ss_esc)

def escape_pdf_name(ss):
    ss_esc = []
    for c in ss:
        if (ord(c) < 33) or (126 < ord(c)) or (ord(c) == 0x23):
            ss_esc.append("#%02x" % ord(c))
        else:
            ss_esc.append(c)
    return "".join(ss_esc)

def handle_hidden(key,fields_hidden):
    if key in fields_hidden:
        return "/SetF 2 "
    else:
        return "/ClrF 2 "

def handle_readonly(key,fields_readonly):
    if key in fields_readonly:
        return "/SetFf 1 "
    else:
        return "/ClrFf 1 "

def handle_data_strings(fdf_data_strings,fields_hidden,fields_readonly):
    for (key,value) in fdf_data_strings:
        yield "<< /V (" + escape_pdf_string(value) + ") " + \
              "/T ("    + escape_pdf_string(key)   + ") " + \
              handle_hidden(key,fields_hidden)     + \
              handle_readonly(key,fields_readonly) + \
              ">> \n"    

def handle_data_names(fdf_data_names,fields_hidden,fields_readonly):
    for (key,value) in fdf_data_names:
        yield "<< /V /" + escape_pdf_name(value) + \
              " /T ("   + escape_pdf_string(key) + ") " + \
              handle_hidden(key,fields_hidden)   + \
              handle_hidden(key,fields_readonly) + \
              ">> \n"

def forge_fdf(pdf_form_url="",fdf_data_strings=[],fdf_data_names=[],
              fields_hidden=[],fields_readonly=[]):
    """ generates fdf string from fields specified

    pdf_form_url is just the url for the form
    fdf_data_strings and fdf_data_names are arrays of (key,value) tuples
      for the form fields. FDF just requires that string type fields be treated seperately
      from boolean checkboxes, radio buttons etc. so strings go into fdf_data_strings, and
      all the other fields go in fdf_data_names.
    fields_hidden is a list of field names that should be hidden
    fields_readonly is a list of field names that should be readonly

    the result is a string suitable for writing to a .fdf file.
    
    """
    fdf = [u'%FDF-1.2\n%\xe2\xe3\xcf\xd3\r\n'] 
    fdf.append(u"1 0 obj\n<< /FDF") 

    fdf.append(u"<< /Fields [ ") 
    fdf.append(u''.join(handle_data_strings(fdf_data_strings,fields_hidden,fields_readonly)))
    fdf.append(u''.join(handle_data_names(fdf_data_names,fields_hidden,fields_readonly)))
    fdf.append(u"] \n") 

    if pdf_form_url:
        fdf.append(u"/F (" + escape_pdf_string(pdf_form_url) + ") \n")

    fdf.append(u">> \n")
    fdf.append(u">> \nendobj\n")
    fdf.append(u"trailer\n<<\n/Root 1 0 R >>\n")
    fdf.append(u'%%EOF\n\x0a')

    return u''.join(fdf)

def unicodify(s):
    try:
        return unicode(s,'utf8')
    except:
        return s


if __name__ == "__main__":
    # a simple example of using fdfgen
    # this will create an FDF file suitable to fill in
    # the vacation request forms we use at work.
    
    from datetime import datetime
    fields = [('Name',u'Anders Pearson'),
              ('Date',datetime.now().strftime("%D")),
              ('Request_1',u'Next Monday through Friday'),
              ('Request_2',''),
              ('Request_3',''),
              ('Total_days',u'5'),
              ('emergency_phone',u'857-6309')]
    fdf = forge_fdf(fdf_data_strings=fields)
    fdf_file = open("vacation.fdf","w")
    fdf_file.write(fdf.encode('utf8'))
    fdf_file.close()
