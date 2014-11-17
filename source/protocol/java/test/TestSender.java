import poker_bot.PokerBot.Event;
import poker_bot.PokerBot.Action;

import poker_messaging.PokerMessaging;

class TestSender {
  public static void main(String[] args) throws Exception {
    System.err.println("Start this sender");
    
    Event.Builder message_builder = Event.newBuilder();
    message_builder.setType(Event.Type.JOIN);
    message_builder.setMessage("message 1");
    PokerMessaging.send_message(System.out, message_builder.build());
    
    Event.Builder message_builder2 = Event.newBuilder();
    message_builder2.setType(Event.Type.QUIT);
    message_builder2.setMessage("message 2");
    PokerMessaging.send_message(System.out, message_builder2.build());
    
    PokerMessaging.send_terminator(System.out);
  }
}