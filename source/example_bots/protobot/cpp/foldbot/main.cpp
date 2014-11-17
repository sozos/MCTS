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

#include <cstdlib>
#include <iostream>
#include <sstream>
#include <vector>

#include "poker_messaging.h"

using namespace std;

int id;
int credits;
int small_blind_amount;
int big_blind_amount;

void parse_commandline_options(int argc, char *argv[])
{
     for(size_t i = 1; i < argc; ++i)
     {
         string arg = string(argv[i]);
         size_t pos = arg.find(":");
         if (pos == string::npos) {
             cerr << "foldbot: unrecognized arg '" << arg << "'" << endl;
             continue;
         }
         string key = arg.substr(0, pos);
         string value = arg.substr(pos+1);
         std::stringstream ss(value);
         int v;
         ss >> v;
         // check if the string conversion worked
         if (!ss) {
             cerr << "foldbot: could not convert '" << value << "' to int" << endl;
             continue;
         }
         if (key == "id")
         {
             id = v;
         }
         else if (key == "credits")
         {
             credits = v;
         }
         else if (key == "small_blind_amount")
         {
             small_blind_amount = v;
         }
         else if (key == "big_blind_amount")
         {
             big_blind_amount = v;
         }
         else
         {
             cerr << "foldbot: unrecognized key '" << key << "'" << endl;
         }
     }
}

poker_bot::Action turn()
{
    poker_bot::Action action;
    action.set_type(poker_bot::Action::FOLD);
    return action;
}

void main_loop()
{
    vector<poker_bot::Event> event_queue;
    while (1)
    {
        event_queue.clear();
        // read a stream of events from stdin
        cerr << "foldbot: waiting for events" << endl;
        poker_bot::Event event;
        bool result = false;
        while (result = receive_message<poker_bot::Event>(cin, event)) {
            if (event.type() == poker_bot::Event::YOUR_TURN) {
                break;
            }
            if (event.type() == poker_bot::Event::QUIT && event.player_id() == id) {
                cerr << "foldbot: quit the game" << endl;
                return;
            }
            event_queue.push_back(event);
        }
        if (!result) {
            // end of stream
            return;
        }
        
        cerr << "foldbot: my turn" << endl;
        poker_bot::Action action = turn();
        send_message<poker_bot::Action>(cout, action);
    }
}

int main(int argc, char *argv[])
{
    // Check if protocol buffer headers match library
    GOOGLE_PROTOBUF_VERIFY_VERSION;
    
    parse_commandline_options(argc, argv);

    cerr << "id: " << id << endl;
    cerr << "credits: " << credits << endl;
    cerr << "small_blind_amount: " << small_blind_amount << endl;
    cerr << "big_blind_amount: " << big_blind_amount << endl;
    
    // main bot loop
    main_loop();
    return EXIT_SUCCESS;
}
