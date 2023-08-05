.. :changelog:

0.1.2 (2014-10-13)
+++++++++++++++++

* Fixed nested dictionary shim.
* More robust error handling in shell (still pretty fragile though)

0.1.0 (2014-10-12)
++++++++++++++++++

* PyPI Launch (holy crap: `pip3 install jsonconfigparser`)
* Minimum viable package (still plenty of errors and features to touch though)
* CLI functionality moved into main app
* Interactive Prompt functionality merged into master
* Several Bug Fixes:
    - Shim for nesting dictionaries.
    - Consolidated string for root node in several modules

0.0.7 (2014-10-12)
++++++++++++++++++

* Basic interactive prompt
    - Tab complete for commands
    - Added write command for prompt use
    - Handle exiting script with ^C followed by ^C again.
* Better type conversion support
* Moved CLI into package
* Improved docstrings on functions

0.0.5 (2014-11-12)
++++++++++++++++++

* Cleaned up commands module
* Added `act_on_path` and `set_on_path` functions
* Added initialization options on ``JSONConfigParser``
    - `storage`: A filepath to write to
    - `source`: Initial file to read from
* Replaced fragile, custom value parsing with more robust ``shlex.split``
* Tests added!
* Sorted out some imports
* Initial implementation of conversion functionality
* Updated CLI example

0.0.3 (2014-10-08)
++++++++++++++++++

* Added JSONpath support
* Added function registry with `command` and `call` support

0.0.1 (2014-10-07)
++++++++++++++++++

* Initial concept
