#include <libavformat/avformat.h>
#include <libavcodec/avcodec.h>
#include <libavutil/avutil.h>

#include <assert.h>
int main(int argc, char**argv)
{
    char* filename = argv[1];
    AVFormatContext* ic = NULL;
    av_register_all();
    int val = avformat_open_input(&ic, filename, NULL, NULL);
    assert(!val);

    AVCodecContext* avctx = avcodec_alloc_context3(NULL);
    avcodec_parameters_to_context(avctx, ic->streams[0]->codecpar);
    AVCodec *codec = avcodec_find_decoder(avctx->codec_id);
    avcodec_open2(avctx, codec, NULL);

    printf("%04x\n",AVERROR_EOF);
    printf("%d\n",AVERROR_EOF);
    while(1) {
        AVPacket* pkt = av_packet_alloc();
        if(av_read_frame(ic, pkt) < 0)
        {
            av_packet_free(&pkt);
            break;
        }

        int ret = avcodec_send_packet(avctx,pkt);
        if (ret < 0) {
            av_packet_free(&pkt);
            break;
        }

        while (ret>=0) {
            AVFrame* frame = av_frame_alloc();
            ret = avcodec_receive_frame(avctx, frame);
                    if (ret == AVERROR(EAGAIN) || ret == AVERROR_EOF)
            {
                av_frame_free(&frame);
                break;
            }
            static int count = 0;
            printf("%d\n", ++count);

            av_frame_free(&frame);
        }

        av_packet_free(&pkt);
    }

    avcodec_free_context(&avctx);
    avformat_free_context(ic);
}
