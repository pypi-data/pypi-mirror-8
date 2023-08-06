import re
import decimal
import operator
import functools
import collections

from django.core.exceptions import ValidationError
from django.core.validators import (
    MinLengthValidator,
    MaxLengthValidator,
)

from flex.context_managers import ErrorCollection
from flex.formats import registry
from flex.utils import (
    is_value_of_any_type,
    is_non_string_iterable,
    get_type_for_value,
)
from flex.constants import (
    EMPTY,
    NUMBER,
    STRING,
    ARRAY,
)
from flex.decorators import (
    skip_if_not_of_type,
    suffix_reserved_words,
)
from flex.error_messages import MESSAGES


def skip_if_empty(func):
    """
    Decorator for validation functions which makes them pass if the value
    passed in is the EMPTY sentinal value.
    """
    @functools.wraps(func)
    def inner(value, *args, **kwargs):
        if value is EMPTY:
            return
        else:
            return func(value, *args, **kwargs)
    return inner


@skip_if_empty
def validate_type(value, types):
    """
    Validate that the value is one of the provided primative types.
    """
    if not is_value_of_any_type(value, types):
        raise ValidationError(MESSAGES['type']['invalid'].format(
            repr(value), get_type_for_value(value), types,
        ))


@suffix_reserved_words
def generate_type_validator(type_, **kwargs):
    """
    Generates a callable validator for the given type or iterable of types.
    """
    if is_non_string_iterable(type_):
        types = type_
    else:
        types = (type_,)
    return functools.partial(validate_type, types=types)


@suffix_reserved_words
def generate_format_validator(format_, **kwargs):
    """
    Returns the validator function for the given format, as registered with the
    format registry.
    """
    if format_ in registry:
        return registry[format_]
    else:
        return noop


def noop(*args, **kwargs):
    """
    No-Op validator that does nothing.
    """
    pass


def validate_required(value):
    if value is EMPTY:
        raise ValidationError(MESSAGES['required']['required'])


def generate_required_validator(required, **kwargs):
    if required:
        return validate_required
    else:
        return noop


@skip_if_empty
@skip_if_not_of_type(NUMBER)
def validate_multiple_of(value, divisor):
    """
    Given a value and a divisor, validate that the value is divisible by the
    divisor.
    """
    if not decimal.Decimal(str(value)) % decimal.Decimal(str(divisor)) == 0:
        raise ValidationError(
            MESSAGES['multiple_of']['invalid'].format(divisor, value),
        )


def generate_multiple_of_validator(multipleOf, **kwargs):
    return functools.partial(validate_multiple_of, divisor=multipleOf)


@skip_if_empty
@skip_if_not_of_type(NUMBER)
def validate_minimum(value, minimum, is_exclusive):
    """
    Validator function for validating that a value does not violate it's
    minimum allowed value.  This validation can be inclusive, or exclusive of
    the minimum depending on the value of `is_exclusive`.
    """
    if is_exclusive:
        comparison_text = "greater than"
        compare_fn = operator.gt
    else:
        comparison_text = "greater than or equal to"
        compare_fn = operator.ge

    if not compare_fn(value, minimum):
        raise ValidationError(
            MESSAGES['minimum']['invalid'].format(value, comparison_text, minimum),
        )


def generate_minimum_validator(minimum, exclusiveMinimum=False, **kwargs):
    """
    Generator function returning a callable for minimum value validation.
    """
    return functools.partial(validate_minimum, minimum=minimum, is_exclusive=exclusiveMinimum)


@skip_if_empty
@skip_if_not_of_type(NUMBER)
def validate_maximum(value, maximum, is_exclusive):
    """
    Validator function for validating that a value does not violate it's
    maximum allowed value.  This validation can be inclusive, or exclusive of
    the maximum depending on the value of `is_exclusive`.
    """
    if is_exclusive:
        comparison_text = "less than"
        compare_fn = operator.lt
    else:
        comparison_text = "less than or equal to"
        compare_fn = operator.le

    if not compare_fn(value, maximum):
        raise ValidationError(
            MESSAGES['maximum']['invalid'].format(value, comparison_text, maximum),
        )


def generate_maximum_validator(maximum, exclusiveMaximum=False, **kwargs):
    """
    Generator function returning a callable for maximum value validation.
    """
    return functools.partial(validate_maximum, maximum=maximum, is_exclusive=exclusiveMaximum)


def generate_min_length_validator(minLength, **kwargs):
    """
    Generates a validator for enforcing the minLength of a string.
    """
    return skip_if_empty(skip_if_not_of_type(STRING)(MinLengthValidator(minLength).__call__))


def generate_max_length_validator(maxLength, **kwargs):
    """
    Generates a validator for enforcing the maxLength of a string.
    """
    return skip_if_empty(skip_if_not_of_type(STRING)(MaxLengthValidator(maxLength).__call__))


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def validate_min_items(value, minimum):
    """
    Validator for ARRAY types to enforce a minimum number of items allowed for
    the ARRAY to be valid.
    """
    if len(value) < minimum:
        raise ValidationError(
            MESSAGES['min_items']['invalid'].format(
                minimum, len(value),
            ),
        )


def generate_min_items_validator(minItems, **kwargs):
    """
    Generator function returning a callable for minItems validation.
    """
    return functools.partial(validate_min_items, minimum=minItems)


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def validate_max_items(value, maximum):
    """
    Validator for ARRAY types to enforce a maximum number of items allowed for
    the ARRAY to be valid.
    """
    if len(value) > maximum:
        raise ValidationError(
            MESSAGES['max_items']['invalid'].format(
                maximum, len(value),
            ),
        )


def generate_max_items_validator(maxItems, **kwargs):
    """
    Generator function returning a callable for maxItems validation.
    """
    return functools.partial(validate_max_items, maximum=maxItems)


@skip_if_empty
@skip_if_not_of_type(ARRAY)
def validate_unique_items(value):
    """
    Validator for ARRAY types to enforce that all array items must be unique.
    """
    # we can't just look at the items themselves since 0 and False are treated
    # the same as dictionary keys.
    counter = collections.Counter((
        (v, type(v)) for v in value
    ))
    dupes = [v[0] for v, count in counter.items() if count > 1]
    if dupes:
        raise ValidationError(
            MESSAGES['unique_items']['invalid'].format(
                repr(dupes),
            ),
        )


def generate_unique_items_validator(uniqueItems, **kwargs):
    """
    Returns the unique_item_validator if uniqueItems is set to True, otherwise
    it returns the noop function.
    """
    if uniqueItems:
        return validate_unique_items
    else:
        return noop


@skip_if_empty
@skip_if_not_of_type(STRING)
def validate_pattern(value, regex):
    if not regex.match(value):
        raise ValidationError(
            MESSAGES['pattern']['invalid'].format(value, regex.pattern),
        )


def generate_pattern_validator(pattern, **kwargs):
    return functools.partial(validate_pattern, regex=re.compile(pattern))


def deep_equal(a, b):
    """
    Because of things in python like:
        >>> 1 == 1.0
        True
        >>> 1 == True
        True
    """
    return a == b and isinstance(a, type(b)) and isinstance(b, type(a))


@skip_if_empty
def validate_enum(value, options):
    if not any(deep_equal(value, option) for option in options):
        raise ValidationError(
            MESSAGES['enum']['invalid'].format(
                value, options,
            )
        )


def generate_enum_validator(enum, **kwargs):
    return functools.partial(validate_enum, options=enum)


def validate_object(obj, validators, inner=False):
    """
    Takes a mapping and applies a mapping of validator functions to it
    collecting and reraising any validation errors that occur.
    """
    with ErrorCollection(inner=inner) as errors:
        if '$ref' in validators:
            ref_ = validators.pop('$ref')
            for k, v in ref_.validators.items():
                validators.setdefault(k, v)
        for key, validator in validators.items():
            try:
                validator(obj)
            except ValidationError as err:
                errors[key].extend(list(err.messages))
