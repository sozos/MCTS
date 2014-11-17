PROTOCOL_PATH := ../../../protocol/java/protocol
LIB_PATH := ../../../protocol/java/lib
MESSAGING_PATH := ../../../protocol/java/messaging
SOURCE_PATH := $(PROTOCOL_PATH):$(LIB_PATH):$(MESSAGING_PATH)

all: test_sender test_receiver

test_sender: TestSender.class
	jar cfm test_sender.jar TestSenderManifest.txt TestSender.class
	jar uf test_sender.jar -C $(PROTOCOL_PATH) .
	jar uf test_sender.jar -C $(LIB_PATH) .
	jar uf test_sender.jar -C $(MESSAGING_PATH) .

test_receiver: TestReceiver.class
	jar cfm test_receiver.jar TestReceiverManifest.txt TestReceiver.class
	jar uf test_receiver.jar -C $(PROTOCOL_PATH) .
	jar uf test_receiver.jar -C $(LIB_PATH) .
	jar uf test_receiver.jar -C $(MESSAGING_PATH) .
	
# %.jar: %.class
# 	jar cfm $< TestReceiverManifest.txt $@
# 	jar uf $< -C $(PROTOCOL_PATH) .
# 	jar uf $< -C $(LIB_PATH) .

%.class: %.java
	javac -sourcepath $(SOURCE_PATH) $<

clean:
	rm -f *.class *.jar
