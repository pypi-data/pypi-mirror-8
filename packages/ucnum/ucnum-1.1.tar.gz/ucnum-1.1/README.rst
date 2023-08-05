===============
Unicode Numbers
===============

The ucnum program is a command line utility which allows you to convert decimal, octal, hexadecimal, and binary numbers; Unicode character and block names; and HTML/XHTML character entity names and numbers into one another. It can be used as an on-line special character reference for Web authors.

This version is a (blind) reimplementation of the original unum Perl utility by Gisle Aas (https://www.fourmilab.ch/webtools/unum/) in Python. It was written because it will stay up-to-date via Python’s own unicodedata updates. It has a few minor discrepancies:

1. The octal syntax 077 is not accepted: Use 0o77 instead.
2. Character information tables also contain the unicode block.
3. The regular expression flavour is Python’s.
4. The HTML escapes argument form is not accepted yet (see “TODO”).
5. Name aliases (e.g. for control characters) are not supported yet.

Arguments
=========

The command line may contain any number of the following forms of I<argument>:

123
	Decimal number.

0o371
	Octal number preceded by “0o”.

0x1D351
	Hexadecimal number preceded by “0x”. Letters may be upper or
	lower case, but the “x” must be lower case.

0b110101
	Binary number.

b=block
	Unicode character blocks matching block are listed.
	The block specification may be a regular expression.
	For example, “b=greek” lists all Greek character blocks
	in Unicode.

c=char...
	The Unicode character codes for the characters “char...” are printed.
	If the first character is not a decimal digit and the second not an
	equal sign, the “c=” may be omitted.

h=entity
	List all HTML/XHTML character entities matching entity, which may
	be a regular expression. Matching is case-insensitive, so
	“h=alpha” finds both “&Alpha;” and “&alpha;”.

l=block
	List all Unicode blocks matching block and all characters
	within each block; “l=goth” lists the Gothic block
	and the 32 characters it contains.

n=name
	List all Unicode character whose names match name, which may be
	a regular expression. For example, “n=telephone” finds the five
	Unicode characters for telephone symbols.

TODO
====

The following argument form is not yet accepted:

'&#number;&#xhexnum;...'
	List the characters corresponding to the specified HTML/XHTML
	character entities, which may be given in either decimal or
	hexadecimal. Note that the “x” in XHTML entities must be lower case.
	On most Unix-like operating systems, you'll need to quote the argument
	so the ampersand, octothorpe, and semicolon aren't interpreted by the
	shell.

Output
======

For number or character arguments, the value(s) are listed in all of the input formats, save binary::

	Octal  Decimal   Hex   HTML  Character        Block  Unicode
	 0o46       38  0x26  &amp;          &  Basic Latin  AMPERSAND


If the terminal font cannot display the character being listed, the “Character” field will contain whatever default is shown in such circumstances. Control characters are shown as a Python hexadecimal escape.

Unicode blocks are listed as follows::

	  Start         End  Unicode Block
	 0x2460  -   0x24ff  Enclosed Alphanumerics
	0x1d400  -  0x1d7ff  Mathematical Alphanumeric Symbols
	0x1f100  -  0x1f1ff  Enclosed Alphanumeric Supplement