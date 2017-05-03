# json++
An extension of JSON with an emphasis on reusability 
## Installation
`pip install jpp`
## Usage
`jpp [-h] [-p PATH [PATH ...]] [-c] [-u USER_INPUT] file`  
For example, the following will write to stdout the generation of a json based on the given jpp file, `ex.jpp`:  
`jpp ex.jpp`
## Features (see [unit-tests](https://github.com/asherbar/json-plus-plus/blob/master/jpp/parser/unit_test/parser_ut.py) for more)
### Superset of JSON
This means any standard JSON is a valid JSON++ file
### Comments
Anything that comes after `#` is ignored.
### Referencing local values
`$> cat ex.jpp`  
`{
    "language": "en",
    "version": "1.2.3-" + local["language"]
}`   
`$> jpp ex.jpp`  
`{
    "language": "en",
    "version": "1.2.3-en"
}`
### Referencing imported values
Other jpp files can be imported at the head of a jpp document:  
`import other;`  
`{ "val": imported["other"]["val"] }`
