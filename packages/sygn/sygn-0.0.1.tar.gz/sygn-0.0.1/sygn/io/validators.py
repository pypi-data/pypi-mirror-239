from typing import Any

import astropy.units
from astropy import units as u


def validate_quantity_units(value: Any, field_name: str,
                            unit_equivalency: astropy.units.Unit) -> astropy.units.Quantity:
    """Return the value as an astropy Quantity if it contains the correct units.

    :param value: THe value to be validated
    :param field_name: The field name of the value
    :param unit_equivalency: The equivalent unit the value should have
    :return: THe value as an astropy Quantity
    """
    if isinstance(value, astropy.units.Quantity) and value.unit.is_equivalent(unit_equivalency):
        return value
    try:
        if isinstance(value, str):
            if u.Quantity(value).unit.is_equivalent(unit_equivalency):
                return u.Quantity(value)
    except TypeError:
        raise TypeError(f'{value} is not a valid input for {field_name}')
    raise ValueError(f'{value} is not a valid input for {field_name}')
