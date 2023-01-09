from positive import Positive

class Planet:
    def __init__(
        self,
        name,
        radius_metres,
        mass_kilograms,
        orbital_period_seconds,
        surface_temperature_kelvin,
    ):
        self.name = name
        self.radius_metres = radius_metres
        self.mass_kilograms = mass_kilograms
        self.orbital_period_seconds = orbital_period_seconds
        self.surface_temperature_kelvin = surface_temperature_kelvin

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value:
            raise ValueError("Cannot set empty name")
        self._name = value

    radius_metres = Positive()
    mass_kilograms = property(
    )

    def _get_orbital_period_seconds(self):
        return self._orbital_period_seconds

    def _set_orbital_period_seconds(self, value):
        if value <= 0:
            raise ValueError(f"orbital_period_seconds value {value} is not positive.")
        self._orbital_period_seconds = value

    orbital_period_seconds = property(
        fget=_get_orbital_period_seconds,
        fset=_set_orbital_period_seconds,
    )

    def _get_surface_temperature_kelvin(self):
        return self._surface_temperature_kelvin

    def _set_surface_temperature_kelvin(self, value):
        if value <= 0:
            raise ValueError(f"surface_temperature_kelvin value {value} is not positive.")
        self._surface_temperature_kelvin = value

    surface_temperature_kelvin = property(
        fget=_get_surface_temperature_kelvin,
        fset=_set_surface_temperature_kelvin,
    )
