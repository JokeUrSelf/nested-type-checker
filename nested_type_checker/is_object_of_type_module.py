import inspect
import types
import typing
from typing import get_args, get_origin

def get_type_root(type_):
    return type_ if get_origin(type_) is None else get_origin(type_)


def is_object_of_type(obj, type_) -> bool:
    origin_type = get_type_root(type_)
    type_children = get_args(type_)

    if origin_type is None:
        return obj is None

    if origin_type is typing.Union or origin_type is types.UnionType:
        return any([is_object_of_type(obj, t) for t in type_children])
    if origin_type is typing.Optional:
        return any(
            [is_object_of_type(obj, t) for t in (*type_children, None)]
        )
    if origin_type is typing.Any:
        return True

    if not isinstance(obj, origin_type):
        return False
    if not type_children:
        return True

    if issubclass(origin_type, typing.Iterable):
        if issubclass(origin_type, typing.Tuple):
            if len(type_children) == 2 and isinstance(
                type_children[1], types.EllipsisType
            ):
                for child in obj:
                    if not is_object_of_type(child, type_children[0]):
                        return False
            elif len(type_children) == len(obj):
                for child, child_type in zip(obj, type_children):
                    if not is_object_of_type(child, child_type):
                        return False
            else:
                return False
            return True
        if any(
            issubclass(origin_type, t)
            for t in {typing.Sequence, typing.Set, typing.FrozenSet}
        ):
            for child in obj:
                if not is_object_of_type(child, type_children[0]):
                    return False
            return True

        if issubclass(origin_type, typing.Mapping):
            obj_item_columns = obj.keys(), obj.values() if obj.keys() else ()
            if len(obj_item_columns) != len(type_children):
                return False

            for obj_item_column, type_child in zip(obj_item_columns, type_children):
                for obj_item in obj_item_column:
                    if not is_object_of_type(obj_item, type_child):
                        return False
            return True

    if issubclass(origin_type, typing.Callable):
        signature = inspect.signature(obj)
        return_type = signature.return_annotation
        param_types = tuple(param.annotation for param in signature.parameters.values())

        specified_return_type = (
            None if type_children[1] is types.NoneType else type_children[1]
        )
        if (
            specified_return_type is not typing.Any
            and return_type is not specified_return_type
        ):
            return False
        if len(param_types) != len(type_children[0]):
            return False
        for i, specified_param_type in enumerate(type_children[0]):
            if specified_param_type is typing.Any:
                continue
            specified_param_type = (
                None if specified_param_type is types.NoneType else specified_param_type
            )
            if param_types[i] is not specified_param_type:
                return False
        return True

    raise RuntimeError("Undefined behaviour")
