from ctypes import *
from ctypes.util import find_library

class MyAudioFrame(Structure):
    _fields_ = [
        ("data", POINTER(c_int8)),
        ("len", c_int),
        ("sample_rate", c_int),
        ("samples", c_int),
        ("format", c_char_p)
    ]
    # def __init__(self):
    #     self._as_parameter_ = POINTER(MyAudioFrame)


sz_avcodec = find_library("avcodec")
libavcodec = CDLL(sz_avcodec)
print (sz_avcodec, libavcodec)
sz_avformat = find_library("avformat")
libavformat = CDLL(sz_avformat)
print (libavformat)
sz_avutil = find_library("avutil")
libavutil = CDLL(sz_avutil)
print (libavutil)

def Version():
    sz_ver = libavcodec.avcodec_version()
    return sz_ver

import os
sz_ff_helper = os.environ['PWD']+'/libffmpeg-helper.so'
libffhelper = CDLL(sz_ff_helper)
print(libffhelper)

if __name__ == '__main__':
    # ver = Version()
    # print(ver)
    # # frame = MyAudioFrame()
    # libffhelper.test.restype = MyAudioFrame
    # frame = libffhelper.test()
    # print(frame.len)
    sz = b'/home/bmi/Desktop/00001.m4a'
    print('media file name: ', sz)
    filename = c_char_p(sz)
    ic = c_void_p(None)
    print('init AVFormatContext: ', ic)
    libavformat.av_register_all()
    ret = libavformat.avformat_open_input(byref(ic), filename, None, None)
    print('avformat_open_input returned: ',ret)
    print('and AVFormatContext after open: ',ic)

    avctx = c_void_p()
    avctx.value = libavcodec.avcodec_alloc_context3(None)
    print('allocated AVCodecContext: ', avctx)

    ret = libffhelper.OpenDecoder(ic, avctx)

    assert(ret == 0)

    EAGAIN = -11
    AVERROR_EOF = -541478725

    count = 0

    while(True):
        pkt = c_void_p()
        pkt.value = libavcodec.av_packet_alloc()
        if(libavformat.av_read_frame(ic, pkt)<0):
            libavformat.av_packet_free(pkt)
            break
        
        ret = libavcodec.avcodec_send_packet(avctx, pkt)
        if(ret < 0):
            break


        while(ret >= 0):
            avframe = c_void_p()
            libavutil.av_frame_alloc.restype = c_void_p
            avframe.value = libavutil.av_frame_alloc()
            libavcodec.avcodec_receive_frame.restype = c_int
            libavcodec.avcodec_receive_frame.argtypes = [c_void_p, c_void_p]
            ret = libavcodec.avcodec_receive_frame(avctx, avframe)
            # if (ret != 0):
            #     print(ret)
            if (ret == EAGAIN or ret == AVERROR_EOF):
                libavcodec.av_frame_free(avframe)
                break
            
            count+=1
            print(count)

            frame = MyAudioFrame()
            libffhelper.GetFrameDataFromAVFrame.restype = MyAudioFrame
            libffhelper.GetFrameDataFromAVFrame.argtypes = [c_void_p, c_void_p]
            frame = libffhelper.GetFrameDataFromAVFrame(avctx, avframe)

            # TODO: use frame before free avframe
            
            
            for i in range(frame.len):
                data = frame.data[i]


            # NOTE: don't access frame after free avframe
            libavcodec.av_frame_free(byref(avframe))
        
        libavformat.av_packet_free(byref(pkt))
    
    libavcodec.avcodec_free_context(byref(avctx))
    libavformat.avformat_free_context(ic)