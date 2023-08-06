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

## API

The code is pretty simple and well-commented, but here's an overview and example
usage for each function. For more, feel free to look through the test suite as well.
