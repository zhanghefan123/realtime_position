# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: node/node.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x0fnode/node.proto\"\xbc\x01\n\x04Node\x12\x17\n\x04type\x18\x01 \x01(\x0e\x32\t.NodeType\x12\n\n\x02id\x18\x02 \x01(\x05\x12\x16\n\x0e\x63ontainer_name\x18\x03 \x01(\t\x12\x0b\n\x03pid\x18\x04 \x01(\x05\x12\x0b\n\x03tle\x18\x05 \x03(\t\x12\x17\n\x0finterface_delay\x18\x06 \x03(\t\x12\x10\n\x08latitude\x18\x07 \x01(\x02\x12\x11\n\tlongitude\x18\x08 \x01(\x02\x12\x10\n\x08\x61ltitude\x18\t \x01(\x02\x12\r\n\x05ifIdx\x18\n \x01(\x05*A\n\x08NodeType\x12\x17\n\x13NODE_TYPE_SATELLITE\x10\x00\x12\x1c\n\x18NODE_TYPE_GROUND_STATION\x10\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'node.node_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _NODETYPE._serialized_start=210
  _NODETYPE._serialized_end=275
  _NODE._serialized_start=20
  _NODE._serialized_end=208
# @@protoc_insertion_point(module_scope)
