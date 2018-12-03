#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/avutil.h>

struct MyAudioFrame{
    uint8_t* data;
    int size;
    int sample_rate;
    int samples;
    const char* fmt;
};

typedef struct MyAudioFrame MyAudioFrame;

static int get_format_from_sample_fmt(const char **fmt,
                                      enum AVSampleFormat sample_fmt)
{
    int i;
    struct sample_fmt_entry {
        enum AVSampleFormat sample_fmt; const char *fmt_be, *fmt_le;
    } sample_fmt_entries[] = {
    { AV_SAMPLE_FMT_U8,  "u8",    "u8"    },
    { AV_SAMPLE_FMT_S16, "s16be", "s16le" },
    { AV_SAMPLE_FMT_S32, "s32be", "s32le" },
    { AV_SAMPLE_FMT_FLT, "f32be", "f32le" },
    { AV_SAMPLE_FMT_DBL, "f64be", "f64le" },
};
    *fmt = NULL;
    for (i = 0; i < FF_ARRAY_ELEMS(sample_fmt_entries); i++) {
        struct sample_fmt_entry *entry = &sample_fmt_entries[i];
        if (sample_fmt == entry->sample_fmt) {
            *fmt = AV_NE(entry->fmt_be, entry->fmt_le);
            return 0;
        }
    }
    fprintf(stderr,
            "sample format %s is not supported as output format\n",
            av_get_sample_fmt_name(sample_fmt));
    return -1;
}

AVCodecParameters* GetCodecParamFromFormatContext(AVFormatContext* ic)
{
    return ic->streams[0]->codecpar;
}

enum AVCodecID GetCodecIdFromCodecContext(AVCodecContext* avctx)
{
    return avctx->codec_id;
}

MyAudioFrame GetFrameDataFromAVFrame(AVCodecContext* avctx, AVFrame* avframe)
{
    MyAudioFrame frame;
    frame.data = avframe->extended_data[0];
    frame.size = avframe->linesize[0] / 4;
    frame.sample_rate = avframe->sample_rate;
    frame.samples = avframe->nb_samples;
    get_format_from_sample_fmt(&frame.fmt,avctx->sample_fmt);
    return frame;
}

MyAudioFrame GetFrame(AVCodecContext* avctx)
{

}

int OpenDecoder(AVFormatContext *ic, AVCodecContext *avctx)
{
    avcodec_parameters_to_context(avctx, ic->streams[0]->codecpar);
    AVCodec *codec = avcodec_find_decoder(avctx->codec_id);

    int ret = avcodec_open2(avctx, codec, NULL);
    printf("%d", ret);
    return ret;
}

//MyAudioFrame test()
//{
//    MyAudioFrame frame;
//    frame.data = "Hello";
//    frame.size = 6;
//    frame.sample_rate = 16000;
//    return frame;
//}
