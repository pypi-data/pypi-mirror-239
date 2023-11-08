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
from typing import Any, ClassVar, Sequence

from str_to_obj import annotation_t
from str_to_obj.type.hint import any_hint_h

from conf_ini_g.phase.specification.parameter.type import type_t


@dtcl.dataclass(repr=False, eq=False)
class collection_t(annotation_t):
    # Items of any type but None
    ANY_ITEMS_TYPES: ClassVar[Any | tuple[Any, ...]] = Any
    ANY_LENGTH: ClassVar[tuple[int, ...]] = (0,)

    ACCEPTED_TYPES = (list, set, tuple)
    items_types: any_hint_h | tuple[any_hint_h, ...] | type_t | tuple[
        type_t, ...
    ] = ANY_ITEMS_TYPES
    lengths: int | tuple[int, ...] = ANY_LENGTH

    def __post_init__(self) -> None:
        """"""
        original_item_types = self.items_types
        original_lengths = self.lengths

        if isinstance(self.items_types, Sequence):
            items_types = []
            for stripe in self.items_types:
                if isinstance(stripe, type_t):
                    items_types.append(stripe)
                else:
                    items_types.append(type_t.NewFromTypeHint(stripe))
            self.items_types = items_types
        elif not isinstance(self.items_types, type_t):
            self.items_types = type_t.NewFromTypeHint(self.items_types)

        if isinstance(self.lengths, int):
            self.lengths = (self.lengths,)
        else:
            self.lengths = tuple(sorted(self.lengths))

        if isinstance(self.items_types, Sequence):
            if max(self.lengths) > self.items_types.__len__():
                raise ValueError(
                    f"{original_item_types}/{original_lengths}: Allowed length(s) must "
                    f"not exceed the length of the item types sequence."
                )

    def Issues(self) -> list[str]:
        """"""
        output = []

        if self.lengths != self.__class__.ANY_LENGTH:
            for length in self.lengths:
                if (not isinstance(length, int)) or (length < 0):
                    output.append(
                        f"{length}: Invalid sequence length in {self}; "
                        f"Expected=strictly positive integer"
                    )

        return output

    def ValueIsCompliant(self, value: tuple, /) -> list[str]:
        """"""
        if (self.lengths != self.__class__.ANY_LENGTH) and (
            value.__len__() not in self.lengths
        ):
            return [
                f"{value}: Sequence of invalid length; "
                f"Expected={' or '.join(map(str, self.lengths))}."
            ]

        if isinstance(self.items_types, Sequence):
            if value.__len__() > self.items_types.__len__():
                return [
                    f"{value}: Sequence too long. Expected=At most {self.items_types.__len__()} element(s)."
                ]

            output = []
            for stripe, element in zip(self.items_types, value):
                output.extend(stripe.ValueIsCompliant(element))
            return output

        stripe: type_t = self.items_types
        output = []
        for element in value:
            output.extend(stripe.ValueIsCompliant(element))
        return output
