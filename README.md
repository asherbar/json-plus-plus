# json++
An extension of JSON with an emphasis on reusability 
## Installation (requires [pip](https://pypi.python.org/pypi/pip))
`pip install jpp`
## CLI Usage
```
usage: cli.py [-h] [-p PATH [PATH ...]] [-c] [-u USER_INPUT] file

positional arguments:
  file                  Path to main JSON++ file

optional arguments:
  -h, --help            show this help message and exit
  -p PATH [PATH ...], --path PATH [PATH ...]
                        One or more path to add to JSON++ path
  -c, --compact-print   If specified, will print the most compact version
  -u USER_INPUT, --user_input USER_INPUT
                        Optional user input values
```
### Basic usage
Write to stdout the generation of a json based on the given jpp file, `ex.jpp`:
`jpp ex.jpp`
### Add to path
`--path` option allows users to add specific locations to [JPP_PATH](#JPP_PATH)
### Print format
if the `--compact-print` option is given, the result JSON is printed in the most compact fashion.
### User Input
`--user_input` allows users to pass input, in JSON format, via CLI. See [User input](#User-input)
## Features (see [unit-tests](jpp/parser/unit_test/parser_ut.py) for more)   
Perhaps an [example](examples) is the best way to show the supported features of JSON++.  Assuming the following is the contents of `ex.jpp`:
```
# Comments support

# Referencing values in other files
import other;

# All data besides imports must be inside the global scope
{

    # Any standard JSON will do
    "standard json": {
        "hello": "world",
        "list": [1, 2, 3],
        "number": 3.14,
    },

    # Referencing other local values
    "local ref example": {
        "some val": 8,
        "same val": local["local ref example"]["some val"],  # evaluates "some val" to 8
        "nested": {
            "some val": 17
        },
        "nested_ref": local["local ref example"]["nested"]["some val"] + 3  # evaluates to 20
    },

    "remote import example": {
        "value from other file": imported["other"]["some val"]
    },

    # Dictionary extending
    "base dict": {
        "foo": 3
    },

    # "sub dict" has 2 entries: "foo": 3 and "bar": 12
    "sub dict" extends local["base dict"]: {
        "bar": 12
    }
}
``` 

... and assuming `other.jpp` contains the following:  
```
{
    "some val": 123
}
```

Then executing `jpp ex.jpp` will print the following to the standard output:
```
{
    "sub dict": {
        "foo": 3,
        "bar": 12
    },
    "base dict": {
        "foo": 3
    },
    "remote import example": {
        "value from other file": 123
    },
    "local ref example": {
        "nested_ref": 20,
        "nested": {
            "some val": 17
        },
        "same val": 8,
        "some val": 8
    },
    "standard json": {
        "number": 3.14,
        "list": [
            1,
            2,
            3
        ],
        "hello": "world"
    }
}
```

As can be seen, the printed result is a valid JSON with all of references and calculated values being replaced. 
### Where does JSON++ look for imported files?
What happens when a `jpp` file encounters an import statement, e.g., `import foo.bar.baz;`?
The parser will look for a file `foo.bar.jpp` in it's _path_.
#### JPP_PATH
Similar to [PYTHONPATH](https://docs.python.org/3/using/cmdline.html#envvar-PYTHONPATH), `JPP_PATH` is an environment variable which contains paths separated by `;`. By default, when the CLI is executed, the current directory is added to the path. Additionally, the user may add additional locations by using the `path` option when invoking the CLI.
E.g., consider the following commands being executed from a shell:
```
$> export JPP_PATH=~/foobar
$> cd ~/foo/bar
$> jpp example.jpp --path ~/foo/baz ~/qux/quux
```
When `jpp` is run, `JPP_PATH` looks like this:
```
JPP_PATH=~/foo/bar;~/foo/baz;~/qux/quux;~/foobar
```
Notice that the search is according to the _order_ of which the locations are specified. So, for example, if `example.jpp` contains the statement `import corge.grault;` then `~/foo/bar` is searched first, and only if not found does the parser search `~/foo/baz` and the rest, etc.
### User input
Sometimes certain values aren't know until runtime. For these kinds of situations JSON++ allows referencing user-given values. This is done by specifying the `--user_input` option, and using the `user_input` keyword in the your `jpp` document. E.g., assuming `example.jpp` contains the following:
```
{
    "version": user_input["version"],
    "cool feature supported": local["version"] >= "2.0"
}
```
Executing `jpp example.jpp -u '{"version": "2.3.1"}'` will give:
```
{
    "version": "2.3.1",
    "cool feature supported": true
}
```
Executing `jpp example.jpp -u '{"version": "1.9"}'` will give:
```
{
    "version": "1.9",
    "cool feature supported": false
}
```