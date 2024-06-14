## Nested Type Checker (Beta)

A runtime strict type-checking module for Python designed to validate parametrized (nested) types.
It supports both Python built-in types and custom types.

## Example Usage

To check if an object matches a specified parametrized type, use the function
`is_object_of_type(obj, parametrized_type)`:

```python
from lib.nested_type_checker import is_object_of_type

obj = [123, ({"", True},)]

CorrectType = list[int | tuple[dict[str, bool]]]
WrongType = list[bool | tuple[dict[str, bool]]]

a = is_object_of_type(obj, CorrectType)
b = is_object_of_type(obj, WrongType)

print(a)  # outputs True
print(b)  # outputs False
```

## Support

The module supports can validate mappings, tuples, lists, sets, frozensets, callables, unions, optionals, and any other parametrized or unparametrized types, including custom (unparametrized) types.

## Installation

To install, use Python's `pip` package manager:

```sh
pip install nested_type_checker
```
