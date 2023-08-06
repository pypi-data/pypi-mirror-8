This is repository is an improved version of htmlcutstring (https://code.google.com/p/cut-html-string/).
I'm not the original author.

Differences between original
============================
1. htmlcutstr has availability to count words instead of characters
2. It works fine on both Python 2.x and 3.x

Installation
============
Run ```setup.py install``` to install this package.

Usage
=====
cutHtmlString(string, limit, countType='c')

string is obviously the string you want to cut<br/>
limit maximum number of characters/words (depending on countType value) output string can have
countType can be equal to 'c' or 'w'
'c' means 'count by characters'
'w' means 'count by words'.

Examples
========
from htmlcutstr import cutHtmlString

htmlstring = '<div>insert your <a>text</a> here</div>'

print(cutHtmlString(htmlstring, 10)) # '<div>insert you</div>'
print(cutHtmlString(htmlstring, 3, 'w')) # '<div>insert your <a>text</a></div>'
