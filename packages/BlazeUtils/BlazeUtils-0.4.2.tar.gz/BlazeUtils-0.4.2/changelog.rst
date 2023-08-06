Changelog
---------

0.4.2 released 2014-12-08
================================

+ fix wrong dates for 0.4.0 and 0.4.1 releases in changelog
+ add roundsecs argument to dates.trim_mils
+ updates to spreadsheets module including .xlsx file support

    - xlsx_to_reader(): converts xlsxwriter.Workbook instance to xlrd reader
    - WriterX: like Writer but for xlsxwriter Worksheets, API is slightly different and won't have
      any faculties for style management like Writer does.
    - Reader: gets a .from_xlsx() method
    - http_headers(): utility function to help when sending files as HTTP response

0.4.1 released 2014-05-17
================================

+ fix packaging issue

0.4.0 released 2014-05-17
================================

+ testing.raises() gets support for custom exception validators, docstring updated w/ usage
+ decorators.curry() use a different approach so multiple curried functions can be used
+ add decorators.hybrid_method() ala SQLAlchemy
+ add decorators.memoize() primarily for SQLAlchemy method caching
+ BC break: .decorators now uses 'wrapt' so that is a new dependency

0.3.14 released 2013-12-17
================================

+ fix bug in xlrd.workbook_to_reader()
+ exc_emailer() now has print_to_stderr argument, defaults to True

0.3.13 released 2013-12-17
================================

+ fix bug which was always causing xlwt to be imported

0.3.12 released 2013-12-17
================================

+ add stderr output when exc_email() encounters an exception
+ add dates.trim_seconds()

0.3.11 released 2013-12-06
================================

+ DEPRECATE: xlrd.workbook_to_reader() moved to .spreadsheets
+ DEPRECATE: spreadsheets.XlwtHelper renamed to Writer
+ added spreadsheets.Reader
+ fix a deprecation warning bug in our error_handling.py tests
+ modified testing.raises() decorator to accept keyword args that will
  be converted into tests of attributes on the exception object
+ move package version to text file
+ add dates.trim_mils()
+ adjustments so deprecation warning always shows in testing


0.3.10 released 2013-06-10
==========================

+ added testing.mock_date*() methods
+ rst: breakout refid prefixing into separate prefix_refids()
+ rst: doctree2dict() now handles RST without doctinfo fields, renamed that
  function docinfo2dict(), but kept an alias for BC.
+ add xlrt.workbook_to_reader()
+ add XlwtHelper.write_merge()

0.3.9 released 2013-02-05
==========================

+ added numbers.ensure_int() and numbers.convert_int()
+ fix readme to have correct bitbucket URL to source

0.3.8 released 2012-03-22
==========================

+ added rst.create_toc() to generate a table of contents from a reST document
+ added some utility functions for reST processing with docutils
+ added testing.FailLoader to help when testing failed imports
+ ensure_datetime() now takes a time_part argument
+ added HTMLAttributes to new containers module, moved LazyDict to containers but
  left reference in datastructures.
+ make error_handling.raise_unexpected_import_error() more thorough and stop
  matching exceptions that shouldn't have been matched
+ add helpers.ensure_list() and ensure_tuple()

0.3.7 released 2011-12-15
==========================

+ (**BC BREAK**) changed testing.raises() to regex escape by default.  There is now a
  keyword arg to control regex escaping. Also switched it to be more lenient
  in its matching by using re.search() instead of re.match()
+ added exc_emailer() decorator
+ added testing.assert_equal_text()
+ add retry() decorator for retrying a function call when exceptions occur

0.3.6 released 2011-08-19
==========================

+ fix bug in sdist build

0.3.5 released 2011-08-18
==========================

+  XlwtHelper can now use XFStyle instances directly.

0.3.4 released 2011-06-11
==========================

+ deprecate error_handling.traceback_* functions
+ deprecate datetime module, moved safe_strftime to dates module
+ add decorators.deprecate() decorator
+ add testing.emits_deprecation() decorator (only usable w/ python >= 2.6)
+ add testing.raises() decorator
+ add dates module and ensure_date(), ensure_datetime()

0.3.3 released 2011-05-19
==========================
+ made moneyfmt/decimalfmt handle floats
