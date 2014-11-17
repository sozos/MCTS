#include "poker_messaging.h"

int main() {
  // Verify that the version of the library that we linked against is
  // compatible with the version of the headers we compiled against.
  GOOGLE_PROTOBUF_VERIFY_VERSION;
  
  // read a stream of events from stdin
  poker_bot::Event message;
  while (receive_message<poker_bot::Event>(cin, message)) {
      cerr << "type: " << message.type() << endl;
      cerr << "amount: " << message.amount() << endl;
  }
  
  return 0;
}