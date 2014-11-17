/*

A command-line bot, this is run as a process by the dealer and given messages
on stdin, while printing messages on stdout. The messages are created using
Google Protocol Buffers.

This bot takes command-line arguments of the form "initial_credits:10000",
supplied when the process is spawned. After that, the bot waits for a
'YOUR_TURN' Event message, at which point it runs the 'turn' function, and
prints the Action message to stdout and waits for the next YOUR_TURN message.

See protocol/poker_bot.proto for the entire protocol specification. See the
wiki for more information.

The Python side of this application is 'foldbot.py'

*/

package foldbot;

import java.util.ArrayList;
import java.io.IOException;

import poker_bot.PokerBot.Event;
import poker_bot.PokerBot.Action;

import poker_messaging.PokerMessaging;

public class Main {
    public static int id;
    public static int credits;
    public static int small_blind_amount;
    public static int big_blind_amount;
    public static void main(String[] args) throws Exception {
        parse_commandline_options(args);

        System.err.println("id: " + id);
        System.err.println("credits: " + credits);
        System.err.println("small_blind_amount: " + small_blind_amount);
        System.err.println("big_blind_amount: " + big_blind_amount);
    
        // main bot loop
        main_loop();
    }

    public static void parse_commandline_options(String[] args) {
        for (int i = 0; i < args.length; i++)
        {
            String arg = args[i];
            int pos = arg.indexOf(':');
            if (pos == -1) {
                System.err.println("foldbot: unrecognized option '" + arg + "'");
                continue;
            }
            String key = arg.substring(0, pos);
            String value = arg.substring(pos+1);
            int v = Integer.parseInt(value);
            System.err.println("foldbot: got arg " + key + ":" + value);
            if (key.equals("id")) {
                id = v;
            }
            else if (key.equals("credits")) {
                credits = v;
            }
            else if (key.equals("small_blind_amount")) {
                small_blind_amount = v;
            }
            else if (key.equals("big_blind_amount")) {
                big_blind_amount = v;
            }
            else {
                System.err.println("foldbot: unrecognized key '" + key + "'");
            }
        }
    }

    public static Action turn() {
        Action.Builder action = Action.newBuilder();
        action.setType(Action.Type.FOLD);
        return action.build();
    }

    public static void main_loop() throws IOException {
        while (true)
        {
            ArrayList event_queue = new ArrayList();
            // read a stream of events from stdin
            System.err.println("foldbot: waiting for events");
            Event.Builder event_builder = Event.newBuilder();
            boolean result = false;
            while (result = PokerMessaging.receive_message(System.in, event_builder)) {
                Event event = event_builder.build();
                if (event.getType() == Event.Type.YOUR_TURN) {
                    break;
                }
                if (event.getType() == Event.Type.QUIT && event.getPlayerId() == id) {
                    System.err.println("foldbot: quit the game");
                    return;
                }
                event_queue.add(event);
            }
            if (!result) {
                // end of stream
                return;
            }
        
            System.err.println("foldbot: my turn");
            Action action = turn();
            PokerMessaging.send_message(System.out, action);
        }
    }
}