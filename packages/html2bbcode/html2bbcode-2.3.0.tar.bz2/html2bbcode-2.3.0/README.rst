About
=====

HTML to BBCode converter

Usage
=====

Command line converter
----------------------

Input data will be read from the specified file and the result will be
written to the specified file using custom elements mapping::

    $ html2bbcode --map map.conf input.html output.bbcode

Input data will be read from the specified file and the result will be
written to the standart output::

    $ html2bbcode input.html

Input data will be read from the standard input and the result will be
written to the specified file::

    $ cat input.html | html2bbcode output.bbcode

Input data will be read from the standard input and the result will be
written to the standard output::

    $ cat input.html | html2bbcode

Mapping
-------

--map option used to extend and change the default mapping::

    [blockquote]
    start: [quote]
    end: [/quote]

Python module
-------------

>>> parser = HTML2BBCode()
>>> str(parser.feed('<ul><li>one</li><li>two</li></ul>'))
'[list][li]one[/li][li]two[/li][/list]'
>>> str(parser.feed('<a href="http://google.com/">Google</a>'))
'[url=http://google.com/]Google[/url]'
>>> str(parser.feed('<img src="http://www.google.com/images/logo.png">'))
'[img]http://www.google.com/images/logo.png[/img]'
>>> str(parser.feed('<em>EM test</em>'))
'[i]EM test[/i]'
>>> str(parser.feed('<strong>Strong text</strong>'))
'[b]Strong text[/b]'
>>> str(parser.feed('<code>a = 10;</code>'))
'[code]a = 10;[/code]'
>>> str(parser.feed('<blockquote>Beautiful is better than ugly.</blockquote>'))
'[quote]Beautiful is better than ugly.[/quote]'

