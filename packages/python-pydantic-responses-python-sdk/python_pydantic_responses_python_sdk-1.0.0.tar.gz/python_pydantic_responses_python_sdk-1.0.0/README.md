# python-pydantic-responses-python-sdk<a id="python-pydantic-responses-python-sdk"></a>

A simple API based on python pydantic responses.


[![PyPI](https://img.shields.io/badge/PyPI-v1.0.0-blue)](https://pypi.org/project/python-pydantic-responses-python-sdk/1.0.0)
[![README.md](https://img.shields.io/badge/README-Click%20Here-green)](https://github.com/konfig-dev/konfig/tree/main/python#readme)
[![More Info](https://img.shields.io/badge/More%20Info-Click%20Here-orange)](http://example.com/support)

## Table of Contents<a id="table-of-contents"></a>

<!-- toc -->

- [Requirements](#requirements)
- [Installing](#installing)
- [Getting Started](#getting-started)
- [Async](#async)
- [Raw HTTP Response](#raw-http-response)
- [Reference](#reference)
  * [`pythonpydanticresponses.test.fetch`](#pythonpydanticresponsestestfetch)
  * [`pythonpydanticresponses.test.reserved_word`](#pythonpydanticresponsestestreserved_word)

<!-- tocstop -->

## Requirements<a id="requirements"></a>

Python >=3.7

## Installing<a id="installing"></a>

```sh
pip install python-pydantic-responses-python-sdk==1.0.0
```

## Getting Started<a id="getting-started"></a>

```python
from pprint import pprint
from python_pydantic import PythonPydanticResponses, ApiException

pythonpydanticresponses = PythonPydanticResponses(
    api_key="YOUR_API_KEY",
)

try:
    # Fetches a JSON value based on input parameter
    fetch_response = pythonpydanticresponses.test.fetch(
        input_parameter="inputParameter_example",
    )
    print(fetch_response)
except ApiException as e:
    print("Exception when calling TestApi.fetch: %s\n" % e)
    pprint(e.body)
    if e.status == 400:
        pprint(e.body["error"])
    if e.status == 500:
        pprint(e.body["error"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```

## Async<a id="async"></a>

`async` support is available by prepending `a` to any method.

```python
import asyncio
from pprint import pprint
from python_pydantic import PythonPydanticResponses, ApiException

pythonpydanticresponses = PythonPydanticResponses(
    api_key="YOUR_API_KEY",
)


async def main():
    try:
        # Fetches a JSON value based on input parameter
        fetch_response = await pythonpydanticresponses.test.afetch(
            input_parameter="inputParameter_example",
        )
        print(fetch_response)
    except ApiException as e:
        print("Exception when calling TestApi.fetch: %s\n" % e)
        pprint(e.body)
        if e.status == 400:
            pprint(e.body["error"])
        if e.status == 500:
            pprint(e.body["error"])
        pprint(e.headers)
        pprint(e.status)
        pprint(e.reason)
        pprint(e.round_trip_time)


asyncio.run(main())
```

## Raw HTTP Response<a id="raw-http-response"></a>

To access raw HTTP response values, use the `.raw` namespace.

```python
from pprint import pprint
from python_pydantic import PythonPydanticResponses, ApiException

pythonpydanticresponses = PythonPydanticResponses(
    api_key="YOUR_API_KEY",
)

try:
    # Fetches a JSON value based on input parameter
    fetch_response = pythonpydanticresponses.test.raw.fetch(
        input_parameter="inputParameter_example",
    )
    pprint(fetch_response.body)
    pprint(fetch_response.body["property_a"])
    pprint(fetch_response.body["property_b"])
    pprint(fetch_response.body["property_c"])
    pprint(fetch_response.headers)
    pprint(fetch_response.status)
    pprint(fetch_response.round_trip_time)
except ApiException as e:
    print("Exception when calling TestApi.fetch: %s\n" % e)
    pprint(e.body)
    if e.status == 400:
        pprint(e.body["error"])
    if e.status == 500:
        pprint(e.body["error"])
    pprint(e.headers)
    pprint(e.status)
    pprint(e.reason)
    pprint(e.round_trip_time)
```


## Reference<a id="reference"></a>
### `pythonpydanticresponses.test.fetch`<a id="pythonpydanticresponsestestfetch"></a>

Provide an input parameter to receive a JSON value with properties.

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
fetch_response = pythonpydanticresponses.test.fetch(
    input_parameter="inputParameter_example",
)
```

#### ⚙️ Parameters<a id="⚙️-parameters"></a>

##### input_parameter: `str`<a id="input_parameter-str"></a>

The input parameter to process.

#### 🔄 Return<a id="🔄-return"></a>

[TestFetchResponse](./python_pydantic/pydantic/test_fetch_response.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/simple-endpoint` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---

### `pythonpydanticresponses.test.reserved_word`<a id="pythonpydanticresponsestestreserved_word"></a>

Reserved word in Python

#### 🛠️ Usage<a id="🛠️-usage"></a>

```python
reserved_word_response = pythonpydanticresponses.test.reserved_word()
```

#### 🔄 Return<a id="🔄-return"></a>

[TestReservedWord](./python_pydantic/pydantic/test_reserved_word.py)

#### 🌐 Endpoint<a id="🌐-endpoint"></a>

`/reserved-word` `get`

[🔙 **Back to Table of Contents**](#table-of-contents)

---


## Author<a id="author"></a>
This Python package is automatically generated by [Konfig](https://konfigthis.com)
