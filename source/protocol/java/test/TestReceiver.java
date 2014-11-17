import poker_bot.PokerBot.Event;
import poker_bot.PokerBot.Action;

import poker_messaging.PokerMessaging;

class TestReceiver {
  public static void main(String[] args) throws Exception {
    System.err.println("Start this receiver");
    
    while (true) {
        Event.Builder message_builder = Event.newBuilder();
        if (!PokerMessaging.receive_message(System.in, message_builder)) {
            // terminate
            break;
        }
        Event message = message_builder.build();
        System.err.println("event message: " + message.getMessage());
    }
  }
}