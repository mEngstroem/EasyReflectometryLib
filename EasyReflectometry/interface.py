__author__ = 'github.com/wardsimon'

from easyCore.Objects.Inferface import InterfaceFactoryTemplate

from EasyReflectometry.calculators import InterfaceTemplate


class InterfaceFactory(InterfaceFactoryTemplate):
    def __init__(self):
        super(InterfaceFactory, self).__init__(InterfaceTemplate._interfaces)

    def reset_storage(self) -> None:
        return self().reset_storage()

    def sld_profile(self, model_id: str) -> tuple:
        return self().sld_profile(model_id)
