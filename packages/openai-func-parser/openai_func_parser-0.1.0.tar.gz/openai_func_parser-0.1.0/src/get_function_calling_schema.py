import inspect
from typing import Any, Callable, Dict, _LiteralGenericAlias

from docstring_parser import Docstring, parse


DESCRIPTION_SEPARATOR = "\n\n"


PY_TO_JSON_TYPES = {
    "int": "number",
    "float": "number",
    "str": "string",
    "bool": "boolean",
    "list": "array",
    "dict": "object",
}


class FunctionDescriptionError(ValueError):
    pass


def get_function_calling_schema(
    func: Callable,
    include_long_description: bool = False,
    include_return_in_parameters: bool = False,
) -> Dict[str, Any]:

    if func.__doc__ is not None:
        parsed_docstring = parse(func.__doc__)
    else:
        raise FunctionDescriptionError(
            f"Function {func.__name__} has no docstring."
        )

    name = getattr(func, "__name__")
    description = create_description(
        parsed_docstring,
        include_long_description=include_long_description,
    )
    if not description:
        raise FunctionDescriptionError(
            f"Failed to create a description for function {name},"
            " either due to empty description or missing long description."
        )

    parameters = create_parameters(
        func=func,
        parsed_docstring=parsed_docstring,
        include_return_in_parameters=include_return_in_parameters,
    )

    function_calling_schema = {
        "name": name,
        "description": description,
        "parameters": parameters,
    }
    return function_calling_schema


def create_description(
    parsed_docstring: Docstring,
    include_long_description: bool,
):
    description = parsed_docstring.short_description
    if include_long_description:
        if parsed_docstring.long_description:
            description = DESCRIPTION_SEPARATOR.join(
                [description, parsed_docstring.long_description]
            )
        else:
            return None
    return description


def create_parameters(
    func: Callable,
    parsed_docstring: Docstring,
    include_return_in_parameters: bool,
):
    signature = inspect.signature(func)

    parameter_properties = {}
    required_parameters = []
    # We also approach the parameter by accessing the function's signature,
    #  especially the type annotations.
    for param in parsed_docstring.params:
        param_docstring_type = param.type_name
        param_annotation = func.__annotations__.get(param.arg_name, None)
        param_annotated_type = (
            param_annotation.__name__ if param_annotation else None
        )
        param_signature = signature.parameters[param.arg_name]
        param_type = param_docstring_type or param_annotated_type
        param_type = transform_py_type_to_json_type(param_type)
        parameter_properties[param.arg_name] = {
            "type": param_type,
            "description": param.description,
        }

        # If the parameter has Literal type annotation, infer the enum values.
        if isinstance(param_annotation, _LiteralGenericAlias):
            param_enum = param_annotation.__args__
            parameter_properties[param.arg_name]["enum"] = list(param_enum)

        if (
            (not param.is_optional)
            and (param_signature.default is param_signature.empty)
        ):
            required_parameters.append(param.arg_name)

    if include_return_in_parameters:
        print(f"Collecting return type for function {func.__name__}")
        if not parsed_docstring.returns:
            raise FunctionDescriptionError(
                f"Function {func.__name__} has no return description."
            )
        return_docstring_type = parsed_docstring.returns.type_name
        return_annotation = func.__annotations__.get("return", None)
        return_annotated_type = (
            return_annotation.__name__ if return_annotation else None
        )
        return_type = return_docstring_type or return_annotated_type
        return_type = transform_py_type_to_json_type(return_type)
        parameter_properties["return"] = {
            "type": return_type,
            "description": parsed_docstring.returns.description,
        }
        required_parameters.append("return")

    return {
        "type": "object",
        "properties": parameter_properties,
        "required": required_parameters,
    }


def transform_py_type_to_json_type(py_type: str) -> str:
    if py_type in PY_TO_JSON_TYPES:
        return PY_TO_JSON_TYPES[py_type]
    else:
        return "string"
