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

## What is giga-json?

It's just a light extension of the excellent python json module.

Let's walk through a scenario to make it clear what drove me to create this.

Something is broken, so you decide to quickly troubleshoot it.  Before breaking out the debugger, you decide to just import json and do a dumps on a dictionary.

```python
import json
... broken code here...
print(json.dumps(some_dict))
```
```bash
TypeError: Object of type datetime is not JSON serializable
```

Doh!  That's annoying.  Ok, let's remove the key for the timestamp so we can dump this data.

```python
del some_dict['timestamp']
print(json.dumps(some_dict))
```
```bash
{"$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#", "contentVersion": "1.0.0.0", "parameters": {"eventHubNamespaceName": {"type": "string", "metadata": {"description": "The name of the EventHub namespace"}}, "eventHubName": {"type": "string", "metadata": {"description": "The name of the Event Hub"}}, "sqlServerName": {"type": "string", "metadata": {"description": "Name of the SQL Server"}}, "sqlServerUserName": {"type": "string", "metadata": {"description": "The administrator username of the SQL Server"}}, "sqlServerPassword": {"type": "securestring", "metadata": {"description": "The administrator password of the SQL Server"}}, "sqlServerDatabaseName": {"type": "string", "metadata": {"description": "The name of the SQL Server database"}}, "storageName": {"type": "string", "metadata": {"description": "The name of the storage account"}}, "functionAppName": {"type": "string", "metadata": {"description": "The name of the function app"}}}, "variables": {"blobContainerName": "windturbinecapture", "functionAppPlanName": "[concat(parameters('functionAppName'),'Plan')]", "storageAccountid": "[concat(resourceGroup().id,'/providers/','Microsoft.Storage/storageAccounts/', parameters('storageName'))]"}, "resources": [{"type": "Microsoft.EventHub/namespaces", "apiVersion": "2017-04-01", "name": "[parameters('eventHubNamespaceName')]", "location": "[resourceGroup().location]", "sku": {"name": "Standard"}, "properties": {"isAutoInflateEnabled": "true", "maximumThroughputUnits": "7"}, "dependsOn": ["[resourceId('Microsoft.Storage/storageAccounts', parameters('storageName'))]"], "resources": [{"type": "EventHubs", "apiVersion": "2017-04-01", "name": "[parameters('eventHubName')]", "dependsOn": ["[concat('Microsoft.EventHub/namespaces/', parameters('eventHubNamespaceName'))]"], "properties": {"messageRetentionInDays": "1", "partitionCount": "2", "captureDescription": {"enabled": "true", "encoding": "Avro", "intervalInSeconds": "60", "sizeLimitInBytes": "314572800", "destination": {"name": "EventHubArchive.AzureBlockBlob", "properties": {"storageAccountResourceId": "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageName'))]", "blobContainer": "[variables('blobContainerName')]", "archiveNameFormat": "{Namespace}/{EventHub}/{PartitionId}/{Year}/{Month}/{Day}/{Hour}/{Minute}/{Second}"}}}}}]}, {"type": "Microsoft.Sql/servers", "apiVersion": "2014-04-01", "name": "[parameters('sqlServerName')]", "location": "[resourceGroup().location]", "scale": null, "properties": {"administratorLogin": "[parameters('sqlServerUserName')]", "administratorLoginPassword": "[parameters('sqlServerPassword')]", "version": "12.0"}, "resources": [{"type": "databases", "apiVersion": "2017-10-01-preview", "name": "[parameters('sqlServerDatabaseName')]", "location": "[resourceGroup().location]", "sku": {"name": "DW100c", "tier": "DataWarehouse"}, "properties": {"collation": "SQL_Latin1_General_CP1_CI_AS"}, "dependsOn": ["[resourceId('Microsoft.Sql/servers', parameters('sqlServerName'))]"]}, {"type": "firewallRules", "apiVersion": "2014-04-01", "name": "AllowAllAzureIps", "location": "[resourceGroup().location]", "dependsOn": ["[parameters('sqlServerName')]"], "properties": {"endIpAddress": "0.0.0.0", "startIpAddress": "0.0.0.0"}}]}, {"type": "Microsoft.Storage/storageAccounts", "apiVersion": "2016-01-01", "name": "[parameters('storageName')]", "location": "[resourceGroup().location]", "sku": {"name": "Standard_LRS", "tier": "Standard"}, "kind": "Storage", "tags": {}, "scale": null, "properties": {}, "dependsOn": []}, {"type": "Microsoft.Web/serverfarms", "apiVersion": "2015-08-01", "name": "[variables('functionAppPlanName')]", "location": "[resourceGroup().location]", "kind": "functionapp", "sku": {"name": "Y1", "tier": "Dynamic", "size": "Y1", "family": "Y", "capacity": 0}, "properties": {"name": "[variables('functionAppPlanName')]", "numberOfWorkers": 0}}, {"type": "Microsoft.Web/sites", "apiVersion": "2016-08-01", "name": "[parameters('functionAppName')]", "location": "[resourceGroup().location]", "kind": "functionapp", "dependsOn": ["[resourceId('Microsoft.Web/serverfarms', variables('functionAppPlanName'))]", "[resourceId('Microsoft.Storage/storageAccounts', parameters('storageName'))]"], "properties": {"serverFarmId": "[resourceId('Microsoft.Web/serverfarms', variables('functionAppPlanName'))]", "siteConfig": {"appSettings": [{"name": "AzureWebJobsDashboard", "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageName'), ';AccountKey=', listKeys(variables('storageAccountid'),'2015-05-01-preview').key1)]"}, {"name": "AzureWebJobsStorage", "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageName'), ';AccountKey=', listKeys(variables('storageAccountid'),'2015-05-01-preview').key1)]"}, {"name": "WEBSITE_CONTENTAZUREFILECONNECTIONSTRING", "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageName'), ';AccountKey=', listKeys(variables('storageAccountid'),'2015-05-01-preview').key1)]"}, {"name": "WEBSITE_CONTENTSHARE", "value": "[toLower(parameters('functionAppName'))]"}, {"name": "StorageConnectionString", "value": "[concat('DefaultEndpointsProtocol=https;AccountName=', parameters('storageName'), ';AccountKey=', listKeys(variables('storageAccountid'),'2015-05-01-preview').key1)]"}, {"name": "SqlDwConnection", "value": "[concat('Server=tcp:',parameters('sqlServerName'),'.database.windows.net,1433;Database=', parameters('sqlServerDatabaseName'), ';Trusted_Connection=False;User ID=',parameters('sqlServerUserName'),'@',parameters('sqlServerName'),';Password=',parameters('sqlServerPassword'),';Connection Timeout=30;Encrypt=True')]"}, {"name": "FUNCTIONS_EXTENSION_VERSION", "value": "~1"}, {"name": "WEBSITE_NODE_DEFAULT_VERSION", "value": "6.5.0"}]}}}]}
```

Ahh, too many keys, and no formatting.  Let's pretty print it

```python
print(json.dumps(some_dict, indent=4, sort_keys=True))
```

```bash
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "WWW-dir": "/var/www",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "eventHubName": {
            "metadata": {
              
  ... many many many more keys and values ...              
              
    "variables":
    } {
        "blobContainerName": "windturbinecapture",
        "functionAppPlanName": "[concat(parameters('functionAppName'),'Plan')]",
        "storageAccountid": "[concat(resourceGroup().id,'/providers/','Microsoft.Storage/storageAccounts/', parameters('storageName'))]"
    }
}
```

You're looking for 'WWW-dir' key, but don't see it at the end, but you did sort_keys=True.  What the heck?  (I'll give you a clue: capital letters sort above lower case letters, so W would come before the entire lowercase alphabet)

Pretty annoying, right?  This is a common issue with sorting keys that are in camel-case, since keys like SAMAccoutnName start with caps, while others start with lower case.  Doing this day in and day out gets old.  json module works for its intended purpose, but as soon as you're troubleshooting and just need it to do what you ask of it, it can start to frustrate.

Let's see what this would look like if you did this using giga-json:

```python
import giga_json as json
print(json.dumps(some_dict))
```

```bash
{
    "$schema": "https://schema.management.azure.com/schemas/2015-01-01/deploymentTemplate.json#",
    "contentVersion": "1.0.0.0",
    "parameters": {
        "eventHubName": {
            "metadata": {

   .... many many many more keys and values ....

    "timestamp": "2023-11-07T03:46:07.453381",
    "variables": {
        "blobContainerName": "windturbinecapture",
        "functionAppPlanName": "[concat(parameters('functionAppName'),'Plan')]",
        "storageAccountid": "[concat(resourceGroup().id,'/providers/','Microsoft.Storage/storageAccounts/', parameters('storageName'))]"
    },
    "WWW-dir": "/var/www"
}
```

Boom.  First try, it parsed correctly, and even processed our datetime object into an ISO timestamp.  It defaulted to pretty print, and it defaulted to sort keys, and on top of that, it sorted the keys case insensitively, so the "WWW-dir" key you were looking for is at the end as you would expect.

What if I told you that it can parse much more than just datetime objects?  How about Response objects from requests module?  Or flask request objects?  Or TensorFlow Tensors?  Or MabPlotLib Plots?

And you don't have to take my word for it.  Let's look at a really unrealistic and absurd (but fun) example:

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

Convenient, yeah?

## Philosophy
In my humble opinion:
- The most commonly used settings/parameters/patterns should be the default.
- Suppressing nuisance exceptions can be acceptable default behavior if you're able to override it.
- Adding convenience features can add value, as long as it doesn't come at the cost of stability, functionality, or performance.

Python's json module is great.  It gets the job done and has processed unfathomable amounts of data, every day.  But I find that I'm using it most often to do quick troubleshooting, and when that's the case, I usually want pretty printing, and I want sort keys.  But typing this every time becomes tiresome.  It's also tiring when you just need to quickly dump some output, but you get an exception because your dictionary contains a datetime object.

<hr>

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

## Sorting

`sort_keys` in the standard json module just does a string sort, and since capital letters in English have lower ascii numbers, they sort lower than lower-case letters, so Zebra would show up above antelope in an alphabetically sorted list.

Walls of text suck, so let's do this visually:

```python
import json
animals = {
  'antelope': 0,
  'deer': 0,
  'elk': 0,
  'Wallaby': 0,
  'monkey': 0,
  'lion': 0,
  'chicken': 0,
  'Zebra': 0
}
print(json.dumps(animals, sort_keys=True, indent=4))
```
```bash
{
    "Wallaby": 0,
    "Zebra": 0,
    "antelope": 0,
    "chicken": 0,
    "deer": 0,
    "elk": 0,
    "lion": 0,
    "monkey": 0
}
```
That doesn't look very alphabetized, right?

Now let's try the same thing with giga-json:
```python
import giga-json as json
print(json.dumps(animals))
```
```bash
{
    "antelope": 0,
    "chicken": 0,
    "deer": 0,
    "elk": 0,
    "lion": 0,
    "monkey": 0,
    "Wallaby": 0,
    "Zebra": 0
}
```
That's more like it!  This isn't a part of the standard json module, and while it is on by default, you can choose to disable it by using json.dumps(obj, ci_sort=False), and when you do that, it will let the standard json module do the sorting.

`sort_keys` is on by default, but you can choose to turn it off if you wish with `json.dumps(obj, sort_keys=False)`. However, you can just use the shortcut for this: `flat_dumps()`.  It is `dumps()`, but with defaults for output formatting set to no line breaks and no indents (same as standard json module).


## Behaviors
- if you do the import like this: `import giga_json as json`, it will be virtually identical to the standard json module.  json.load() and json.loads() are literally the vanilla functions
- the serializer has an intelligent order of checks.  for example, it checks for mapping before it tries iteration.  and before mapping, it checks the object for any built-in serialization methods, like to_json(), json(), etc.  this ensures that not only will your object be successfully serialized, but it will try the best method first
- if a serialization match and attempt fails, the serializer is allowed to continue down the list in case another method might match and work for the given object, increasing the chance of successful serialization
- .og_dumps() is an alias to the standard json.dumps() method, completely unchanged, if you need it
- .flat_dumps() uses giga_json's custom serializer, but its output argument defaults match standard json module, which means no pretty printing (no line breaks and no indents).  this is for convenience.  dumps() you'd probably use for troubleshooting, as it pretty prints, and you'd use this one for other purposes (like when you'd use jsonify)
- this literally just inherits from standard json module, so all the original features are there.  you can still change indent and sort_keys and even pass in your own encode using default=
- if you provide some really complex object, like with tuples as keys, which json module can't parse anyway, the sorting function can possibly break
  - it tries to sort the object BEFORE sending it into the encoder
  - if that fails, it then tries to let the standard module parse and serialize it
  - if that succeeds, it then loads() the output, tries case-insensitive sort again, but this time against the object after it's been completely serialized by the encoder, then dumps() the object again  
  - if that fails, it returns the traditionally sorted object by default as a fallback, unless raise_on_error is set to true, in which case it'll throw an exception

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
