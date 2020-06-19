# Lint as: python2, python3
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
"""Tests for tfx.dsl.component.experimental.kubeflow_container_component."""

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import mock
import tensorflow as tf
from tfx.dsl.component.experimental import placeholders, container_component
from tfx.dsl.component.experimental.kubeflow_container_component import create_kubeflow_container_component
from tfx.types.experimental.simple_artifacts import File

class KubeflowContainerComponentTest(tf.test.TestCase):

  def setUp(self):
    super(KubeflowContainerComponentTest, self).setUp()
    self._testdata_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
        'component/experimental/testdata')

  
  def testCreateComponent(self):
    component = create_kubeflow_container_component(os.path.join(self._testdata_path, 'kubeflow_container_component_test.yaml'))
    ref_component = container_component.create_container_component(
      "Test_KubeFlow_Container_Component", 
      "image1", 
      [
        "command1", 
        "command2", 
        "command3", 
        placeholders.InputUriPlaceholder("Directory"),
        placeholders.InputValuePlaceholder("Subpath"),
        placeholders.OutputUriPlaceholder("File"),
        "--arg1", placeholders.InputValuePlaceholder("input3"),
        "--arg2", placeholders.InputUriPlaceholder("input4"),
        "--arg3", placeholders.OutputUriPlaceholder("output2")
      ],
      {
        "input1": File,
        "input2": File
      },
      {
        "output1": File
      },
      {}
    )
    self.assertEqual(type(component), type(ref_component))
    self.assertEqual(ref_component.__dict__['EXECUTOR_SPEC'].image, component.__dict__['EXECUTOR_SPEC'].image)
    self.assertEqual(ref_component.__dict__['EXECUTOR_SPEC'].command, component.__dict__['EXECUTOR_SPEC'].command)
