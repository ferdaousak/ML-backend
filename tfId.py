txt = "bla bla blaé bla bla"
import re
regex = re.compile('[^a-zA-Z ]')
txt = regex.sub('',txt)
print(txt)