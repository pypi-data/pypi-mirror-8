Provides a mixin class for Django's commands. This mixin adds a logger that
sets the appropriate log level.

Commands can be run with these args:

* -s: Silent, only showing log Warnings and Errors
* --extrasilent: Only show log messages marked Critical
* --debug: Show all log messages