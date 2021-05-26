__author__ = 'github.com/arm61'
__version__ = '0.0.1'
"""
Tests for Layer class module
"""

import os
import unittest
import numpy as np
from numpy.testing import assert_almost_equal, assert_equal
from easyReflectometryLib.Experiment.model import Model
from easyReflectometryLib.Sample.material import Material
from easyReflectometryLib.Sample.layer import Layer
from easyReflectometryLib.Sample.layers import Layers
from easyReflectometryLib.Sample.item import Item
from easyReflectometryLib.Sample.structure import Structure
from easyReflectometryLib.interface import InterfaceFactory


class TestModel(unittest.TestCase):
    def test_default(self):
        p = Model.default()
        assert_equal(p.name, 'easyModel')
        assert_equal(p.interface, None)
        assert_equal(p.structure.name, 'easyStructure')
        assert_equal(p.scale.display_name, 'scale')
        assert_equal(str(p.scale.unit), 'dimensionless')
        assert_equal(p.scale.value.n, 1.0)
        assert_equal(p.scale.min, 0.0)
        assert_equal(p.scale.max, np.Inf)
        assert_equal(p.scale.fixed, True)
        assert_equal(p.background.display_name, 'background')
        assert_equal(str(p.background.unit), 'dimensionless')
        assert_almost_equal(p.background.value.n, 1.e-7)
        assert_equal(p.background.min, 0.0)
        assert_equal(p.background.max, np.Inf)
        assert_equal(p.background.fixed, True)
        assert_equal(p.resolution.display_name, 'resolution')
        assert_equal(str(p.resolution.unit), 'dimensionless')
        assert_almost_equal(p.resolution.value.n, 5.0)
        assert_equal(p.resolution.min, 0.0)
        assert_equal(p.resolution.max, np.Inf)
        assert_equal(p.resolution.fixed, True)

    def test_from_pars(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, o2, name='myModel')
        mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel')
        assert_equal(mod.name, 'newModel')
        assert_equal(mod.interface, None)
        assert_equal(mod.structure.name, 'myModel')
        assert_equal(mod.scale.display_name, 'scale')
        assert_equal(str(mod.scale.unit), 'dimensionless')
        assert_equal(mod.scale.value.n, 2.0)
        assert_equal(mod.scale.min, 0.0)
        assert_equal(mod.scale.max, np.Inf)
        assert_equal(mod.scale.fixed, True)
        assert_equal(mod.background.display_name, 'background')
        assert_equal(str(mod.background.unit), 'dimensionless')
        assert_almost_equal(mod.background.value.n, 1.e-5)
        assert_equal(mod.background.min, 0.0)
        assert_equal(mod.background.max, np.Inf)
        assert_equal(mod.background.fixed, True)
        assert_equal(mod.resolution.display_name, 'resolution')
        assert_equal(str(mod.resolution.unit), 'dimensionless')
        assert_almost_equal(mod.resolution.value.n, 2.0)
        assert_equal(mod.resolution.min, 0.0)
        assert_equal(mod.resolution.max, np.Inf)
        assert_equal(mod.resolution.fixed, True)

    def test_add_item(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, name='myModel')
        mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel') 
        assert_equal(len(mod.structure), 1)
        mod.add_item(o2)
        assert_equal(len(mod.structure), 2)
        assert_equal(mod.structure[1].name, 'oneLayerItem2')
        assert_equal(issubclass(mod.structure[1].__class__, Item), True)

    def test_add_item_with_interface_refnx(self):
        interface = InterfaceFactory()
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, name='myModel')
        mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface)
        assert_equal(len(mod.interface().calculator.storage['item']), 1)
        assert_equal(len(mod.interface().calculator.storage['layer']), 2)
        mod.add_item(o2)
        assert_equal(len(mod.interface().calculator.storage['item']), 2)
        assert_equal(len(mod.interface().calculator.storage['layer']), 2)

    def test_duplicate_item(self):
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, name='myModel')
        mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel') 
        assert_equal(len(mod.structure), 1)
        mod.add_item(o2)
        assert_equal(len(mod.structure), 2)
        mod.duplicate_item(1)
        assert_equal(len(mod.structure), 3)
        assert_equal(mod.structure[2].name, 'oneLayerItem2')
        assert_equal(issubclass(mod.structure[2].__class__, Item), True)

    def test_duplicate_item_with_interface_refnx(self):
        interface = InterfaceFactory()
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, name='myModel')
        mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface) 
        assert_equal(len(mod.interface().calculator.storage['item']), 1)
        mod.add_item(o2)
        assert_equal(len(mod.interface().calculator.storage['item']), 2)
        mod.duplicate_item(1)
        assert_equal(len(mod.interface().calculator.storage['item']), 3)

    def test_remove_item_with_interface_refnx(self):
        interface = InterfaceFactory()
        m1 = Material.from_pars(6.908, -0.278, 'Boron')
        m2 = Material.from_pars(0.487, 0.000, 'Potassium')
        l1 = Layer.from_pars(m1, 5.0, 2.0, 'thinBoron')
        l2 = Layer.from_pars(m2, 50.0, 1.0, 'thickPotassium')
        ls1 = Layers.from_pars(l1, l2, name='twoLayer1')
        ls2 = Layers.from_pars(l2, l1, name='twoLayer2')
        o1 = Item.from_pars(ls1, 2.0, 'twoLayerItem1')
        o2 = Item.from_pars(ls2, 1.0, 'oneLayerItem2')
        d = Structure.from_pars(o1, name='myModel')
        mod = Model.from_pars(d, 2, 1e-5, 2.0, 'newModel', interface=interface)
        assert_equal(len(mod.interface().calculator.storage['item']), 1)
        assert_equal(len(mod.interface().calculator.storage['layer']), 2)
        mod.add_item(o2)
        assert_equal(len(mod.interface().calculator.storage['item']), 2)
        assert_equal(len(mod.interface().calculator.storage['layer']), 2)
        mod.remove_item(0)
        assert_equal(len(mod.interface().calculator.storage['item']), 1)
        assert_equal(len(mod.interface().calculator.storage['layer']), 2)

    def test_uid(self):
        p = Model.default()
        assert_equal(p.uid, p._borg.map.convert_id_to_key(p))
    
    def test_repr(self):
        p = Model.default()
        assert_equal(
            p.__repr__(),
            "<easyModel: (structure: easyStructure, scale: 1.000, background: 1.000e-07, resolution: 5.00)>"
        )
