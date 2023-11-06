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

**TL;DR:** Overrides only the `dumps()` function of the standard `json` module.  It sets default arguments for 
`sort_keys` to `True` and `indent` to `4`, and also overrides the default encoder for the ability to serialize nearly 
anything and returns `null` on failure to serialize instead of throwing an exception, unless the argument 
`raise_on_error` is set to `True`.

But walls of text suck, so let's just jump right into examples.  First, let's start with the problems we're solving.

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
- when you do json.dumps(), you'll get pretty printed output by default (similar to pprint)
- objects like datetime that the standard json module will throw an Exception on will serialize correctly
- the other functions that come with the standard json module are included and are unmolested, so once you do: `import giga_json as json`, you can do json.load(), json.loads(), etc like you would with the standard module.
- the serializer has an intelligent order of checks.  for example, it checks for mapping before it tries iteration.  and before mapping, it checks the object for any built-in serialization methods, like to_json(), json(), etc.  this ensures that not only will your object be successfully serialized, but it will try the best method first
- if a serialization match and attempt fails, the serializer is allowed to continue down the list in the case that another method might match and work for the given object, increasing the chance of successful serialization
- .og_dumps() is an alias to the standard json.dumps() method, completely unchanged, if you need it
- .flat_dumps() uses giga_json's custom serializer, but its output argument defaults match standard json module, which means no pretty printing (no line breaks and no indents).  this is for convenience.  you can use normal dumps and pass in None for indent and False for sort_keys, and you will get an identical outcome
- being a simple function override, giga_json's dumps() function still allows you to pass in your own indent and sort_keys value, as well as using default= to pass in your own custom serializer

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









