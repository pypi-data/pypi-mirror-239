# Copyright CNRS/Inria/UNS
# Contributor(s): Eric Debreuve (since 2021)
#
# eric.debreuve@cnrs.fr
#
# This software is governed by the CeCILL  license under French law and
# abiding by the rules of distribution of free software.  You can  use,
# modify and/ or redistribute the software under the terms of the CeCILL
# license as circulated by CEA, CNRS and INRIA at the following URL
# "http://www.cecill.info".
#
# As a counterpart to the access to the source code and  rights to copy,
# modify and redistribute granted by the license, users are provided only
# with a limited warranty  and the software's author,  the holder of the
# economic rights,  and the successive licensors  have only  limited
# liability.
#
# In this respect, the user's attention is drawn to the risks associated
# with loading,  using,  modifying and/or developing or reproducing the
# software by the user in light of its specific status of free software,
# that may mean  that it is complicated to manipulate,  and  that  also
# therefore means  that it is reserved for developers  and  experienced
# professionals having in-depth computer knowledge. Users are therefore
# encouraged to load and test the software's suitability as regards their
# requirements in conditions enabling the security of their systems and/or
# data to be ensured and,  more generally, to use and operate it in the
# same conditions as regards security.
#
# The fact that you are presently reading this means that you have had
# knowledge of the CeCILL license and that you accept its terms.

import dataclasses as dtcl
import sys as sstm
import textwrap as text
from typing import Any, Sequence

from rich import print as rprint
from rich.text import Text as text_t
from str_to_obj import ObjectFromStr
from str_to_obj.interface.console import TypeAsRichStr
from str_to_obj.type.hint import any_hint_h

from conf_ini_g.catalog.specification.annotation.callable import callable_t
from conf_ini_g.catalog.specification.annotation.choices import choices_t
from conf_ini_g.extension.python import SpecificationPath
from conf_ini_g.interface.storage.parameter import INI_UNIT_SEPARATOR
from conf_ini_g.interface.storage.section import INI_UNIT_SECTION
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.parameter.type import ANY_TYPE, type_t
from conf_ini_g.phase.specification.parameter.unit import unit_t
from conf_ini_g.phase.specification.parameter.value import MISSING_REQUIRED_VALUE
from conf_ini_g.phase.specification.section.main import controller_t, section_t
from conf_ini_g.phase.specification.section.unit import IsUnitSection


@dtcl.dataclass(init=False, repr=False, eq=False)
class config_t(list[section_t]):
    path: str = None

    def __init__(self, sections: Sequence[section_t], /) -> None:
        """
        Raising exceptions is adapted here since execution cannot proceed without a
        valid specification.
        """
        list.__init__(self, sections)

        # After __init__ so that self iterator is usable
        for section in self:
            if (controller := section.controller) is None:
                continue

            if self.GetController(controller).type is ANY_TYPE:
                choices = choices_t.NewAnnotatedType(section.controlling_values)
                self.GetController(controller).type = type_t.NewFromTypeHint(choices)

        self.path = SpecificationPath(sections)

        issues = self.Issues()
        if issues.__len__() > 0:
            rprint(
                self.path,
                "[red]Invalid specification[/]",
                "\n".join(issues),
                sep="\n",
            )
            sstm.exit(1)

    def AddUnitSection(self) -> None:
        """"""
        section = section_t(
            name=INI_UNIT_SECTION,
            definition="Unit definitions",
            description=f"Units can be used in any other section "
            f"to specify a parameter value as follows: "
            f"numerical_value{INI_UNIT_SEPARATOR}unit, e.g., 1.5'mm.",
            basic=True,
            optional=True,
            category=INI_UNIT_SECTION,
            is_growable=True,
        )
        self.append(section)

    def AddPluginParameter(
        self,
        section: str | section_t,
        name: str,
        /,
        *,
        definition: str = "Programmatic plugin parameter",
        description: str = "This parameter is not part of the specification. "
        'It was added programmatically in a "plugin" way.',
        basic: bool = True,
        stripe: any_hint_h | type_t = None,
        default: Any = MISSING_REQUIRED_VALUE,
        controlling_value: str = None,
    ) -> None:
        """
        See definition and description above.
        """
        if isinstance(section, str):
            section = self[section]

        parameter = parameter_t(
            name=name,
            definition=definition,
            description=description,
            basic=basic,
            type=stripe,
            default=default,
        )
        self.AddParameter(
            section, parameter, controlling_value, config_t.AddPluginParameter.__name__
        )

    def AddRuntimeParameter(
        self,
        section: str | section_t,
        name: str,
        value: str | float,
        /,
        *,
        controlling_value: str = None,
    ) -> parameter_t:
        """
        See definition and description below.
        The existence of such a method is justified by the fact that the parameter
        created can be a "normal" parameter or a unit depending on the section.

        value: float if unit.

        /!\ Cannot deal with str values with units.
        """
        if isinstance(section, str):
            section = self[section]

        if IsUnitSection(section.name):
            parameter_or_unit_t = unit_t
            basic = True
            converted = value
            stripe = None  # Correctly set by the constructor.
        else:
            parameter_or_unit_t = parameter_t
            basic = section.basic
            converted, _ = ObjectFromStr(value)
            stripe = type(converted)
        definition = "Programmatic runtime parameter"
        description = (
            "This parameter is not part of the specification. "
            "It was added programmatically because it was found in the INI document, "
            "or passed as a command-line argument."
        )
        parameter = parameter_or_unit_t(
            name=name,
            definition=definition,
            description=description,
            basic=basic,
            type=stripe,
            default=converted,  # Just a trick to prevent error if basic is False.
        )
        self.AddParameter(
            section, parameter, controlling_value, config_t.AddRuntimeParameter.__name__
        )

        return parameter

    def AddParameter(
        self,
        section: section_t,
        parameter: parameter_t,
        controlling_value: str,
        caller: str,
        /,
    ) -> None:
        """"""
        if (controller := section.controller) is None:
            section.append(parameter)
            return

        if controlling_value is None:
            raise ValueError(
                f"{caller}: A Controlling value must be passed for parameter "
                f"{section.name}.{parameter.name}."
            )

        if controller.primary_value is None:
            # controller_t is immutable, so it must be re-created.
            section.controller = controller_t(
                section=controller.section,
                parameter=controller.parameter,
                primary_value=controlling_value,
            )
            controller = section.controller
            section.append(parameter)
            should_update_controller_choices = True
        elif controlling_value == controller.primary_value:
            section.append(parameter)
            should_update_controller_choices = False
        elif section.alternatives is None:
            section.alternatives = {controlling_value: [parameter]}
            should_update_controller_choices = True
        elif controlling_value in section.alternatives:
            section.alternatives[controlling_value].append(parameter)
            should_update_controller_choices = False
        else:
            section.alternatives[controlling_value] = [parameter]
            should_update_controller_choices = True

        if should_update_controller_choices:
            nnts = self.GetController(controller).type.annotations
            if nnts.__len__() > 0:
                first_annotation = nnts[0]
            else:
                first_annotation = None
            if (first_annotation is None) or isinstance(first_annotation, choices_t):
                choices = choices_t.NewAnnotatedType(section.controlling_values)
                new_type = type_t.NewFromTypeHint(choices)
            else:  # Must be callable_t.
                callable_ = callable_t.NewAnnotatedType(
                    kind=first_annotation.kind,
                    catalog=section.controlling_values,
                    allow_external=first_annotation.allow_external,
                )
                new_type = type_t.NewFromTypeHint(callable_)
            self.GetController(controller).type = new_type

    def Issues(self) -> list[str]:
        """"""
        output = []

        if self.__len__() == 0:
            output.append(f"Empty specification: {self.path}")
            return output

        names = self.section_names
        if names.__len__() > set(names).__len__():
            output.append("Specification with repeated section names")

        for section in self:
            if not isinstance(section, section_t):
                output.append(
                    f"{type(section).__name__}: Invalid section type; Expected={section_t.__name__}."
                )
                continue

            output.extend(section.Issues())
            if section.controller is not None:
                if section.controller.section not in self:
                    output.append(
                        f"{section.controller.section}: "
                        f'Unspecified section declared as controller of section "{section.name}"'
                    )
                else:
                    controller_section = self[section.controller.section]
                    if controller_section.controller is not None:
                        output.append(
                            f"{section.controller.section}: "
                            f'Section controlling "{section.name}" is itself controlled'
                        )
                    if section.controller.parameter not in controller_section:
                        output.append(
                            f"{section.controller.section}.{section.controller.parameter}: "
                            f'Unspecified parameter declared as controller of section "{section.name}"'
                        )
                    else:
                        controller_parameter = controller_section[
                            section.controller.parameter
                        ]
                        if controller_parameter.optional:
                            output.append(
                                f"{section.controller.section}.{section.controller.parameter}: "
                                f'Optional parameter declared as controller of section "{section.name}"'
                            )

        return output

    @property
    def section_names(self) -> Sequence[str]:
        """"""
        return tuple(_sct.name for _sct in self)

    def GetController(self, controller: controller_t, /) -> parameter_t:
        """"""
        return self[controller.section][controller.parameter]

    def _Item(self, key: str | int, /) -> section_t | None:
        """"""
        if isinstance(key, int):
            return list.__getitem__(self, key)

        for section in self:
            if section.name == key:
                return section

        return None

    def __contains__(self, key: str, /) -> bool:
        """"""
        return self._Item(key) is not None

    def __getitem__(self, key: str | int, /) -> section_t:
        """"""
        item = self._Item(key)
        if item is None:
            raise KeyError(f"{key}: Not a section of config.")

        return item

    def AsDict(self) -> dict[str, dict[str, Any]]:
        """"""
        return {_sct.name: _sct.AsDict() for _sct in self}

    def __str__(self) -> str:
        """"""
        return text_t.from_markup(self.__rich__()).plain

    def __rich__(self) -> str:
        """"""
        output = [
            TypeAsRichStr(self),
            f"    [blue]path[/]={self.path}" f"[yellow]:{type(self.path).__name__}[/]",
        ]

        for section in self:
            output.append(text.indent(section.__rich__(), "    "))

        return "\n".join(output)
