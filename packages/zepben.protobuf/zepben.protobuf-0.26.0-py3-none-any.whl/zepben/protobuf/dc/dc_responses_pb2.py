# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/dc/dc-responses.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.dc import dc_data_pb2 as zepben_dot_protobuf_dot_dc_dot_dc__data__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n%zepben/protobuf/dc/dc-responses.proto\x12\x12zepben.protobuf.dc\x1a zepben/protobuf/dc/dc-data.proto\"y\n\x1cGetIdentifiedObjectsResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x46\n\x11identifiedObjects\x18\x02 \x03(\x0b\x32+.zepben.protobuf.dc.DiagramIdentifiedObject\"v\n\x19GetDiagramObjectsResponse\x12\x11\n\tmessageId\x18\x01 \x01(\x03\x12\x46\n\x11identifiedObjects\x18\x02 \x03(\x0b\x32+.zepben.protobuf.dc.DiagramIdentifiedObjectB/\n\x16\x63om.zepben.protobuf.dcP\x01\xaa\x02\x12Zepben.Protobuf.DCb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'zepben.protobuf.dc.dc_responses_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n\026com.zepben.protobuf.dcP\001\252\002\022Zepben.Protobuf.DC'
  _globals['_GETIDENTIFIEDOBJECTSRESPONSE']._serialized_start=95
  _globals['_GETIDENTIFIEDOBJECTSRESPONSE']._serialized_end=216
  _globals['_GETDIAGRAMOBJECTSRESPONSE']._serialized_start=218
  _globals['_GETDIAGRAMOBJECTSRESPONSE']._serialized_end=336
# @@protoc_insertion_point(module_scope)
