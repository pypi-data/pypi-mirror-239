#!/usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
import numpy

from pathlib import Path

from MPSTools.material_catalogue.loader import get_silica_index


def load_fiber_as_dict(fiber_name: str, wavelength: float = None) -> dict:
    """
    Loads the fiber parameters as dictionary.

    :param      fiber_name:      The fiber name
    :type       fiber_name:      str
    :param      wavelength:      The wavelength, can be None if no material is describing the fiber
    :type       wavelength:      float

    :returns:   The fiber parameters
    :rtype:     dict
    """
    output_dict = {}

    cwd = Path(__file__).parent

    file = cwd.joinpath(f'./fiber_files/{fiber_name}.yaml')

    assert file.exists(), f'Fiber file: {fiber_name} does not exist.'

    configuration = yaml.safe_load(file.read_text())

    outer_layer = None
    for layer_idx, current_layer in configuration['layers'].items():

        output_dict[layer_idx] = current_layer

        index = current_layer.get('index')
        NA = current_layer.get('NA')
        name = current_layer.get('name')
        radius = current_layer.get('radius')
        material = current_layer.get('material')

        if outer_layer is not None:
            assert radius <= outer_layer.get('radius'), f'Layer declaration order for {file} is not from outer-most to inner-most as it should be.'

        assert numpy.count_nonzero([material, NA, index]), f"Either NA or index has to be provided for the layer: {name}."

        if NA is not None:
            assert bool(outer_layer), 'Cannot compute NA if no outer layer is defined.'
            output_dict[layer_idx]['index'] = numpy.sqrt(NA**2 + outer_layer.get('index')**2)

        if material == 'silica':
            assert bool(wavelength), 'Cannot evaluate material refractive index if wavelength is not provided.'
            output_dict[layer_idx]['index'] = get_silica_index(wavelength=wavelength)

        outer_layer = output_dict[layer_idx]

    return output_dict


# -
