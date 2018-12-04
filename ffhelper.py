from ctypes import *

import os
sz_ff_helper = os.environ['PWD']+'/libffmpeg-helper.so'
libffhelper = CDLL(sz_ff_helper)
assert(libffhelper)

libffhelper.GetCodecParamFromFormatContext.argtypes = [c_void_p]
libffhelper.GetCodecParamFromFormatContext.restype = c_void_p
def get_cedec_param_from_format_context(p_ic: c_void_p):
    return libffhelper.GetCodecParamFromFormatContext(p_ic)

libffhelper.GetCodecIdFromCodecContext.argtypes = [c_void_p]
libffhelper.GetCodecIdFromCodecContext.restype = c_int
def get_codec_id_from_codec_context(p_avctx: c_void_p):
    return libffhelper.GetCodecIdFromCodecContext(p_avctx)

class MyAudioFrame(Structure):
    _fields_ = [
        ("data", POINTER(c_int8)),
        ("len", c_int),
        ("sample_rate", c_int),
        ("samples", c_int),
        ("format", c_char_p)
    ]

libffhelper.GetFrameDataFromAVFrame.restype = MyAudioFrame
libffhelper.GetFrameDataFromAVFrame.argtypes = [c_void_p, c_void_p]
def get_frame_data_from_avframe(p_avctx: c_void_p, p_avframe: c_void_p):
    return libffhelper.GetFrameDataFromAVFrame(p_avctx,p_avframe)