#include "poker_messaging.h"

int main() {
    // Verify that the version of the library that we linked against is
    // compatible with the version of the headers we compiled against.
    GOOGLE_PROTOBUF_VERIFY_VERSION;

    // generate a stream of events
    poker_bot::Event message;
    message.set_type(poker_bot::Event::JOIN);
    message.set_amount(301);
    message.set_message("this is a really long message hopefully longer than 255 bytes");
    if (!send_message<poker_bot::Event>(cout, message)) {
      cerr << "Failed to write message" << endl;
      return -1;
    }
    
    message.set_type(poker_bot::Event::NEW_ROUND);
    message.set_amount(402);
    message.set_message("");
    if (!send_message<poker_bot::Event>(cout, message)) {
      cerr << "Failed to write message" << endl;
      return -1;
    }
    
    send_terminator(cout);

    return 0;
}