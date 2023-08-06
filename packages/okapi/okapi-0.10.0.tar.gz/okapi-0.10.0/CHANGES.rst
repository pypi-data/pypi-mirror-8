0.10.0 (2014-11-11)
-------------------
- New Features:

  - Don't hardcode the name of the database but expect it to be in
    the mongodb_uri parameter.

0.9.0 (2014-10-16)
------------------
- New Features:

  - Decouple okapi from requests so that any library following requests 
    interface can be used. This introduces a backward incompatible change
    because now the __init__ method for okapi Api class requires a new
    argument

0.8.0 (2014-09-26)
------------------
- New features:

  - Use one collection per project instead of saving all projects in the same collection
  - Add a time_bucket attribute to make time based queries faster

0.7.1 (2014-07-28)
----------------
- Bug Fixes:

	-Make sure to raise the exception if an error occurs so the user know 
	exactly what is happening instead of code crashing
