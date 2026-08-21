# Copyright 2026 Greenmoo Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.

"""Carbon emission metrics and grid intensity calculations for Greenmoo."""

# Global average carbon intensity of electricity generation (approximate gCO2eq/kWh)
# Source: International Energy Agency (IEA) global averages or standard default benchmarks
DEFAULT_CARBON_INTENSITY = 475.0  # gCO2eq / kWh

class CarbonTracker:
    """Calculates carbon emissions resulting from neural network training energy consumption.

    Parameters
    ----------
    carbon_intensity : float, optional
        The carbon intensity of the local electricity grid in gCO2eq/kWh. 
        Defaults to the global average (~475.0 gCO2eq/kWh).
    """

    def __init__(self, carbon_intensity: float = DEFAULT_CARBON_INTENSITY):
        self.carbon_intensity = float(carbon_intensity)

    def energy_to_carbon_g(self, energy_joules: float) -> float:
        """Converts energy consumed in Joules to carbon emissions in grams of CO2 equivalent (gCO2eq).

        Conversion logic:
        1 Joule = 1 Watt-second
        1 kWh = 3,600,000 Joules
        Carbon (g) = Energy (kWh) * Carbon Intensity (gCO2eq / kWh)
        """
        if energy_joules < 0:
            raise ValueError("Energy consumption in Joules cannot be negative.")
        
        energy_kwh = energy_joules / 3600000.0
        carbon_grams = energy_kwh * self.carbon_intensity
        return carbon_grams

    def energy_kwh_to_carbon_g(self, energy_kwh: float) -> float:
        """Converts energy consumed in kilowatt-hours (kWh) directly to carbon emissions in grams (gCO2eq)."""
        if energy_kwh < 0:
            raise ValueError("Energy consumption in kWh cannot be negative.")
        
        return energy_kwh * self.carbon_intensity


def calculate_carbon_emissions(energy_consumption: float, unit: str = "joules", carbon_intensity: float = DEFAULT_CARBON_INTENSITY) -> float:
    """Standalone utility function to calculate carbon emissions.

    Parameters
    ----------
    energy_consumption : float
        The total energy consumed during training.
    unit : str
        The unit of the energy measurement ('joules' or 'kwh').
    carbon_intensity : float
        Grid carbon intensity in gCO2eq/kWh.

    Returns
    -------
    float
        Total carbon emissions in grams of CO2 equivalent (gCO2eq).
    """
    tracker = CarbonTracker(carbon_intensity=carbon_intensity)
    
    if unit.lower() in ("joules", "j"):
        return tracker.energy_to_carbon_g(energy_consumption)
    elif unit.lower() in ("kwh", "kilowatt-hour"):
        return tracker.energy_kwh_to_carbon_g(energy_consumption)
    else:
        raise ValueError(f"Unsupported energy unit '{unit}'. Use 'joules' or 'kwh'.")