"""Contains functions for calculating dissociation rates
"""
__author__ = 'George Oblapenko'
__license__ = "GPL"
__maintainer__ = "George Oblapenko"
__email__ = "kunstmord@kunstmord.com"
__status__ = "Production"

import numpy as np
from scipy import constants
from .crosssection import raw_diss_integral_rigid_sphere
from .particles import MoleculeSTS, Molecule


def k_diss_eq(T: float, model_data: np.ndarray, molecule_diss: float) -> float:
    """Calculates the equilibrium dissociation rate constant using the Arrhenius model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    model_data : 1-D array-like
        dissociation model data
    molecule_diss : float
        the dissociation energy of the molecule

    Returns
    -------
    float
        Equilibrium dissociation rate constant

    """
    return raw_k_diss_eq(T, model_data[0], model_data[1], molecule_diss)


def diss_rate_treanor_marrone_sts(T: float, model_data: np.ndarray, molecule: MoleculeSTS, i: int,
                                  model: str='D6k') -> float:
    """Calculates the state-to-state non-equilibrium rate constant using the Treanor-Marrone model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    model_data : 1-D array-like
        dissociation model data
    molecule : MoleculeSTS or Molecule
        the molecule which dissociates
    i : int
        the vibrational level from which the molecule dissociates
    model : str
        the model for the `U` parameter to be used, possible values:
            * ``'inf'`` - the U parameter in the non-equilbrium factor
              will be equal to :math:`\\infty`
            * ``'D6k'`` - the U parameter in the non-equilbrium factor will be equal
              to :math:`D / 6k`, where :math:`D` is the dissociation energy of the molecule
            * ``'3T'`` - the U parameter in the non-equilbrium factor will be equal to :math:`3T`

        defaults to 'D6k'

    Returns
    -------
    float
        Non-equilibrium dissociation state-to-state rate constant

    """
    return raw_diss_rate_treanor_marrone_sts(T, model_data[0], model_data[1], molecule.Z_diss(i, T, model),
                                             molecule.diss)


def diss_rate_rigid_sphere_sts(T: float, idata: np.ndarray, molecule: MoleculeSTS, i: int,
                               center_of_mass: bool=True, vl_dependent: bool=True) -> float:
    """Calculates the state-to-state non-equilibrium rate constant using the rigid-sphere crosssection

    Parameters
    ----------
    T : float
        the temperature of the mixture
    idata : 1-D array-like
        the array of interaction data
    molecule : MoleculeSTS or Molecule
        the molecule which dissociates
    i : int
        the vibrational level from which the molecule dissociates (if ``vl_dependent``
        is ``False``, can be any value)
    center_of_mass : bool, optional
        if ``True``, the kinetic energy of the collision partners will be calculated along the center-of-mass line,
        if ``False``, the total kinetic energy will be used, defaults to ``True``
    vl_dependent : bool, optional
        if ``True``, the dissociation crosssection takes into account the vibrational energy of the
        dissociating molecule,
        if ``False``, the crosssection is independent of the vibrational energy, defaults to ``True``

    Returns
    -------
    float
        Non-equilibrium dissociation state-to-state rate constant
    """
    return raw_diss_rate_rigid_sphere_sts(T, idata[1], idata[0], molecule.vibr[i], molecule.diss, center_of_mass,
                                          vl_dependent)


def diss_rate_treanor_marrone(T: float, T1: float, model_data: np.ndarray, molecule: Molecule,
                              model: str='D6k') -> float:
    """Calculates the multi(one)-temperature non-equilibrium rate constant using the Treanor-Marrone model

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule which dissociates
    model_data : 1-D array-like
        dissociation model data
    molecule : Molecule
        the molecule which dissociates
    model : str
        the model for the `U` parameter to be used, possible values:
            * 'inf' - the U parameter in the non-equilbrium factor
              will be equal to :math:`\\infty`
            * 'D6k' - the U parameter in the non-equilbrium factor will be equal
              to :math:`D / 6k`, where :math:`D` is the dissociation energy of the molecule
            * if equal to '3T', the U parameter in the non-equilbrium factor will be equal to :math:`3T`

        defaults to 'D6k'

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant

    """
    res = 0.0
    for i in range(molecule.num_vibr_levels(T, T1, True) + 1):
        res += molecule.vibr_exp(i, T, T1)\
               * raw_diss_rate_treanor_marrone_sts(T, model_data[0], model_data[1],
                                                   molecule.Z_diss(i, T, model), molecule.diss)
    return res / molecule.Z_vibr(T, T1)


def diss_rate_rigid_sphere(T: float, T1: float, idata: np.ndarray, molecule: Molecule,
                           center_of_mass: bool=True, vl_dependent: bool=True) -> float:
    """Calculates the multi(one)-temperature non-equilibrium rate constant using the rigid-sphere crosssection

    Parameters
    ----------
    T : float
        the temperature of the mixture
    T1 : float
        the temperature of the first vibrational level of the molecule which dissociates
    idata : 1-D array-like
        the array of interaction data
    molecule : Molecule
        the molecule which dissociates
    center_of_mass : bool, optional
        if ``True``, the kinetic energy of the collision partners will be calculated along the center-of-mass line,
        if ``False``, the total kinetic energy will be used, defaults to ``True``
    vl_dependent : bool, optional
        if ``True``, the dissociation crosssection takes into account the vibrational energy of the
        dissociating molecule,
        if ``False``, the crosssection is independent of the vibrational energy, defaults to ``True``

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant
    """
    res = 0.0
    for i in range(molecule.num_vibr_levels(T, T1, True) + 1):
        res += molecule.vibr_exp(i, T, T1)\
               * raw_diss_rate_rigid_sphere_sts(T, idata[1], idata[0], molecule.vibr[i], molecule.diss, center_of_mass,
                                                vl_dependent)
    return res / molecule.Z_vibr(T, T1)


def raw_k_diss_eq(T: float, arrhenius_n: float, arrhenius_A: float, molecule_diss: float) -> float:
    """Calculates the equilibrium dissociation rate constant using the Arrhenius model, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    arrhenius_n : float
        Arrhenius model n parameter
    arrhenius_A : float
        Arrhenius model A parameter
    molecule_diss : float
        the dissociation energy of the molecule

    Returns
    -------
    float
        Equilibrium dissociation rate constant

    """
    return arrhenius_A * (T ** arrhenius_n) * np.exp(-molecule_diss / (constants.k * T))


def raw_diss_rate_treanor_marrone_sts(T: float, arrhenius_n: float, arrhenius_A: float, Z_diss: float,
                                      molecule_diss: float) -> float:
    """Calculates the state-to-state non-equilibrium rate constant using the Treanor-Marrone model, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    arrhenius_n : float
        Arrhenius model n parameter
    arrhenius_A : float
        Arrhenius model A parameter
    Z_diss : float
        the non-equilibrium factor
    molecule_diss : float
        the dissociation energy of the molecule

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant

    """
    return Z_diss * raw_k_diss_eq(T, arrhenius_n, arrhenius_A, molecule_diss)


def raw_diss_rate_rigid_sphere_sts(T: float, sigma: float, mass: float, molecule_vibr: float, molecule_diss: float,
                                   center_of_mass: bool=True, vl_dependent: bool=True) -> float:
    """Calculates the state-to-state non-equilibrium rate constant using the rigid-sphere crosssection, *raw* version

    Parameters
    ----------
    T : float
        the temperature of the mixture
    sigma : float
        the collision diameter :math:`\\sigma_{cd}`
    mass : float
        the collision-reduced mass :math:`m_{cd}`
    molecule_vibr : float
        the dimensional vibrational energy of the level from which the molecule dissociates (if ``vl_dependent``
        is ``False``, can be any value)
    molecule_diss : float
        the dissociation energy of the molecule which dissociates
    center_of_mass : bool, optional
        if ``True``, the kinetic energy of the collision partners will be calculated along the center-of-mass line,
        if ``False``, the total kinetic energy will be used, defaults to ``True``
    vl_dependent : bool, optional
        if ``True``, the dissociation crosssection takes into account the vibrational energy of the
        dissociating molecule,
        if ``False``, the crosssection is independent of the vibrational energy, defaults to ``True``

    Returns
    -------
    float
        Non-equilibrium dissociation rate constant
    """
    return 8.0 * raw_diss_integral_rigid_sphere(T, 0, sigma, mass, molecule_vibr, molecule_diss, center_of_mass,
                                                vl_dependent, False)