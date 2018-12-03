TEMPLATE = lib
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    helper_functions.c

LIBS += -lavformat -lavcodec -lavutil -lswresample -pthread -lcrystalhd -lz -ldl -lX11 -llzma -lva -lvdpau -lva-x11 -lva-drm
