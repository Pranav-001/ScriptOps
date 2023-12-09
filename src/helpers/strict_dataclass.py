"""
This file contains custom utilities for dataclass.
"""
from dataclasses import dataclass, fields, is_dataclass
from typing import Any, get_type_hints, Iterable


def strict_dataclass(*args, **kwargs):
    """
    This decorator is used to add :
        - dataclass functionality
        - strict type validation
    """

    def wrapper(cls):
        cls = dataclass(cls, **kwargs)
        original_init = cls.__init__
        # get_type_hints is used to get actual type class of class attributes
        # it returns dict which contains mapping of class attribute name with type
        # Ex: {name:str,phone:typing.Optional[str]}
        fields_types = get_type_hints(cls)

        def validate_nested_fields(*, field_name, field_type, field_value) -> bool:
            """
            Used to validate nested fields
            """
            field_type_origin = field_type.__origin__

            for field_arg_type in field_type.__args__:
                # check if field_type_origin is any Iterable instance
                # Ex: List[Any], Iterable(Any)
                if isinstance(field_type_origin, type) and issubclass(
                    field_type_origin, Iterable
                ):
                    # check instance must be Iterable instance except str
                    success = isinstance(
                        field_value, field_type_origin
                    ) and not isinstance(field_value, str)

                    if not success:
                        continue

                    # validate for each field's value
                    for datum in field_value:
                        success = validate_field_type(
                            field_name=field_name,
                            field_type=field_arg_type,
                            field_value=datum,
                        )
                        if not success:
                            break
                else:
                    success = validate_field_type(
                        field_name=field_name,
                        field_type=field_arg_type,
                        field_value=field_value,
                    )

                if success:
                    return success
            return False

        def validate_field_type(*, field_name, field_type, field_value) -> bool:
            """
            This method is used to validate type conversion
            """
            if field_type is Any:
                return True

            success = None
            if hasattr(field_type, "__origin__"):
                success = validate_nested_fields(
                    field_name=field_name,
                    field_type=field_type,
                    field_value=field_value,
                )
            else:
                if field_type is int:
                    success = isinstance(field_value, field_type) and not isinstance(
                        field_value, bool
                    )
                elif is_dataclass(field_type) and isinstance(field_value, dict):
                    field_type(**field_value)
                    success = True
                else:
                    success = isinstance(field_value, field_type)

            return success

        def __init__(self, *args, **kwargs):
            original_init(self, *args, **kwargs)

            attributes_type_dict = {}

            for field in fields(self):
                field_type = fields_types[field.name]
                field_value = getattr(self, field.name)

                success = validate_field_type(
                    field_name=field.name,
                    field_type=field_type,
                    field_value=field_value,
                )
                if not success:
                    raise TypeError(
                        f"Invalid {field.name}'s data. Expected data must be {field_type}'s instance"
                    )

                # Build attributes type dict
                attributes_type_dict[field.name] = field_type

            # Set attributes types
            setattr(self, "attributes_type_dict", attributes_type_dict)

        cls.__init__ = __init__
        return cls

    return wrapper(args[0]) if args else wrapper
