# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: zepben/protobuf/cim/iec61968/assetinfo/TransformerEndInfo.proto
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


from zepben.protobuf.cim.iec61968.assets import AssetInfo_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61968_dot_assets_dot_AssetInfo__pb2
from zepben.protobuf.cim.iec61970.base.wires import WindingConnection_pb2 as zepben_dot_protobuf_dot_cim_dot_iec61970_dot_base_dot_wires_dot_WindingConnection__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n?zepben/protobuf/cim/iec61968/assetinfo/TransformerEndInfo.proto\x12&zepben.protobuf.cim.iec61968.assetinfo\x1a\x33zepben/protobuf/cim/iec61968/assets/AssetInfo.proto\x1a?zepben/protobuf/cim/iec61970/base/wires/WindingConnection.proto\"\xd0\x04\n\x12TransformerEndInfo\x12:\n\x02\x61i\x18\x01 \x01(\x0b\x32..zepben.protobuf.cim.iec61968.assets.AssetInfo\x12Z\n\x0e\x63onnectionKind\x18\x02 \x01(\x0e\x32\x42.zepben.protobuf.cim.iec61970.base.wires.winding.WindingConnection\x12\x12\n\nemergencyS\x18\x03 \x01(\x05\x12\x11\n\tendNumber\x18\x04 \x01(\x05\x12\x13\n\x0binsulationU\x18\x05 \x01(\x05\x12\x17\n\x0fphaseAngleClock\x18\x06 \x01(\x05\x12\t\n\x01r\x18\x07 \x01(\x01\x12\x0e\n\x06ratedS\x18\x08 \x01(\x05\x12\x0e\n\x06ratedU\x18\t \x01(\x05\x12\x12\n\nshortTermS\x18\n \x01(\x05\x12\x1f\n\x17transformerTankInfoMRID\x18\x0b \x01(\t\x12$\n\x1ctransformerStarImpedanceMRID\x18\x0c \x01(\t\x12#\n\x1b\x65nergisedEndNoLoadTestsMRID\x18\r \x01(\t\x12)\n!energisedEndShortCircuitTestsMRID\x18\x0e \x01(\t\x12(\n groundedEndShortCircuitTestsMRID\x18\x0f \x01(\t\x12#\n\x1bopenEndOpenCircuitTestsMRID\x18\x10 \x01(\t\x12(\n energisedEndOpenCircuitTestsMRID\x18\x11 \x01(\tBW\n*com.zepben.protobuf.cim.iec61968.assetinfoP\x01\xaa\x02&Zepben.Protobuf.CIM.IEC61968.AssetInfob\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'zepben.protobuf.cim.iec61968.assetinfo.TransformerEndInfo_pb2', _globals)
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  DESCRIPTOR._serialized_options = b'\n*com.zepben.protobuf.cim.iec61968.assetinfoP\001\252\002&Zepben.Protobuf.CIM.IEC61968.AssetInfo'
  _globals['_TRANSFORMERENDINFO']._serialized_start=226
  _globals['_TRANSFORMERENDINFO']._serialized_end=818
# @@protoc_insertion_point(module_scope)
