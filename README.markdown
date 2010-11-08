Python port of the PHP [forge_fdf](http://www.pdfhacks.com/forge_fdf/) library by Sid Steward


PDF forms work with FDF data. I ported a PHP FDF library to Python a
while back when I had to do this and released it as fdfgen. I use that
to generate an fdf file with the data for the form, then use pdftk to
push the fdf into a PDF form and generate the output.

The whole process works like this:

You (or a designer) design the PDF in Acrobat or whatever and mark the
form fields and take note of the field names (I'm not sure exactly how
this is done; our designer does this step). Let's say your form has
fields "name" and "telephone".

Use fdfgen to create a FDF file:

    #!python
    from fdfgen import forge_fdf
    fields = [('name','John Smith'),('telephone','555-1234')]
    fdf = forge_fdf("",fields,[],[],[])
    fdf_file = open("data.fdf","w")
    fdf_file.write(fdf)
    fdf_file.close()

Then you run pdftk to merge and flatten:

    pdftk form.pdf fill_form data.fdf output output.pdf flatten

and a filled out, flattened (meaning that there are no longer editable
form fields) pdf will be in output.pdf.

