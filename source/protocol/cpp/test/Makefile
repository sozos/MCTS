PROGRAMS := test_receiver test_sender

all: $(PROGRAMS)

test_sender:
	g++ test_sender.cc ../poker_bot.pb.cc  -I/opt/local/include -I.. -lprotobuf -o test_sender

test_receiver:
	g++ test_receiver.cc ../poker_bot.pb.cc  -I/opt/local/include -I.. -lprotobuf -o test_receiver

clean:
	rm -f $(PROGRAMS)