# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

from aliyunsdkcore.request import RpcRequest

class UpdateVccRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'eflo', '2022-05-30', 'UpdateVcc','eflo')
		self.set_method('POST')

	def get_Bandwidth(self): # Integer
		return self.get_body_params().get('Bandwidth')

	def set_Bandwidth(self, Bandwidth):  # Integer
		self.add_body_params('Bandwidth', Bandwidth)
	def get_OrderId(self): # String
		return self.get_body_params().get('OrderId')

	def set_OrderId(self, OrderId):  # String
		self.add_body_params('OrderId', OrderId)
	def get_VccName(self): # String
		return self.get_body_params().get('VccName')

	def set_VccName(self, VccName):  # String
		self.add_body_params('VccName', VccName)
	def get_VccId(self): # String
		return self.get_body_params().get('VccId')

	def set_VccId(self, VccId):  # String
		self.add_body_params('VccId', VccId)
