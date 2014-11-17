PROGRAMS := foldbot
ROOT := ../../../..
PROTOCOL_ROOT := $(ROOT)/protocol/cpp

all: $(PROGRAMS)

foldbot:
	g++ main.cpp $(PROTOCOL_ROOT)/protocol/poker_bot.pb.cc  -I/opt/local/include -I$(PROTOCOL_ROOT) -I$(PROTOCOL_ROOT)/include -lprotobuf -o foldbot

clean:
	rm -f $(PROGRAMS) *.o
