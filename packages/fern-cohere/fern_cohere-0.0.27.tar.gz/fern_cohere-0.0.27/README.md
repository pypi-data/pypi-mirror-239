# Cohere Python Library

[![pypi](https://img.shields.io/pypi/v/fern-cohere.svg)](https://pypi.python.org/pypi/fern-cohere)
[![fern shield](https://img.shields.io/badge/%F0%9F%8C%BF-SDK%20generated%20by%20Fern-brightgreen)](https://github.com/fern-api/fern)

## Installation

Add this dependency to your project's build file:

```bash
pip install fern-cohere
# or
poetry add fern-cohere
```

## Requirements

- Python 3.7+

## Usage

```python
from cohere.client import Cohere

co = Cohere(api_key="YOUR_API_KEY")

prediction = co.generate(
  model='large',
  prompt='co:here',
  max_tokens=10
)

print('prediction: {}'.format(prediction.generations[0].text))
```

## Async Client

```python
from cohere.client import AsyncCohere

import asyncio

co = AsyncCohere(api_key="YOUR_API_KEY")

async def generate() -> None:
    prediction = co.generate(
      model='large',
      prompt='co:here',
      max_tokens=10
    )
    print(prediction)

asyncio.run(generate())
```

## Streaming 

```python
from cohere.client import Cohere

co = Cohere(api_key="YOUR_API_KEY")

stream = co.chat_stream(
  model="command",
  message="Tell me a story in 5 parts!"
)
for chat in stream: 
  if chat.event_type == "text-generation": 
    print(chat.text)
```


## Endpoints

For a full breakdown of endpoints and arguments, please consult the 
[SDK Docs](https://cohere-sdk.readthedocs.io/en/latest/) and [Cohere API Docs](https://docs.cohere.ai/).

| Cohere Endpoint  | Function             |
| ---------------- | -------------------- |
| /generate        | co.generate()        |
| /embed           | co.embed()           |
| /classify        | co.classify()        |
| /tokenize        | co.tokenize()        |
| /detokenize      | co.detokenize()      |
| /detect-language | co.detect_language() |

## Timeouts
By default, the client is configured to have a timeout of 60 seconds. You can customize this value at client instantiation. 

```python
from cohere.client import Cohere

co = Cohere(api_key="YOUR_API_KEY", timeout=15)
```

## Handling Exceptions
All exceptions thrown by the SDK will sublcass [cohere.ApiError](./src/cohere/core/api_error.py). 

```python
from cohere.core import ApiError
from cohere import BadRequestError

try:
  co..generate(model='large', prompt='co:here', max_tokens=10)
except BadRequestError as e: 
  # handle bad request error
except APIError as e:  
  # handle any api related error
```

Error codes are as followed:

| Status Code | Error Type                 |
| ----------- | -------------------------- |
| 400         | `BadRequestError`          |
| 500         | `InternalServerError`      |

## Beta status

This SDK is in beta, and there may be breaking changes between versions without a major version update. Therefore, we recommend pinning the package version to a specific version in your pyproject.toml file. This way, you can install the same version each time without breaking changes unless you are intentionally looking for the latest version.

## Contributing

While we value open-source contributions to this SDK, this library is generated programmatically. Additions made directly to this library would have to be moved over to our generation code, otherwise they would be overwritten upon the next generated release. Feel free to open a PR as a proof of concept, but know that we will not be able to merge it as-is. We suggest opening an issue first to discuss with us!

On the other hand, contributions to the README are always very welcome!
