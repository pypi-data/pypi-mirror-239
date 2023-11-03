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

class ListErAttachmentsRequest(RpcRequest):

	def __init__(self):
		RpcRequest.__init__(self, 'eflo', '2022-05-30', 'ListErAttachments','eflo')
		self.set_method('POST')

	def get_PageNumber(self): # Integer
		return self.get_body_params().get('PageNumber')

	def set_PageNumber(self, PageNumber):  # Integer
		self.add_body_params('PageNumber', PageNumber)
	def get_ResourceTenantId(self): # String
		return self.get_body_params().get('ResourceTenantId')

	def set_ResourceTenantId(self, ResourceTenantId):  # String
		self.add_body_params('ResourceTenantId', ResourceTenantId)
	def get_AutoReceiveAllRoute(self): # Boolean
		return self.get_body_params().get('AutoReceiveAllRoute')

	def set_AutoReceiveAllRoute(self, AutoReceiveAllRoute):  # Boolean
		self.add_body_params('AutoReceiveAllRoute', AutoReceiveAllRoute)
	def get_PageSize(self): # Integer
		return self.get_body_params().get('PageSize')

	def set_PageSize(self, PageSize):  # Integer
		self.add_body_params('PageSize', PageSize)
	def get_InstanceType(self): # String
		return self.get_body_params().get('InstanceType')

	def set_InstanceType(self, InstanceType):  # String
		self.add_body_params('InstanceType', InstanceType)
	def get_ErAttachmentName(self): # String
		return self.get_body_params().get('ErAttachmentName')

	def set_ErAttachmentName(self, ErAttachmentName):  # String
		self.add_body_params('ErAttachmentName', ErAttachmentName)
	def get_ErId(self): # String
		return self.get_body_params().get('ErId')

	def set_ErId(self, ErId):  # String
		self.add_body_params('ErId', ErId)
	def get_InstanceId(self): # String
		return self.get_body_params().get('InstanceId')

	def set_InstanceId(self, InstanceId):  # String
		self.add_body_params('InstanceId', InstanceId)
	def get_ErAttachmentId(self): # String
		return self.get_body_params().get('ErAttachmentId')

	def set_ErAttachmentId(self, ErAttachmentId):  # String
		self.add_body_params('ErAttachmentId', ErAttachmentId)
	def get_EnablePage(self): # Boolean
		return self.get_body_params().get('EnablePage')

	def set_EnablePage(self, EnablePage):  # Boolean
		self.add_body_params('EnablePage', EnablePage)
	def get_Status(self): # String
		return self.get_body_params().get('Status')

	def set_Status(self, Status):  # String
		self.add_body_params('Status', Status)
