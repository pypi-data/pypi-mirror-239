# OpenAI Function Parser

Transform Python function docstrings into JSON schemas compliant with OpenAI function calling protocols.


## Installation

```bash
pip install openai-function-parser
```

## Usage

```python

from openai_function_parser import get_function_calling_schema


def my_function(a: int, b: str, c: float = 1.0) -> int:
    """
    My function description.

    Args:
        a: My first argument.
        b: My second argument.
        c: My third argument.

    Returns:
        My return value.
    """
    return 1

function_call_schema = get_function_calling_schema(my_function)
print(function_call_schema)
```


## Authors

Xiaotian Duan (xduan7 at gmail dot com)
