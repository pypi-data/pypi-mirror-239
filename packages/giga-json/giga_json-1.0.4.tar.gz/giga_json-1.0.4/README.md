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

<hr>

## Installation: `python -m pip install giga-json`

<hr>

## TL;DR:

Imagine python's json module.  And it pretty prints by default.  And it can serialize almost anything.  And objects it can't serialize return a null instead of throwing an exception.  Syntax is identical to vanilla json module because it just does very light extending and overriding of the standard module.  That's what this is.

## Philosophy
In my humble opinion:
- The most commonly used settings/parameters/patterns should be the default.
- Suppressing nuisance exceptions can be acceptable default behavior if you're able to override it.
- Adding convenience features can add value, as long as it doesn't come at the cost of stability, functionality, or performance.

Python's json module is great.  It gets the job done and has processed unfathomable amounts of data, every day.  But I find that I'm using it most often to do quick troubleshooting, and when that's the case, I usually want pretty printing, and I want sort keys.  But typing this every time becomes tiresome.  It's also tiring when you just need to quickly dump some output, but you get an exception because your dictionary contains a datetime object.

<hr>

# Enter the Rabbit Hole...

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

*(I removed the full setup code of the absurd example below, but you can see it in its entirety [here](documentation/bohemoth.md) if you're curious)*
```python
import giga_json as json

... see documentation/bohemoth.md for the full code for this silly example ...

bohemoth = {
    'Bytes': b'bite force',
    'Bytearray': bytearray(b'giga'),
    'Complex': 4+2j,
    'Custom dict-like object': room(),
    'Custom with built-in serialize': dismissed(),
    'Date': datetime.date(2023, 1, 1),
    'Datetime': datetime.datetime.now(),
    'Decimal': Decimal('3.141592654'),
    'Dict': {'map': 'all', 'the': 'things'},
    'Enum': MyEnum.A,
    'Flask.request (get)': flask_request_get,
    'Flask.request (post)': flask_request_post,
    'Float': 3.14,
    'Frozenset': frozenset([1, 2, 3]),
    'Hex': hex(100),
    'Int': 42,
    'Iterables': {1, 2},
    'List': [1, 2],
    'Mapping': {'any': 'mapping', 'types': 'parse'},
    'MatPlotLib.plot': mplp_plot,
    'Memoryview': memoryview(bytearray(b'hello world')),
    'Named tuple': CustomObject(),
    'NumPy.array': numpy.array([1, 2, 3]),
    'NumPy.int': numpy_array,
    'NumPy.dtype': numpy_array.dtype,
    'NumPy.masked_array': numpy.ma.masked_array([1, 2], mask=[False, True]),
    'NumPy.recarray': numpy_recarray,
    'Pandas.DataFrame': pandas.DataFrame({'a': [1, 2], 'b': [3, 4]}),
    'Pandas.Series': pandas.Series([1, 2, 3], index=['a', 'b', 'c']),
    'Pandas.Index': pandas.Index([1, 2, 3]),
    'PyTorch.Tensor': torch.tensor([[1, 2], [3, 4]]),
    'Range': range(3),
    'Requests.Response': requests.get('https://catfact.ninja/fact'),
    'SciPy.compressed_sparse_row_matrix': csr_matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]]),
    'Set': {1,2,3},
    'Singletons': (True, False, None),
    'String': 'hello mars!',
    'TensorFlow.Tensor': tensorflow.constant([[1, 2], [3, 4]]),
    'Tuple': (1, 2),
    'UUID': uuid.uuid4()
}
print(json.dumps(bohemoth))
```

output:
```json
{
    "Bytearray": [
        103,
        105,
        103,
        97
    ],
    "Bytes": "bite force",
    "Complex": "4 + 2i",
    "Custom dict-like object": {
        "pie": "thawn"
    },
    "Custom with built-in serialize": {
        "cake": "lie"
    },
    "Date": "2023-01-01",
    "Datetime": "2023-11-06T18:32:50.912921",
    "Decimal": 3.141592654,
    "Dict": {
        "map": "all",
        "the": "things"
    },
    "Enum": 1,
    "Flask.request (get)": {
        "body": {
            "param": "value"
        },
        "headers": {
            "Host": "localhost",
            "User-Agent": "UnitTest"
        },
        "http_method": "GET",
        "ip_address": "127.0.0.1",
        "url": "http://localhost/test?param=value",
        "user_agent": "UnitTest"
    },
    "Flask.request (post)": {
        "body": {
            "key": "value"
        },
        "headers": {
            "Content-Length": "16",
            "Content-Type": "application/json",
            "Host": "localhost",
            "User-Agent": "UnitTest"
        },
        "http_method": "POST",
        "ip_address": "127.0.0.1",
        "url": "http://localhost/test",
        "user_agent": "UnitTest"
    },
    "Float": 3.14,
    "Frozenset": [
        1,
        2,
        3
    ],
    "Hex": "0x64",
    "Int": 42,
    "Iterables": [
        1,
        2
    ],
    "List": [
        1,
        2
    ],
    "Mapping": {
        "any": "mapping",
        "types": "parse"
    },
    "MatPlotLib.plot": [
        {
            "x": [
                1,
                2,
                3
            ],
            "y": [
                4,
                5,
                6
            ]
        }
    ],
    "Memoryview": "hello world",
    "Named tuple": {
        "giga_key": "giga_value"
    },
    "NumPy.array": [
        1,
        2,
        3
    ],
    "NumPy.dtype": "int32",
    "NumPy.int": 10,
    "NumPy.masked_array": {
        "data": [
            1,
            2
        ],
        "mask": [
            false,
            true
        ]
    },
    "NumPy.recarray": [
        {
            "x": 1,
            "y": 1.0
        },
        {
            "x": 2,
            "y": 2.0
        }
    ],
    "Pandas.DataFrame": [
        {
            "a": 1,
            "b": 3
        },
        {
            "a": 2,
            "b": 4
        }
    ],
    "Pandas.Index": [
        1,
        2,
        3
    ],
    "Pandas.Series": {
        "a": 1,
        "b": 2,
        "c": 3
    },
    "PyTorch.Tensor": [
        [
            1,
            2
        ],
        [
            3,
            4
        ]
    ],
    "Range": [
        0,
        1,
        2
    ],
    "Requests.Response": {
        "fact": "The biggest wildcat today is the Siberian Tiger. It can be more than 12 feet (3.6 m) long (about the size of a small car) and weigh up to 700 pounds (317 kg).",
        "headers": {
            "Access-Control-Allow-Origin": "*",
            "Cache-Control": "no-cache, private",
            "Connection": "keep-alive",
            "Content-Encoding": "gzip",
            "Content-Type": "application/json",
            "Date": "Tue, 07 Nov 2023 00:32:51 GMT",
            "Server": "nginx",
            "Set-Cookie": "<redacted>",
            "Transfer-Encoding": "chunked",
            "Vary": "Accept-Encoding",
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "SAMEORIGIN",
            "X-Ratelimit-Limit": "100",
            "X-Ratelimit-Remaining": "99",
            "X-XSS-Protection": "1; mode=block"
        },
        "length": 158,
        "reason": "OK",
        "status_code": 200
    },
    "SciPy.compressed_sparse_row_matrix": [
        [
            1,
            0,
            0
        ],
        [
            0,
            2,
            0
        ],
        [
            0,
            0,
            3
        ]
    ],
    "Set": [
        1,
        2,
        3
    ],
    "Singletons": [
        true,
        false,
        null
    ],
    "String": "hello mars!",
    "TensorFlow.Tensor": [
        [
            1,
            2
        ],
        [
            3,
            4
        ]
    ],
    "Tuple": [
        1,
        2
    ],
    "UUID": "deeefd1a-527d-4196-9b36-ee68f514fb1d"
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
