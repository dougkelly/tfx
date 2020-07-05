# Copyright 2020 Google LLC. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Tests for tfx.extensions.experimental.kfp_compatibility.kfp_container_component."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tensorflow as tf
from tfx.dsl.component.experimental import placeholders, container_component
from tfx.extensions.experimental.kfp_compatibility.kfp_container_component import load_kfp_yaml_container_component, _convert_target_fields_to_kv_pair, _get_command_line_argument_type
from tfx.extensions.experimental.kfp_compatibility.proto import kfp_component_spec_pb2
from tfx.types.experimental.simple_artifacts import File

class KubeflowContainerComponentTest(tf.test.TestCase):

  def setUp(self):
    super(KubeflowContainerComponentTest, self).setUp()
    self._testdata_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'experimental/kfp_compatibility/testdata')


  def testCreateComponent(self):
    component = load_kfp_yaml_container_component(
        os.path.join(self._testdata_path,
                     'kfp_container_component_test.yaml')
    )
    ref_component = container_component.create_container_component(
        "Test_Kfp_Container_Component",
        "image1",
        [
            "command1",
            "command2",
            "command3",
            placeholders.InputUriPlaceholder("Directory"),
            placeholders.InputValuePlaceholder("Subpath"),
            placeholders.OutputUriPlaceholder("File"),
            "--arg1", placeholders.InputUriPlaceholder("input1"),
            "--arg2", placeholders.InputValuePlaceholder("input2"),
            "--arg3", placeholders.OutputUriPlaceholder("output1"),
        ],
        {
            "input1": File,
            "input2": File,
        },
        {
            "output1": File,
        },
        {},
    )
    self.assertEqual(type(component), type(ref_component))
    self.assertEqual(ref_component.EXECUTOR_SPEC.image,
                     component.EXECUTOR_SPEC.image)
    self.assertEqual(ref_component.EXECUTOR_SPEC.command,
                     component.EXECUTOR_SPEC.command)


  def testConvertTargetFieldsToKvPair(self):
    test_dict = {
        'implementation': {
            'container': {
                'args': ['arg0'],
                'command': ['command0'],
            }
        }
    }
    ref_dict = {
        'implementation': {
            'container': {
                'args': [{
                    'stringValue': 'arg0',
                }],
                'command': [{
                    'stringValue': 'command0',
                }],
            }
        }
    }
    _convert_target_fields_to_kv_pair(test_dict)
    self.assertEqual(ref_dict, test_dict)


  def testGetCommandLineArgumentType(self):
    command = kfp_component_spec_pb2.CommandlineArgumentTypeWrapper()
    command.stringValue = 'stringValue'
    self.assertEqual(_get_command_line_argument_type(command),
                     'stringValue')


if __name__ == '__main__':
  tf.test.main()
