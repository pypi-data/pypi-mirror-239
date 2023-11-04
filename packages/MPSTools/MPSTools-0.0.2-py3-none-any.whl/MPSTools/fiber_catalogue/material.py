#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy

# From https://refractiveindex.info/?shelf=main&book=SiO2&page=Malitson
silica_parameters = dict(
    A_0=0.6961663,  # numerator
    A_1=0.0684043,  # denominator
    B_0=0.4079426,
    B_1=0.1162414,
    C_0=0.8974794,
    C_1=9.896161,
)


def dispersion_formula(material_parameters: dict, wavelength: float) -> float:
    index = (material_parameters['A_0'] * wavelength**2) / (wavelength**2 - material_parameters['A_1']**2)
    index += (material_parameters['B_0'] * wavelength**2) / (wavelength**2 - material_parameters['B_1']**2)
    index += (material_parameters['C_0'] * wavelength**2) / (wavelength**2 - material_parameters['C_1']**2)
    index += 1
    index = numpy.sqrt(index)

    return index


def get_silica_index(wavelength: float) -> float:
    index = dispersion_formula(
        material_parameters=silica_parameters,
        wavelength=wavelength
    )

    return index
