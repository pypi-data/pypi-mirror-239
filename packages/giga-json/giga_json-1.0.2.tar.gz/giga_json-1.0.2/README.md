```
    ▄███▀          ▄█                          ▄█                           ▀██▄
   ██▌             ▀▀                          ▀▀                             ▐██
   ██      ▄▄██▄▄▄ ▄▄   ▄▄██▄▄▄ ▄▄▄██▄▄  ▄▄  ▄▄▄▄▄  ▄█▄▄▄    ▄█▄▄  ▄▄▄ ▄▄█▄    ██
   ██    ▄██▀ ▀██▌ █▌ ▄██▀ ▀██▌ ▀▀▀  ▀██ ██    ▀█ ██  ▀▀█ ▄██▀ ▀██▄ ███▀▀▀██   ██
  ██▀    ██    ▐█▌ █▌ ██    ▐█▌      ▄██       ▐█ ██      ██     ██ █▌    ██   ▀██▄
▀█▄      ██    ▐█▌ █▌ ██    ▐█▌ ▄███▀▀██       ▐█  ▀███▄  ██     ██ █▌    ▐█▌    ▄██▀
  ██▄    ██    ▐█▌ █▌ ██    ▐█▌ █▌    ▐█       ▐█     ▀██ ██     ██ █▌    ▐█▌  ▄██▀
   ██    ▀██▄▄███▌ █▌ ▀██▄▄███▌ ██   ▄██ ██    ▐█ █▄  ▄██ ▐██▄ ▄██▀ █▌    ▐█▌  ██
   ██      ▀▀▀ ▐█▌ █▌   ▀▀▀ ▐█▌ ▀▀███▀▐█ ▀▀    ▐█ ▀▀██▀▀    ▀▀█▀▀   █▌    ▐█▌  ██
   ██▌   ▄▄    ██     ▄▄    ██            ▄▄   ▐█                             ▄██
    ▀▀██▄ ▀████▀       ▀████▀              ▀████▀                           ▄██▀
```

## Installation: `python -m pip install giga-json`

## What is it?

**TL;DR:** Imagine python's json module, except when you call json.dumps(your_object), it defaults to `indent=4, sort_keys=True`.  Also imagine having things like datetime objects in your dictionary, and doing a dumps, and not getting an exception.  Now imagine passing in objects like request module's response object, or pandas dataframes, or pytorch tensors, or flask's request object, and not only not raising an exception, but also serializing the data.  That's what this is.  But it's just a mild extension and override of what's still mostly just the standard python json module.

## Philosophy
Things I believe are important to software tools:
- The most commonly used settings/parameters/patterns should be the default
  - Most of the time, when I use json.dumps(), it's for quick troubleshooting.  I shouldn't need to type `indent=4, sort_keys=True` every time.
  - But since this is just an extension/inheritance of the standard module, you can still use those two arguments to get the desired output format.
- Adding convenience features can add value
  - as long as they don't involve a loss of other functionality
  - and as long as it doesn't come at the cost of reliability
  - and as long as it doesn't come at the cost of performance
JSON module doesn't serialize datetime objects
  - by serializing datetime objects by default to ISO format, most users get the outcome they want, and users that prefer another format can parse it in their code before it reaches our encoder
  - by never throwing an exception, the module doesn't become a burden
  - but by allowing this feature to be overridden, as with all features in giga-json, the users don't lose any functionality to gain this convenience

## Why?

Are you familiar with the below exception?
```bash
TypeError: Object of type datetime is not JSON serializable
```

Do you find yourself typing `indent=4, sort_keys=True` way too often?
```python
json.dumps(some_object, indent=4, sort_keys=True)
```

If you answered yes to one or both of those questions, you might be interested in using `giga_json`.  Let's see some real
examples.  A picture is worth a thousand words, so behold!

```python
>>> import giga_json as json
>>> from datetime import datetime
>>> 
>>> some_dict = {'timestamp': datetime.now()}
>>>
>>> print(json.dumps(some_dict))
{
  "timestamp": "2023-11-03T23:20:39.943919"
}
```

No more TypeError?  Indeed!  And there's much more!

```python
>>> import giga_json as json
>>> import requests
>>> 
>>> response = requests.get('https://catfact.ninja/fact')
>>> 
>>> print(json.dumps(response))
{
    "fact": "On average, cats spend 2/3 of every day sleeping. That means a nine-year-old cat has been awake for only three years of its life.",
    "headers": {
        "Access-Control-Allow-Origin": "*",
        "Cache-Control": "no-cache, private",
        "Connection": "keep-alive",
        "Content-Encoding": "gzip",
        "Content-Type": "application/json",
        "Server": "nginx",
        "Transfer-Encoding": "chunked",
        "Vary": "Accept-Encoding",
        "X-Content-Type-Options": "nosniff",
        "X-Frame-Options": "SAMEORIGIN",
        "X-Ratelimit-Limit": "100",
        "X-Ratelimit-Remaining": "98",
        "X-XSS-Protection": "1; mode=block"
    },
    "length": 129,
    "reason": "OK",
    "status_code": 200
}
```

Cool, right?  You will struggle to find things that `giga_json` will fail to serialize, especially for Python's most commonly used objects.  You also probably noticed that it pretty prints by default without having to set `indent=4`.

As long as you do the import like this: `import giga_json as json`, it will be a drop-in replacement for the standard json module, as far as usage syntax goes.  

What all can be serialized by giga_json's custom GigaEncoder?  All the things!  Ok probably not all, but it does cover most bases as you can see in this fairly extreme example:

```python
>>> from datetime import datetime
>>> from decimal import Decimal
>>> import giga_json as json
>>> 
>>> class room:
...     def __init__(self): self.data = {'pie': 'thawn'}
...     def __iter__(self): return iter(self.data)
...     def __getitem__(self, key): return self.data[key]
...     def items(self): return self.data.items()
... 
>>> giga_data = {
...     'math_things': [Decimal('3.141592654'), 9001, 4+2j, 0.02, hex(100)],
...     'bin_things': ['hello world!', b'bite me', bytearray(b'giga'), memoryview(bytearray(b'hello world'))],
...     'singleton_things': {True, False, None},
...     'object_things': (datetime.now(), room()),
...     'arrayish_things': (0, 1, [5, 4, {1, 2, range(3)}])
... }
>>> 
>>> print(json.dumps(giga_data))
{
    "arrayish_things": [
        0,
        1,
        [
            5,
            4,
            [
                [
                    0,
                    1,
                    2
                ],
                1,
                2
            ]
        ]
    ],
    "bin_things": [
        "hello world!",
        "bite me",
        [
            103,
            105,
            103,
            97
        ],
        "hello world"
    ],
    "math_things": [
        3.141592654,
        9001,
        "4 + 2i",
        0.02,
        "0x64"
    ],
    "object_things": [
        "2023-11-04T05:09:04.022359",
        {
            "pie": "thawn"
        }
    ],
    "singleton_things": [
        false,
        true,
        null
    ]
}

```

As an added convenience, you can use the flat_dumps() function to use giga_json's robust serializer/encoder, but default to flat output like the standard json module.  Calling this method is identical to calling `dumps(your_obj, indent=None, sort_keys=False)`.
```python
>>> print(json.flat_dumps(response))
{"fact": "Neutering a cat extends its life span by two or three years.", "length": 60}
```

This module retains all of the functionality of the standard json module if it's needed.  If you do: `import giga_json as json`, you will have immediate access to the vanilla json.load() and json.loads() functions.  While dumps() is overridden, I created an alias, so you can still access the original unmolested version by aliased name like this: `og_dumps()`

```python
>>> import giga_json as json
>>> print(json.og_dumps(my_dict))

Traceback (most recent call last):
TypeError: Object of type datetime is not JSON serializable
```

^ I don't know why you'd want to put yourself through that pain, but it's there if you need it! 😉

Since the point of this module is convenience, by just forcing anything and everything through the serializer, it returns null if all else fails, in order to keep your code from raising an exception.  But if you DO want it to raise an exception when it encounters an object it can't handle, use the `raise_on_error` argument for the `dumps()` function:

  - Default behavior trying to parse something that you can't serialize, like a function:
    - ```python
       >>> import giga_json as json
       >>>
       >>> json.dumps(some_func)
       '"<function some_func at 0x1012e0dc0>"'
       ```

  - Behavior if you set `raise_on_error=True`:
    - ```python
       >>> import giga_json as json
       >>>
       >>> json.dumps(some_func, raise_on_error=True)

       Traceback (most recent call last):
       TypeError: Object of type function is not JSON serializable.
      ```

## Behaviors
- if you do the import like this: `import giga_json as json`, it will be virtually identical to the standard json module.  json.load() and json.loads() are literally the vanilla functions
- the serializer has an intelligent order of checks.  for example, it checks for mapping before it tries iteration.  and before mapping, it checks the object for any built-in serialization methods, like to_json(), json(), etc.  this ensures that not only will your object be successfully serialized, but it will try the best method first
- if a serialization match and attempt fails, the serializer is allowed to continue down the list in case another method might match and work for the given object, increasing the chance of successful serialization
- .og_dumps() is an alias to the standard json.dumps() method, completely unchanged, if you need it
- .flat_dumps() uses giga_json's custom serializer, but its output argument defaults match standard json module, which means no pretty printing (no line breaks and no indents).  this is for convenience.  dumps() you'd probably use for troubleshooting, as it pretty prints, and you'd use this one for other purposes (like when you'd use jsonify)
- this literally just inherits from standard json module, so all the original features are there.  you can still change indent and sort_keys and even pass in your own encode using default=

## Supported Objects
**This list isn't exhaustive, as there are a lot of objects that would be handled by the various checks the encoder does, like looking for built-in serialization methods, checking for iteration dunder methods, etc.**

- bytes
- bytearray
- complex
- custom dict-like objects
- custom objects that contain built-in serializers
  - obj.json()
  - obj.to_json()
  - obj.to_JSON()
  - obj.as_json()
  - obj.get_json()
  - obj.serialize()
- date
- datetime
- Decimal
- Enum
- Flask.request
- frozenset
- Iterables
- Mappings
- MatPlotLib Plots
- memoryview
- named tuple
- NumPy
  - MaskedArray
  - dtype
  - matrix
  - ndarray
  - number
  - recarray
- Pandas
  - DataFrames
  - Index
  - Series
- PyTorch Tensor
- range
- Requests.Response
- SciPy Spare Matrix
- set
- TensorFLow Tensor
- UUID

## Examples

This is just an extension of the standard JSON module, so the syntax is identical.

```python
>>> import giga_json as json
>>> print(json.dumps({'hello': 'world!'}))
{
    'hello': 'world!'
}
```

load() and loads() functions are literally the stock ones, completely untouched/unchanged
```python
>>> import giga_json as json
>>> j1 = json.load(data_a)
>>> j2 = json.loads(data_b)
```

even the original dumps() function is included, but under an aliased name, should you need it:
```python
>>> import giga_json as json
>>> print(json.og_dumps({'hello': 'world!'}))
{'hello': 'world!'}
```

if you want giga-json's convenient encoder, but prefer the default flat output formatting of standard json module, use flat_dumps():
```python
>>> import giga_json as json
>>> from datetime import datetime
>>> print(json.flat_dumps({'timestamp': datetime.now()}))
{"timestamp": "2023-11-04T11:26:01.154089"}
```
