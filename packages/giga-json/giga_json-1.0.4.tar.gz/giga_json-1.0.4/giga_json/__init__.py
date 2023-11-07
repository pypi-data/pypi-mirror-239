import datetime
import json as og_json
from json import *
from collections.abc import Mapping, Iterable
from typing import Any, Optional, Union
from enum import Enum

"""
will be virtually identical to the standard json module, except it pretty 
prints by default, and the encoder is more resilient, and won't throw 
exceptions by default.

Example usage:

import giga_json as json
json.dumps(some_dict)

see https://github.com/nebko16/giga_json for the full details and examples
"""


class GigaEncoder(og_json.JSONEncoder):

    def __init__(self, *args, raise_on_error: bool = False, debug: bool = False, **kwargs):
        super().__init__(*args, **kwargs)
        self.raise_on_error = raise_on_error
        self.debug = debug

    def default(self, o: Any) -> Optional[Any]:
        object_type_name = type(o).__name__
        object_type = str(type(o))
        if self.debug:
            print(f"actual type: {object_type}")
            print(f"actual type.__name__: {object_type_name}")

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # date and datetime

        if isinstance(o, (datetime.date, datetime.datetime)):
            if self.debug:
                print(f"match: datetime")

            try:
                return o.isoformat()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # requests support

        elif object_type_name == 'Response':
            if self.debug:
                print(f"match: requests Response")

            try:
                jdata = o.json()
                jdata['status_code'] = o.status_code
                jdata['reason'] = o.reason
                jdata['headers'] = o.headers
                return jdata
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # flask support

        elif object_type == "<class 'werkzeug.local.LocalProxy'>":
            if self.debug:
                print(f"match: flask request")

            try:
                url = o.url
                http_method = o.method
                headers = dict(o.headers)
                user_agent = o.headers.get('User-Agent')
                ip_address = o.remote_addr
                content_type = o.headers.get('Content-Type')

                if o.method == 'POST':
                    if content_type == 'application/json':
                        body = o.json
                    elif content_type == 'application/x-www-form-urlencoded':
                        body = o.form
                    elif content_type == 'multipart/form-data':
                        body = o.form
                    else:
                        body = None
                else:
                    body = o.args

                important_data = {
                    'url': url,
                    'http_method': http_method,
                    'headers': headers,
                    'user_agent': user_agent,
                    'ip_address': ip_address,
                    'body': body
                }
                return important_data
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # MatPlotLib support

        elif object_type_name == 'Axes':
            if self.debug:
                print(f"match: MatPlotLib Plot")

            try:
                plot_data = [{'x': line.get_xdata().tolist(), 'y': line.get_ydata().tolist()} for line in o.get_lines()]
                return plot_data
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # SciPy support

        elif object_type_name == 'csr_matrix':
            if self.debug:
                print(f"match: SciPy sparse matrix")

            try:
                return o.toarray().tolist()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # PyTorch support

        elif object_type_name == 'Tensor':

            if self.debug:
                print(f"match: PyTorch tensor")

            try:
                return o.tolist()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # TensorFlow support

        elif object_type_name == 'EagerTensor':
            if self.debug:
                print(f"match: TensorFlow tensor")

            try:
                return o.numpy().tolist()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # Pandas support

        elif object_type_name == 'DataFrame':
            if self.debug:
                print(f"match: Pandas DataFrame")

            try:
                return o.to_dict(orient='records')
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'Series':
            if self.debug:
                print(f"match: Pandas Series")

            try:
                return o.to_dict()
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'Index':
            if self.debug:
                print(f"match: Pandas Index")

            try:
                return o.tolist()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # this block checks to see if an object might have its own built-in serialization.  if it does, we use that, as
        # it's likely going to handle serialization better than relying on dunder checks later in our encoder

        elif hasattr(o, 'to_json'):
            if self.debug:
                print(f"match: to_json()")

            try:
                return o.to_json()
            except (TypeError, ValueError):
                pass

        elif hasattr(o, 'json'):
            if self.debug:
                print(f"match: json()")

            try:
                return o.json()
            except (TypeError, ValueError):
                pass

        elif hasattr(o, 'toJSON'):
            if self.debug:
                print(f"match: toJSON()")

            try:
                return o.toJSON()
            except (TypeError, ValueError):
                pass

        elif hasattr(o, 'as_json'):
            if self.debug:
                print(f"match: as_json()")

            try:
                return o.as_json()
            except (TypeError, ValueError):
                pass

        elif hasattr(o, 'get_json'):
            if self.debug:
                print(f"match: get_json()")

            try:
                return o.get_json()
            except (TypeError, ValueError):
                pass

        elif hasattr(o, 'serialize'):
            if self.debug:
                print(f"match: serialize()")

            try:
                return o.serialize()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # NumPy support

        elif object_type_name == 'recarray':
            if self.debug:
                print(f"match: numpy recarray")

            try:
                from handlers.numpy import handle_recarray
                return handle_recarray(o)
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'MaskedArray':
            if self.debug:
                print(f"match: numpy masked array")

            try:
                return {'data': o.data.tolist(), 'mask': o.mask.tolist()}
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'ndarray':
            if self.debug:
                print(f"match: numpy ndarray")

            try:
                return o.tolist()
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'int32':
            if self.debug:
                print(f"match: numpy number")

            try:
                return o.item()
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'Int64DType':
            if self.debug:
                print(f"match: numpy dtype")

            try:
                return str(o)
            except (TypeError, ValueError):
                pass

        elif object_type_name == 'matrix':
            if self.debug:
                print(f"match: numpy matrix")

            try:
                return o.tolist()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif isinstance(o, (bytearray, set, frozenset, range)):
            if self.debug:
                print(f"match: (bytearray, set, frozenset, range)")

            try:
                return list(o)
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif isinstance(o, memoryview):
            if self.debug:
                print(f"match: memoryview")

            try:
                return o.tobytes().decode('utf-8')
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif object_type_name == 'Decimal':
            if self.debug:
                print(f"match: Decimal")

            try:
                return float(o)
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif object_type_name == 'UUID':
            if self.debug:
                print(f"match: UUID")

            try:
                return str(o)
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # named tuple

        elif hasattr(o, '_asdict'):
            if self.debug:
                print(f"match: _asdict()")

            try:
                return o._asdict()
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # check for K:V types first, since they also meet the criteria for iterables, which would only take the keys

        elif isinstance(o, Mapping):
            if self.debug:
                print(f"match: Mapping")

            try:
                return dict(o)
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif isinstance(o, bytes):
            if self.debug:
                print(f"match: bytes")

            try:
                return o.decode('utf-8')
            except UnicodeDecodeError:
                import base64
                try:
                    return base64.b64encode(o).decode('ascii')
                except (TypeError, ValueError):
                    pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif isinstance(o, Enum):
            if self.debug:
                print(f"match: Enum")

            try:
                return o.value
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

        elif isinstance(o, complex):
            if self.debug:
                print(f"match: complex")

            try:
                r, i = decimal_trunc(o.real), decimal_trunc(o.imag)
                s = f' + {i}i' if i >= 0 else f' - {i*-1}i'
                return f"{r}{s}"
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # objects that don't extend built-in types, and don't have _asdict(),  but have iter and getitem

        elif is_dict_like(o):
            if self.debug:
                print(f"match: dict-like custom object")

            try:
                return dict(o.items() if hasattr(o, 'items') else o)
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # objects you can directly iterate. we do this last because many types actually fit this criteria

        elif (isinstance(o, Iterable) and not isinstance(o, str)) or hasattr(o, '__iter__'):
            if self.debug:
                print(f"match: Iterable or has __iter__")

            try:
                return list(iter(o))
            except (TypeError, ValueError):
                pass

        # %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
        # if all other serialization attempts either didn't match or didn't succeed, we either raise, if raise on error
        # flag is set to True, otherwise we return json null

        else:
            if self.debug:
                print(f"match: else")

            if self.raise_on_error:
                return super().default(o)
            else:
                try:
                    return str(o)
                except (TypeError, ValueError):
                    return None


def is_dict_like(obj: Any) -> bool:
    return hasattr(obj, '__getitem__') and hasattr(obj, '__iter__')


def decimal_trunc(num: Union[int, float]) -> Union[int, float]:
    return int(num) if num == int(num) else num


def og_dumps(obj: Any, *, indent: bool = None, sort_keys: bool = False, **kwargs) -> Optional[str]:
    """ this is literally the vanilla json.dumps(), but with a different name.  it's here purely for convenience """
    return og_json.dumps(obj, indent=indent, sort_keys=sort_keys, **kwargs)


def flat_dumps(obj: Any, *, debug: bool = False, raise_on_error: bool = False, indent: Optional[int] = None, sort_keys: bool = False, **kwargs) -> Optional[str]:
    """ same as dumps(), but no pretty printing (no indents/no sort_keys).  basically leverages GigaEncoder but defaults
    to flat output like vanilla json dumps.  equivalent to dumps(obj, indent=None, sort_keys=False)
    """
    return og_json.dumps(obj, cls=GigaEncoder, debug=debug, raise_on_error=raise_on_error, indent=indent, sort_keys=sort_keys, **kwargs)


def dumps(obj: Any, *, debug: bool = False, raise_on_error: bool = False, indent: Optional[int] = 4, sort_keys: bool = True, **kwargs) -> Optional[str]:
    """ this one is why you're here.  this is the magic sauce """
    return og_json.dumps(obj, cls=GigaEncoder, debug=debug, raise_on_error=raise_on_error, indent=indent, sort_keys=sort_keys, **kwargs)
