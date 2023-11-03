# Copyright 2021 Google LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numpy as np
import pandas as pd
from absl.testing import absltest

from temporian.implementation.numpy.data.io import event_set
from temporian.core.operators.binary import (
    EqualOperator,
    NotEqualOperator,
    GreaterEqualOperator,
    GreaterOperator,
    LessEqualOperator,
    LessOperator,
)
from temporian.implementation.numpy.operators.binary import (
    EqualNumpyImplementation,
    NotEqualNumpyImplementation,
    GreaterEqualNumpyImplementation,
    GreaterNumpyImplementation,
    LessEqualNumpyImplementation,
    LessNumpyImplementation,
)
from temporian.io.pandas import from_pandas
from temporian.implementation.numpy.operators.test.utils import (
    assertEqualEventSet,
    testOperatorAndImp,
)


class ArithmeticNumpyImplementationTest(absltest.TestCase):
    """Test numpy implementation of all arithmetic operators:
    addition, subtraction, division and multiplication"""

    def setUp(self):
        self.evset_1 = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, 10.0],
                    [0, 2.0, 1.0],
                    [1, 3.0, 12.0],
                    [1, 4.0, np.nan],
                    [2, 5.0, -30.0],
                    [2, 6.0, 0],
                ],
                columns=["store_id", "timestamp", "sales"],
            ),
            indexes=["store_id"],
        )

        self.evset_2 = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, 10.0],
                    [0, 2.0, -1.0],
                    [1, 3.0, 12.000000001],
                    [1, 4.0, np.nan],
                    [2, 5.0, -30.0],
                    [2, 6.0, np.nan],
                ],
                columns=["store_id", "timestamp", "costs"],
            ),
            indexes=["store_id"],
        )
        self.node_1 = self.evset_1.node()
        self.node_2 = self.evset_2.node()

        # FIXME: This should not be necessary
        self.node_2._sampling = self.node_1._sampling
        for index, data in self.evset_1.data.items():
            self.evset_2.data[index].timestamps = data.timestamps

    def test_correct_equal(self) -> None:
        """Test correct equal operator."""
        output_evset = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, True],
                    [0, 2.0, False],
                    [1, 3.0, False],
                    [1, 4.0, False],  # nan == nan is False
                    [2, 5.0, True],
                    [2, 6.0, False],
                ],
                columns=["store_id", "timestamp", "eq_sales_costs"],
            ),
            indexes=["store_id"],
        )
        operator = EqualOperator(input_1=self.node_1, input_2=self.node_2)
        operator.outputs["output"].check_same_sampling(self.node_1)
        operator.outputs["output"].check_same_sampling(self.node_2)

        operator_output = EqualNumpyImplementation(operator).call(
            input_1=self.evset_1, input_2=self.evset_2
        )
        self.assertEqual(output_evset, operator_output["output"])

    def test_equal_str(self) -> None:
        timestamps = [1, 2, 3, 4]
        evset_1 = event_set(
            timestamps=timestamps,
            features={"a": ["A", "A", "B", "B"]},
        )
        evset_2 = event_set(
            timestamps=timestamps,
            features={"b": ["A", "B", "A", "B"]},
            same_sampling_as=evset_1,
        )

        expected_output = event_set(
            timestamps=timestamps,
            features={"eq_a_b": [True, False, False, True]},
        )

        op = EqualOperator(evset_1.node(), evset_2.node())
        instance = EqualNumpyImplementation(op)
        testOperatorAndImp(self, op, instance)
        output = instance.call(input_1=evset_1, input_2=evset_2)["output"]
        assertEqualEventSet(self, output, expected_output)

    def test_notequal_str(self) -> None:
        timestamps = [1, 2, 3, 4]
        evset_1 = event_set(
            timestamps=timestamps,
            features={"a": ["A", "A", "B", "B"]},
        )
        evset_2 = event_set(
            timestamps=timestamps,
            features={"b": ["A", "B", "A", "B"]},
            same_sampling_as=evset_1,
        )

        expected_output = event_set(
            timestamps=timestamps,
            features={"ne_a_b": [False, True, True, False]},
        )

        op = NotEqualOperator(evset_1.node(), evset_2.node())
        instance = NotEqualNumpyImplementation(op)
        testOperatorAndImp(self, op, instance)
        output = instance.call(input_1=evset_1, input_2=evset_2)["output"]
        assertEqualEventSet(self, output, expected_output)

    def test_correct_not_equal(self) -> None:
        """Test correct not-equal operator."""
        output_evset = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, False],
                    [0, 2.0, True],
                    [1, 3.0, True],
                    [1, 4.0, True],  # nan != nan is True
                    [2, 5.0, False],
                    [2, 6.0, True],
                ],
                columns=["store_id", "timestamp", "ne_sales_costs"],
            ),
            indexes=["store_id"],
        )
        operator = NotEqualOperator(input_1=self.node_1, input_2=self.node_2)
        operator_output = NotEqualNumpyImplementation(operator).call(
            input_1=self.evset_1, input_2=self.evset_2
        )
        self.assertEqual(output_evset, operator_output["output"])

    def test_correct_greater(self) -> None:
        output_evset = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, False],
                    [0, 2.0, True],
                    [1, 3.0, False],
                    [1, 4.0, False],  # nan > nan is always False
                    [2, 5.0, False],
                    [2, 6.0, False],  # any comparison to nan is False
                ],
                columns=["store_id", "timestamp", "gt_sales_costs"],
            ),
            indexes=["store_id"],
        )
        operator = GreaterOperator(input_1=self.node_1, input_2=self.node_2)
        operator_output = GreaterNumpyImplementation(operator).call(
            input_1=self.evset_1, input_2=self.evset_2
        )
        self.assertEqual(output_evset, operator_output["output"])

    def test_correct_greater_equal(self) -> None:
        output_evset = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, True],
                    [0, 2.0, True],
                    [1, 3.0, False],
                    [1, 4.0, False],  # nan >= nan is always False
                    [2, 5.0, True],
                    [2, 6.0, False],  # any comparison to nan is False
                ],
                columns=["store_id", "timestamp", "ge_sales_costs"],
            ),
            indexes=["store_id"],
        )
        op = GreaterEqualOperator(input_1=self.node_1, input_2=self.node_2)
        operator_output = GreaterEqualNumpyImplementation(op).call(
            input_1=self.evset_1, input_2=self.evset_2
        )
        self.assertEqual(output_evset, operator_output["output"])

    def test_correct_less(self) -> None:
        output_evset = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, False],
                    [0, 2.0, False],
                    [1, 3.0, True],
                    [1, 4.0, False],  # nan < nan is always False
                    [2, 5.0, False],
                    [2, 6.0, False],  # any comparison to nan is False
                ],
                columns=["store_id", "timestamp", "lt_sales_costs"],
            ),
            indexes=["store_id"],
        )
        op = LessOperator(input_1=self.node_1, input_2=self.node_2)
        operator_output = LessNumpyImplementation(op).call(
            input_1=self.evset_1, input_2=self.evset_2
        )
        self.assertEqual(output_evset, operator_output["output"])

    def test_correct_less_equal(self) -> None:
        output_evset = from_pandas(
            pd.DataFrame(
                [
                    [0, 1.0, True],
                    [0, 2.0, False],
                    [1, 3.0, True],
                    [1, 4.0, False],  # nan <= nan is always False
                    [2, 5.0, True],
                    [2, 6.0, False],  # any comparison to nan is False
                ],
                columns=["store_id", "timestamp", "le_sales_costs"],
            ),
            indexes=["store_id"],
        )
        op = LessEqualOperator(input_1=self.node_1, input_2=self.node_2)
        operator_output = LessEqualNumpyImplementation(op).call(
            input_1=self.evset_1, input_2=self.evset_2
        )
        self.assertEqual(output_evset, operator_output["output"])


if __name__ == "__main__":
    absltest.main()
