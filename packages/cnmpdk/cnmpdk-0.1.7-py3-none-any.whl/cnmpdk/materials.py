" Based in gdsfactory/gdsfactory/generic_tech/simulation_settings.py "

from __future__ import annotations

from functools import partial
from typing import TYPE_CHECKING

import numpy as np
from pydantic import BaseModel
from scipy import interpolate

import numpy as np
import tidy3d as td

if TYPE_CHECKING:
    pass
nm = 1e-3

def _interpolate_material(wav: np.ndarray, wavelengths, refractive_index) -> np.ndarray:
    """Returns Interpolated refractive index of material for given wavelength.

    Args:
        wav: wavelength (um) to interpolate.
        wavelengths: list of reference wavelengths (um).
        refractive_index: list of reference refractive indices.
    """
    f = interpolate.interp1d(wavelengths, refractive_index)
    return f(wav)

cnm_wavelengths = [
    0.600,
    0.700,
    0.800,
    0.900,
    1.0,
    1.1,
    1.2,
    1.3,
    1.4,
    1.5,
    1.6,
    1.7,
    1.8,
    1.9,
    2.0,
]

refractive_indices_cnm_nitride = [
    2.0215222,
    2.0096571,
    2.0019563,
    1.9966765,
    1.9929,
    1.9901058,
    1.9879806,
    1.9863266,
    1.9850143,
    1.9839556,
    1.9830891,
    1.9823709,
    1.9817691,
    1.9812598,
]

refractive_indices_cnm_oxide = [
    1.4594667,
    1.4551134,
    1.4522938,
    1.450366,
    1.4489918,
    1.4479795,
    1.4472136,
    1.4466212,
    1.4461547,
    1.4457816,
    1.4454793,
    1.4452316,
    1.4450268,
    1.4448561,
]

cnm_sinx = partial(
    _interpolate_material,
    wavelengths=cnm_wavelengths,
    refractive_index=refractive_indices_cnm_nitride,
)

#TODO: Add Silicon

cnm_sio2 = partial(
    _interpolate_material,
    wavelengths=cnm_wavelengths,
    refractive_index=refractive_indices_cnm_oxide,
)

wavelength = np.linspace(600, 2000, 15) * nm

f = td.C_0 / wavelength

Cr_eps_complex = td.material_library["Cr"]["Rakic1998BB"].eps_model(f)
n_Cr, k_Cr = td.Medium.eps_complex_to_nk(Cr_eps_complex)

Au_eps_complex = td.material_library["Au"]["Olmon2012crystal"].eps_model(f)
n_Au, k_Au = td.Medium.eps_complex_to_nk(Au_eps_complex)

#TODO: Avoid using partials for this one
cnm_Au = partial(
    _interpolate_material,
    wavelengths=cnm_wavelengths,
    refractive_index=n_Au,
)

#TODO: Avoid using partials for this one
cnm_Cr = partial(
    _interpolate_material,
    wavelengths=cnm_wavelengths,
    refractive_index=n_Cr,
)

cnm_materials_index = {"SiN": cnm_sinx,
                        "SiO2": cnm_sio2,
                        "Au": cnm_Au,       # TODO: Add Losses (imag part)
                        "Cr": cnm_Cr        # TODO: Add Losses (imag part)
                    }

if __name__ == "__main__":
    print(cnm_sinx(1.55))