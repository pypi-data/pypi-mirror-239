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

from conf_ini_g.phase.specification.base import base_t
from conf_ini_g.phase.specification.parameter.main import parameter_t
from conf_ini_g.phase.specification.section.controller import controller_t


@dtcl.dataclass(repr=False, eq=False)
class section_t(base_t):
    category: str = "Main"
    optional: bool = False
    is_growable: bool = False  # True by default if no parameters are specified.
    parameters: list[parameter_t] | None = None
    controller: controller_t = None
    alternatives: dict[str, list[parameter_t]] = None

    def __post_init__(self) -> None:
        """"""
        if self.parameters is None:
            self.is_growable = True

    @property
    def controlling_values(self) -> tuple[str, ...]:
        """
        Call only on controlled sections.
        """
        if self.controller.primary_value is None:
            # The controlling values are not mentioned in the specification. They will
            # be set programmatically later on.
            return ()

        if self.alternatives is None:
            # The controlling values are not mentioned in the specification. They are
            # being set programmatically.
            return (self.controller.primary_value,)

        return (self.controller.primary_value,) + tuple(self.alternatives.keys())

    def Issues(self) -> list[str]:
        """"""
        output = super().Issues()

        if self.parameters is not None:
            valid_name_sets = [tuple(_prm.name for _prm in self.parameters)]
            if self.alternatives is not None:
                for parameters in self.alternatives.values():
                    valid_name_sets.append(tuple(_prm.name for _prm in parameters))
            for valid_name_set in valid_name_sets:
                if valid_name_set.__len__() > set(valid_name_set).__len__():
                    output.append(
                        f"{self.name}: Section with repeated parameter names "
                        f"(possibly in alternatives)"
                    )

        basic = self.basic
        optional = self.optional

        if not (basic or optional):
            output.append(f"{self.name}: Section is not basic but not optional")

        if (
            (self.controller is None)
            and (not optional)
            and ((self.parameters is None) or (self.parameters.__len__() == 0))
        ):
            output.append(f"{self.name}: Empty mandatory section")

        if self.parameters is not None:
            n_parameters = 0
            n_basic_prms = 0
            for parameter in self.parameters:
                output.extend(f"/{self.name}/ {_iss}" for _iss in parameter.Issues())

                n_parameters += 1
                if parameter.basic:
                    n_basic_prms += 1

                if parameter.basic and not basic:
                    output.append(
                        f'{parameter.name}: Basic parameter in '
                        f'advanced section "{self.name}"'
                    )
                if optional and not parameter.optional:
                    output.append(
                        f'{parameter.name}: Mandatory parameter in '
                        f'optional section "{self.name}"'
                    )

            if (n_parameters == 0) and not self.is_growable:
                output.append(
                    f"{self.name}: Section without specified parameters "
                    f"which does not accept unspecified parameters"
                )
            if basic and (n_parameters > 0) and (n_basic_prms == 0):
                output.append(
                    f"{self.name}: Basic section without any basic parameters"
                )

        if self.controller is None:
            if self.alternatives is not None:
                output.append(f"{self.name}: Uncontrolled section with alternatives")
        else:
            if self.controller.section == self.name:
                output.append(f"{self.name}: Section cannot be controlled by itself")
            controlling_values = self.controlling_values
            if controlling_values.__len__() > set(controlling_values).__len__():
                output.append(
                    f"{self.name}: Controlled section has duplicated controller values"
                )
            if self.parameters is not None:
                for parameter in self.parameters:
                    if not parameter.optional:
                        output.append(
                            f'{parameter.name}: Mandatory parameter in '
                            f'controlled section "{self.name}"'
                        )

            if self.controller.primary_value is None:
                if self.alternatives is not None:
                    output.append(
                        f"{self.name}: Controlled section without primary value"
                    )
                # else: This will be set programmatically later on.
            elif self.alternatives is None:
                output.append(f"{self.name}: Controlled section without alternatives")

        return output
