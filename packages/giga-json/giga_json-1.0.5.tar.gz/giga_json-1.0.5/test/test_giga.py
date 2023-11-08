import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import datetime
import giga_json as json
import unittest
import uuid
try:
    import flask
except ImportError:
    flask = None
try:
    import matplotlib.pyplot as plt
except ImportError:
    plt = None
try:
    import numpy as np
except ImportError:
    np = None
try:
    import pandas as pd
except ImportError:
    pd = None
try:
    import requests
except ImportError:
    requests = None
try:
    from scipy.sparse import csr_matrix
except ImportError:
    csr_matrix = None
try:
    import tensorflow as tf
except ImportError:
    tf = None
try:
    import torch
except ImportError:
    torch = None
from decimal import Decimal
from enum import Enum


if flask:
    app = flask.Flask(__name__)

    @app.route('/test', methods=['GET', 'POST'])
    def test_route():
        return json.flat_dumps(flask.request)



class MyEnum(Enum):
    A = 1
    B = 2


class CustomObject:
    def _asdict(self):
        return {'giga_key': 'giga_value'}


class Mappy:
    def __init__(self): self.data = {'pie': 'thawn'}
    def __iter__(self): return iter(self.data)
    def __getitem__(self, key): return self.data[key]
    def items(self): return self.data.items()


class CustomJSONEncoderTestCase(unittest.TestCase):

    maxDiff = None

    @unittest.skipIf(flask is None, "flask is not installed.")
    def setUp(self):
        self.app = app.test_client()

    @unittest.skipIf(flask is None, "flask is not installed.")
    def test_flask_request_get(self):
        response = self.app.get('/test', headers={'User-Agent': 'UnitTest'}, query_string={'param': 'value'})
        actual = json.loads(response.data)
        expected = {'url': 'http://localhost/test?param=value', 'http_method': 'GET', 'headers': {'User-Agent': 'UnitTest', 'Host': 'localhost'}, 'user_agent': 'UnitTest', 'ip_address': '127.0.0.1', 'body': {'param': 'value'}}
        self.assertEqual(actual, expected)

    @unittest.skipIf(flask is None, "flask is not installed.")
    def test_flask_request_post(self):
        response = self.app.post('/test', headers={'User-Agent': 'UnitTest', 'Content-Type': 'application/json'}, json={'key': 'value'})
        actual = json.loads(response.data)
        expected = {'url': 'http://localhost/test', 'http_method': 'POST', 'headers': {'User-Agent': 'UnitTest', 'Host': 'localhost', 'Content-Type': 'application/json', 'Content-Length': '16'}, 'user_agent': 'UnitTest', 'ip_address': '127.0.0.1', 'body': {'key': 'value'}}
        self.assertEqual(actual, expected)

    def test_date(self):

        date = datetime.date(2023, 4, 1)
        self.assertEqual(json.dumps(date), '"2023-04-01"')

    def test_datetime(self):

        dt = datetime.datetime(2023, 4, 1, 12, 0)
        self.assertEqual(json.dumps(dt), '"2023-04-01T12:00:00"')

    def test_decimal(self):

        dec = Decimal('12.34')
        self.assertEqual(json.dumps(dec), '12.34')

    def test_uuid(self):

        u = uuid.uuid4()
        self.assertEqual(json.dumps(u), '"' + str(u) + '"')

    def test_mapping(self):

        m = {'a': 1, 'b': 2}
        self.assertEqual(json.dumps(m), '{\n    "a": 1,\n    "b": 2\n}')

    def test_iterable(self):

        l = [1, 2, 3]
        self.assertEqual(json.dumps(l), '[\n    1,\n    2,\n    3\n]')

    def test_bytes(self):

        b = b'hello'
        self.assertEqual(json.dumps(b), '"hello"')

    def test_set(self):

        s = {1, 2, 3}
        self.assertEqual(json.dumps(s), '[\n    1,\n    2,\n    3\n]')

    def test_complex(self):

        c = 1 + 2j
        self.assertEqual(json.dumps(c), '"1 + 2i"')

        c = 0 + 1j
        self.assertEqual(json.dumps(c), '"0 + 1i"')

        c = 4.1 - 0j
        self.assertEqual(json.dumps(c), '"4.1 + 0i"')

        c = 3.14 - 2.4j
        self.assertEqual(json.dumps(c), '"3.14 - 2.4i"')

        c = 0 + 0j
        self.assertEqual(json.dumps(c), '"0 + 0i"')

        c = 2j
        self.assertEqual(json.dumps(c), '"0 + 2i"')

    def test_asdict(self):

        obj = CustomObject()
        self.assertEqual(json.dumps(obj), '{\n    "giga_key": "giga_value"\n}')

    def test_custom(self):

        mappy = Mappy()
        self.assertEqual(json.dumps(mappy), '{\n    "pie": "thawn"\n}')

    @unittest.skipIf(np is None, "NumPy is not installed.")
    def test_numpy(self):

        numpy_array = np.array([1, 2, 3])
        self.assertEqual(json.flat_dumps(numpy_array), '[1, 2, 3]')

        numpy_int = np.int32(10)
        self.assertEqual(json.flat_dumps(numpy_int), '10')

        numpy_dtype = numpy_array.dtype
        self.assertEqual(json.flat_dumps(numpy_dtype), '"int64"')

        # deprecated; use ndarray
        # numpy_matrix = np.matrix([[1, 2], [3, 4]])
        # self.assertEqual(json.flat_dumps(numpy_matrix), '[[1, 2], [3, 4]]')

        numpy_masked_array = np.ma.masked_array([1, 2], mask=[False, True])
        self.assertEqual(json.flat_dumps(numpy_masked_array), '{"data": [1, 2], "mask": [false, true]}')

        numpy_recarray = np.recarray((2,), dtype=[('x', int), ('y', float)])
        numpy_recarray[:] = [(1, 1.0), (2, 2.0)]
        self.assertEqual(json.flat_dumps(numpy_recarray), '[{"x": 1, "y": 1.0}, {"x": 2, "y": 2.0}]')

    @unittest.skipIf(pd is None, "Pandas is not installed.")
    def test_pandas(self):

        df = pd.DataFrame({'a': [1, 2], 'b': [3, 4]})
        self.assertEqual(json.flat_dumps(df), '[{"a": 1, "b": 3}, {"a": 2, "b": 4}]')

        series = pd.Series([1, 2, 3], index=['a', 'b', 'c'])
        self.assertEqual(json.flat_dumps(series), '{"a": 1, "b": 2, "c": 3}')

        index = pd.Index([1, 2, 3])
        self.assertEqual(json.flat_dumps(index), '[1, 2, 3]')

    @unittest.skipIf(torch is None, "PyTorch is not installed.")
    def test_pytorch(self):
        tensor = torch.tensor([[1, 2], [3, 4]])
        self.assertEqual(json.flat_dumps(tensor), '[[1, 2], [3, 4]]')

    @unittest.skipIf(tf is None, "TensorFlow is not installed.")
    def test_tensorflow(self):
        tensor = tf.constant([[1, 2], [3, 4]])
        self.assertEqual(json.flat_dumps(tensor), '[[1, 2], [3, 4]]')

    @unittest.skipIf(plt is None, "MatPlotLib is not installed.")
    def test_matplotlib(self):
        fig, ax = plt.subplots()
        ax.plot([1, 2, 3], [4, 5, 6])
        self.assertEqual(json.flat_dumps(ax), '[{"x": [1, 2, 3], "y": [4, 5, 6]}]')

    @unittest.skipIf(csr_matrix is None, "SciPy is not installed.")
    def test_scipy(self):
        sparse_matrix = csr_matrix([[1, 0, 0], [0, 2, 0], [0, 0, 3]])
        self.assertEqual(json.flat_dumps(sparse_matrix), '[[1, 0, 0], [0, 2, 0], [0, 0, 3]]')

    @unittest.skipIf(requests is None, "requests is not installed.")
    def test_requests(self):
        response = requests.models.Response()
        response._content = b'{"key": "value"}'
        response.status_code = 200
        response.reason = 'OK'
        response.headers = requests.structures.CaseInsensitiveDict({'Content-Type': 'application/json'})
        self.assertEqual(json.flat_dumps(response), '{"key": "value", "status_code": 200, "reason": "OK", "headers": {"Content-Type": "application/json"}}')

    def test_frozenset_serialization(self):
        actual = json.flat_dumps(frozenset([1, 2, 3]))
        actual = list(json.loads(actual))
        actual.sort()
        # they're unordered so we're converting to list and sorting before assertion
        self.assertEqual(str(actual), '[1, 2, 3]')

    def test_enum(self):
        self.assertEqual(json.dumps(MyEnum.A), '1')

    def test_memory_view_serialization(self):
        mem_view = memoryview(bytearray(b'hello world'))
        serialized_data = json.dumps(mem_view)
        self.assertEqual(serialized_data, '"hello world"')

    def test_fallback_to_str(self):
        obj = object()
        self.assertTrue(isinstance(json.dumps(obj), str))


if __name__ == '__main__':
    unittest.main(verbosity=2)
