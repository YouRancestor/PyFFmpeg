TEMPLATE = app
CONFIG += console c++11
CONFIG -= app_bundle
CONFIG -= qt

SOURCES += \
    main.c
DEFINES +=__need_timeval
LIBS += -lavformat -lavcodec -lavutil -lswresample -pthread -lcrystalhd -lz -ldl -lX11 -llzma -lva -lvdpau -lva-x11 -lva-drm
