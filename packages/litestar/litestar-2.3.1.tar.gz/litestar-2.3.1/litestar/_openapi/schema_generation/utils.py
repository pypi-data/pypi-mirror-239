from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from litestar.typing import FieldDefinition

__all__ = (
    "_type_or_first_not_none_inner_type",
    "_should_create_enum_schema",
    "_should_create_literal_schema",
)


def _type_or_first_not_none_inner_type(field_definition: FieldDefinition) -> Any:
    """Get the first inner type that is not None.

    This is a narrow focussed utility to be used when we know that a field definition either represents
    a single type, or a single type in a union with `None`, and we want the single type.

    Args:
        field_definition: A field definition instance.

    Returns:
        A field definition instance.
    """
    if not field_definition.is_optional:
        return field_definition.annotation
    inner = next((t for t in field_definition.inner_types if not t.is_none_type), None)
    if inner is None:
        raise ValueError("Field definition has no inner type that is not None")
    return inner.annotation


def _should_create_enum_schema(field_definition: FieldDefinition) -> bool:
    """Predicate to determine if we should create an enum schema for the field def, or not.

    This returns true if the field definition is an enum, or if the field definition is a union
    of an enum and ``None``.

    When an annotation is ``SomeEnum | None`` we should create a schema for the enum that includes ``null``
    in the enum values.

    Args:
        field_definition: A field definition instance.

    Returns:
        A boolean
    """
    return field_definition.is_subclass_of(Enum) or (
        field_definition.is_optional
        and len(field_definition.args) == 2
        and field_definition.has_inner_subclass_of(Enum)
    )


def _should_create_literal_schema(field_definition: FieldDefinition) -> bool:
    """Predicate to determine if we should create a literal schema for the field def, or not.

    This returns ``True`` if the field definition is an literal, or if the field definition is a union
    of a literal and None.

    When an annotation is `Literal["anything"] | None` we should create a schema for the literal that includes `null`
    in the enum values.

    Args:
        field_definition: A field definition instance.

    Returns:
        A boolean
    """
    return (
        field_definition.is_literal
        or field_definition.is_optional
        and all(inner.is_literal for inner in field_definition.inner_types if not inner.is_none_type)
    )
