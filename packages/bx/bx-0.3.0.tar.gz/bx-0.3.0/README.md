# Bx

In-memory storage for Python

![build-status](https://travis-ci.org/tylucaskelley/bx-python.svg?branch=master)
![version](https://pypip.in/version/bx/badge.svg)
![downloads](https://pypip.in/download/bx/badge.svg)

---

```
                  __
           ___~~~`  `~~__
     ___~~~              `~~_
     |~_                     `~_
     |  ~_               ___ ~~ |
     |    ~_        __~~~       |
     |      ~_ __~~~            |
     |        |                 |
     |        |                 |
     |        |       bx        |
      ~_      |               __|
         ~_   |          __~~~
           ~_ |     __~~~
             ~|__~~~
```

bx lets you store things in memory. It has a few special features:

* Thread safe
* Setting a timeout before object is destroyed
* JSON Schema validation
* Clean & simple API
* Badass ASCII art
* Supports Python 2.7 and 3.4

## Installation

Just make sure you have Python 2.7.x or 3.4.x and pip installed:

```bash
$ pip install bx
```

## Usage

The code is pretty simple and well-commented, but here's some example usage. If
you want more detail, run `pydoc bx.Db` once you've installed it or look through
the code to get info.

```python
import bx

student = {
    'title': 'student',
    'type': 'object',
    'required': ['name', 'major', 'gpa'],
    'properties': {
        'name': {
            'type': 'string'
        },
        'major': {
            'type': 'string'
        },
        'gpa': {
            'type': 'number'
        }
    }
}

# The schema argument defaults to None, and there is also an optional
# debug mode (for console logging) that defaults to False
db = bx.Db(schema=student)

try:
    db.put('bad', 'data')
except bx.db.ValidationError: # same as jsonschema.exceptions.ValidationError
    print('This does not fit the schema!')

john = {
    'name': 'John Doe',
    'major': 'Computer Science',
    'gpa': 3.6
}

susan = {
    'name': 'Susan Jones',
    'major': 'Physics',
    'gpa': 3.96
}

db.put('john', john)
db.put('susan', susan)

# get average gpa
print(sum([v['gpa'] for v in db.vals()]) / len(db.vals()))

db.delete('susan')

try:
    db.delete('bob')
except KeyError:
    print('bob is not in the data store!')
```
