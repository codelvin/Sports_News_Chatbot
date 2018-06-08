import cgi
import cgitb

cgitb.enable()

form = cgi.FieldStorage()

input_text = form.getfirst("textinput", "0")
first = form.getvalue("textinput")

print "<p>%s</p>" % input_text
print "%s" % first