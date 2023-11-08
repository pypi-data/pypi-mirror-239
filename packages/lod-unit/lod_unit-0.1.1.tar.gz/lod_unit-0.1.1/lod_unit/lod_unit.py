import astropy.units as u
from astropy.units.equivalencies import Equivalency

# Creating a unit for lambda/D
lod = u.def_unit("λ/D")


def lod_eq(lam, D):
    """
    Function to allow conversion between λ/D and angular units natively
    with the astropy units package
    Args:
        ulod (Astropy Unit):
            The lambda/D unit defined
        lam (Astropy Quantity):
            Wavelength
        D (Astropy Quantity):
            Diameter
    Returns:
        An astropy Equivalency object to allow conversion between λ/D and
        angular units
    Usage:
        >>> diam = 10*u.m
        >>> lam = 500*u.nm
        >>> angseparation = 3 * lod
        >>> angseparation.to(u.arcsec, lod_equiv(lam, diam))
            <Quantity 0.03093972 arcsec>

    """
    base_equivalence = [
        (
            lod,
            u.rad,
            lambda x: x * (lam / D).decompose().value,
            lambda x: x * (D / lam).decompose().value,
        )
    ]
    return Equivalency(base_equivalence)
