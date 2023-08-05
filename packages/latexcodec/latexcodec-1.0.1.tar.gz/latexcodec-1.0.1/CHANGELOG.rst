1.0.1 (24 September 2014)
-------------------------

* br"\par" is now decoded using two newlines (see issue #26, reported
  by Jorrit Wronski).

* Fix encoding and decoding of the ogonek (see issue #24, reported by
  beltiste).

1.0.0 (5 August 2014)
---------------------

* Add Python 3.4 support.

* Fix "DZ" decoding (see issue #21, reported and fixed by Philipp
  Spitzer).

0.3.2 (17 April 2014)
---------------------

* Fix underscore "\_" encoding (see issue #17, reported and fixed by
  Michael Radziej).

0.3.1 (5 February 2014)
-----------------------

* Drop Python 3.2 support.

* Drop 2to3 and instead use six to support both Python 2 and 3 from a
  single code base.

* Fix control space "\ " decoding.

* Fix LaTeX encoding of number sign "#" and other special ascii
  characters (see issues #11 and #13, reported by beltiste).

0.3.0 (19 August 2013)
----------------------

* Copied lexer and codec from sphinxcontrib-bibtex.

* Initial usage and API documentation.

* Some small bugs fixed.

0.2 (28 September 2012)
-----------------------

* Adding additional codec with brackets around special characters.

0.1 (26 May 2012)
-----------------

* Initial release.
