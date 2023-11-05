from typing import Any

import astropy.units
from astropy import units as u
from pydantic import BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from sygn.core.simulation.sources.star import Star
from sygn.io.validators import validate_quantity_units


class Observation(BaseModel):
    """Class representation of an observation."""
    adjust_baseline_to_habitable_zone: bool
    integration_time: Any
    optimized_wavelength: Any
    observatory: Any = None
    sources: dict = {}

    @field_validator('integration_time')
    def validate_integration_time(cls, value: Any, info: ValidationInfo) -> astropy.units.Quantity:
        """Validate the integration time input.

        :param value: Value given as input
        :param info: ValidationInfo object
        :return: The integration time in units of time
        """
        return validate_quantity_units(value=value, field_name=info.field_name, unit_equivalency=u.s)

    @field_validator('optimized_wavelength')
    def validate_optimized_wavelength(cls, value: Any, info: ValidationInfo) -> astropy.units.Quantity:
        """Validate the optimized wavelength input.

        :param value: Value given as input
        :param info: ValidationInfo object
        :return: The optimized wavelength in units of length
        """
        return validate_quantity_units(value=value, field_name=info.field_name, unit_equivalency=u.m)

    def set_optimal_baseline(self):
        """Set the baseline to optimize for the habitable zone, if it is between the minimum and maximum allowed
        baselines.
        """
        star = [value for _, value in self.sources.items() if isinstance(value, Star)][0]
        optimal_baseline = self.observatory.array_configuration.get_optimal_baseline(
            wavelength=self.optimized_wavelength,
            optimal_angular_distance=star.habitable_zone_central_angular_radius).to(u.m)

        if self.observatory.array_configuration.baseline_minimum <= optimal_baseline and optimal_baseline <= self.observatory.array_configuration.baseline_maximum:
            self.observatory.array_configuration.baseline = optimal_baseline
        else:
            raise ValueError(
                f'Optimal baseline of {optimal_baseline} is not within allowed ranges of baselines {self.observatory.array_configuration.baseline_minimum}-{self.observatory.array_configuration.baseline_maximum}')
