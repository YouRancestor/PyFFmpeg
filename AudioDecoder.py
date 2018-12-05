from ffmpeg import *

from ffhelper import *

class AudioFrame(MyAudioFrame):
    def __init__(self, avframe: c_void_p):
        self.__src_avframe = c_void_p()
        self.__src_avframe.value = avframe.value
    def __del__(self):
        av_frame_free(byref(self.__src_avframe))

class AudioDecoder():
    def __init__(self, audio_path:bytes):
        self.__audio_path = audio_path

        av_register_all()

        self.__ic = c_void_p(None)

        file_name = c_char_p(self.__audio_path)
        avformat_open_input(byref(self.__ic), file_name, None, None)

        self.__avctx = c_void_p()
        self.__avctx.value = avcodec_alloc_context3(None)

        codec_params = c_void_p(None)
        codec_params.value = get_cedec_param_from_format_context(self.__ic)
        avcodec_parameters_to_context(self.__avctx, codec_params)
        codec_id = c_int(0)
        codec_id.value = get_codec_id_from_codec_context(self.__avctx)
        codec = c_void_p(None)
        codec.value = avcodec_find_decoder(codec_id)

        ret = avcodec_open2(self.__avctx, codec, None)
        assert(ret == 0)

    def get_frame(self):
        pkt = c_void_p(None)
        pkt.value = av_packet_alloc()
        if(av_read_frame(self.__ic, pkt) < 0):
            av_packet_free(byref(pkt))
            raise IOError("Read error, may reach end of file.")
        ret = avcodec_send_packet(self.__avctx, pkt)
        av_packet_free(byref(pkt))
        if(ret < 0 ):
            av_packet_free(byref(pkt))
            raise IOError("Decoder don't accept the packet.\navcodec_send_packet returned: %d"%ret)

        avframe = c_void_p(None)
        avframe.value = av_frame_alloc()
        ret = avcodec_receive_frame(self.__avctx, avframe)
        if (ret == EAGAIN or ret == AVERROR_EOF):
            av_frame_free(byref(avframe))
            return None
        
        frame = AudioFrame(avframe)
        frame1 = get_frame_data_from_avframe(self.__avctx, avframe)
        
        # FIXME
        frame.data          = frame1.data
        frame.len           = frame1.len
        frame.sample_rate   = frame1.sample_rate
        frame.samples       = frame1.samples
        frame.format        = frame1.format

        av_packet_free(byref(pkt))
        return frame

    def __del__(self):
        avcodec_free_context(byref(self.__avctx))
        avformat_free_context(self.__ic)


if __name__ == '__main__':
    capture = AudioDecoder(b"/home/bmi/Desktop/00001.m4a")
    count = 0
    while(True):
        try:
            frame = capture.get_frame()
        except Exception as e:
            print(e)
            break
        if(not frame):
            continue
        else:
            data = []
            # read frame data
            for i in range(frame.len):
                data.append(frame.data[i])
            count += 1
    print(count)