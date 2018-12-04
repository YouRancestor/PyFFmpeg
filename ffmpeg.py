from ctypes import *
from ctypes.util import find_library


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

# void av_register_all();
libavformat.av_register_all.argtypes = []
def av_register_all():
    libavformat.av_register_all()

# int avformat_open_input(AVFormatContext **ps, const char *url, AVInputFormat *fmt, AVDictionary **options);
libavformat.avformat_open_input.argtypes = [POINTER(c_void_p), c_char_p, c_void_p, POINTER(c_void_p)]
libavformat.avformat_open_input.restype = c_int
def avformat_open_input(pp_ic: POINTER(c_void_p), p_file_name: c_char_p, p_fmt: c_void_p, pp_options: POINTER(c_void_p)):
    libavformat.avformat_open_input(pp_ic, p_file_name, p_fmt, pp_options)


# AVCodecContext *avcodec_alloc_context3(const AVCodec *codec);
avcodec_alloc_context3 = libavcodec.avcodec_alloc_context3
avcodec_alloc_context3.argtypes = [c_void_p]
avcodec_alloc_context3.restype = c_void_p

# int avcodec_parameters_to_context(AVCodecContext *ctx,
#                                   const AVCodecParameters *par);
libavcodec.avcodec_parameters_to_context.argtypes = [c_void_p, c_void_p]
def avcodec_parameters_to_context(p_avctx: c_void_p, p_param: c_void_p):
    return libavcodec.avcodec_parameters_to_context(p_avctx, p_param)

# AVCodec *avcodec_find_decoder(enum AVCodecID id);
libavcodec.avcodec_find_decoder.argtypes = [c_int]
libavcodec.avcodec_find_decoder.restype = c_void_p
def avcodec_find_decoder(codec_id: c_int):
    return libavcodec.avcodec_find_decoder(codec_id)

# int avcodec_open2(AVCodecContext *avctx, const AVCodec *codec, AVDictionary **options);
libavcodec.avcodec_open2.argtypes = [c_void_p, c_void_p, POINTER(c_void_p)]
libavcodec.avcodec_open2.restype = c_int
def avcodec_open2(p_avctx: c_void_p, p_codec: c_void_p, pp_options: POINTER(c_void_p)):
    return libavcodec.avcodec_open2(p_avctx, p_codec, pp_options)

# AVPacket *av_packet_alloc(void);
libavcodec.av_packet_alloc.argtypes = []
libavcodec.av_packet_alloc.restype = c_void_p
def av_packet_alloc():
    return libavcodec.av_packet_alloc()

# void av_packet_free(AVPacket **pkt);
libavformat.av_packet_free.argtypes = [POINTER(c_void_p)]
def av_packet_free(pp_pkt: POINTER(c_void_p)):
    libavformat.av_packet_free(pp_pkt)

# int av_read_frame(AVFormatContext *s, AVPacket *pkt);
libavformat.av_read_frame.argtypes = [c_void_p, c_void_p]
def av_read_frame(p_ic: c_void_p, p_pkt: c_void_p):
    libavformat.av_read_frame(p_ic, p_pkt)

# int av_read_frame(AVFormatContext *s, AVPacket *pkt);
libavcodec.avcodec_send_packet.argtypes = [c_void_p, c_void_p]
libavcodec.avcodec_send_packet.restype = c_int
def avcodec_send_packet(p_avctx: c_void_p, p_pkt: c_void_p):
    return libavcodec.avcodec_send_packet(p_avctx, p_pkt)

# AVFrame *av_frame_alloc(void);
libavutil.av_frame_alloc.argtypes = []
libavutil.av_frame_alloc.restype = c_void_p
def av_frame_alloc():
    return libavutil.av_frame_alloc()

# void av_frame_free(AVFrame **frame);
libavutil.av_frame_free.argtypes = [POINTER(c_void_p)]
def av_frame_free(pp_pkt: POINTER(c_void_p)):
    libavutil.av_frame_free(pp_pkt)

# int avcodec_receive_frame(AVCodecContext *avctx, AVFrame *frame);
libavcodec.avcodec_receive_frame.argtypes = [c_void_p, c_void_p]
libavcodec.avcodec_receive_frame.restype = c_int
def avcodec_receive_frame(p_avctx: c_void_p, p_avframe: c_void_p):
    return libavcodec.avcodec_receive_frame(p_avctx, p_avframe)


# void avcodec_free_context(AVCodecContext **avctx);
libavcodec.avcodec_free_context.argtypes = [POINTER(c_void_p)]
def avcodec_free_context(pp_avctx: POINTER(c_void_p)):
    libavcodec.avcodec_free_context(pp_avctx)

# void avformat_free_context(AVFormatContext *s);
libavformat.avformat_free_context.argtypes = [c_void_p]
def avformat_free_context(p_ic: c_void_p):
    libavformat.avformat_free_context(p_ic)

EAGAIN = -11
AVERROR_EOF = -541478725

if __name__ == '__main__':
    # ver = Version()
    # print(ver)
    # # frame = MyAudioFrame()
    # libffhelper.test.restype = MyAudioFrame
    # frame = libffhelper.test()
    # print(frame.len)
    from ffhelper import MyAudioFrame

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

    codec_params = c_void_p()
    codec_params.value = libffhelper.GetCodecParamFromFormatContext(ic)
    print('AVCodecParameters: ', codec_params)
    libavcodec.avcodec_parameters_to_context(avctx, codec_params)
    codec_id = libffhelper.GetCodecIdFromCodecContext(avctx)
    print('Codec Id: ', codec_id)
    codec = c_void_p()
    libavcodec.avcodec_find_decoder.restype = c_void_p
    codec.value = libavcodec.avcodec_find_decoder(codec_id)
    print('codec found: 0x%x'%codec.value)
    print('codec contex: 0x%x'%avctx.value)
    ret = libavcodec.avcodec_open2(avctx, codec, None)
    print('avcodec_open2 returned: ', ret)


    assert(ret == 0)


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

            # frame = MyAudioFrame()
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