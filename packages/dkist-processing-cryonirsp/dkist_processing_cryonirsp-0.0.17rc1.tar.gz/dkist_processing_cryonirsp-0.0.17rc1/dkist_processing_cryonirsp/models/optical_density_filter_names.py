"""List of allowable Optical Density Filter names."""
from enum import StrEnum


class AllowableOpticalDensityFilterNames(StrEnum):
    """Enum to implement list of allowable Optical Density Filter names."""

    G358 = "G358"
    G408 = "G408"
    OPEN = "Open"
    NONE = "none"
