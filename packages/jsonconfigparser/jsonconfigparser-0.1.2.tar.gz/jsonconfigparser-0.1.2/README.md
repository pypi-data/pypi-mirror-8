#JSONConfigParser
A JSON config editor built on top of [jsonpath-rw.](https://github.com/kennknowles/python-jsonpath-rw/).

##Installation

Simple as `pip install --user jsonconfigparser`

##Use
Right now there is an example of building a CLI utility in the examples directory.

It can also be used programmatically as well by importing the `JSONConfigParser` class and the commands modules.

###CLI App

This is built with argparse. Using it is as simple as:

    jsonconf path/to/conf.json view -p $

That command will view the entire JSON file. Other actions include:

| command  | description                                                                                                                           |                                                                                                                                                                                                                                |
|----------|---------------------------------------------------------------------------------------------------------------------------------------|--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| addfile  | Concatenates a second JSON file onto the current. Warning: This will overwrite any shared keys.                                       | `jsonconf conf.json addfile -o path/to/other.json`                                                                                                                                                                         |
| addfield | Adds a key and value to a specified JSONPath                                                                                          | `jsonconf conf.json addfield -p $.name -v jsonconfigparser`                                                                                                                                                                |
| append   | Appends a value to the specified JSONPath. Optionally, converts the field to another type. Optionally, apply to every found endpoint. | `jsonconf conf.json append -p $.things.[0] -v "Star bellied sneeches"`  `jsonconf conf.json append -p $.products.hats -v "23.44" -t float`  `jsonconf conf.json append -p $.products.[*].descript -v "A thing" -m` |
| delete   | Deletes an item from the specific JSONPath.                                                                                           | `jsonconf conf.json delete $.products.hats`                                                                                                                                                                                |
| edit     | Reset the value at the endpoint of the JSONPath                                                                                       | `jsonconf conf.json edit -p $.products.hats.descript -v "A really cool hat."`                                                                                                                                              |
| shell    | Drop into the interactive prompt.                                                                                                     | `jsonconf conf.json shell`   |

Arguments:

| flags        | description                                                                                                                                                                              |
|--------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| -p/--path    | The path flag the only acceptable value is a JSONPath string                                                                                                                             |
| -o/--other   | The other file flag, used with addfile to concatenate files together                                                                                                                     |
| -v/--value   | The value flag, used with any action that requires a value                                                                                                                               |
| -m/--multi   | The multi boolean flag. Currently only used with append action. Defaults to false, if True append will add the value to every path found                                                 |
| -c/--convert | The conversion flag. Currently only used with append. Defaults to False. If passed, a value must be provided of `int`, `float`, `list`, `dict`, `bool`,`str` or some combination of them |

###Interactive Shell Prompt

This is built with readlines. To enter it, simply run `jsonconf path/to/conf.json shell`

Executing commands is exactly the same as on the command line, except the shell can't be reinstantiated inside itself.

To exit, two consecutive keyboard interrupts are needed. If a command is run between them, then the exit flag is reset.

There is also an extra method available in the shell `write` which saves the current state of the file.

##Todo:
There are several things that I want to do, small and big:

* Apply the multiflag where needed.
* Clean up the whole package up and turn what I can into classes/objects.
* Ability to write to a different file for CLI and Shell.
