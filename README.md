# json++
An extension of JSON with an emphasis on reusability 
## Installation
`pip install jpp`
## CLI Usage
`jpp [-h] [-p PATH [PATH ...]] [-c] [-u USER_INPUT] file`  
For example, the following will write to stdout the generation of a json based on the given jpp file, `ex.jpp`:  
`jpp ex.jpp`
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

