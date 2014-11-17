#include <iostream>
#include <fstream>
#include <string>
#include <cstdio>
#include <cmath>
#include <iomanip>
#include "protocol/poker_bot.pb.h"

using namespace std;

#define LENGTH_BYTES 4

void print_byte_array(const string& s)
{
    cerr << "byte array: ";
    for(size_t i = 0; i < s.length(); ++i)
    {
        cerr << "0x" << hex << int(static_cast<unsigned char>(s[i])) << dec << " ";
    }
    cerr << endl;
}

void print_byte_array(char *s, size_t bytes)
{
    cerr << "byte array: ";
    for(size_t i = 0; i < bytes; ++i)
    {
        cerr << "0x" << hex << int(static_cast<unsigned char>(s[i])) << dec << " ";
    }
    cerr << endl;
}

template <class MessageType>
bool receive_message(istream& in, MessageType& message)
{
    // get a message of the specified type from the input stream, return true
    // on success, false on failure
    
    // make sure the int has enough storage space
    assert(sizeof(int) >= 4);
    // get length in bytes of next message, in big-endian
    unsigned int bytes = 0;
    for (int i = LENGTH_BYTES-1; i >= 0; i--) {
        char byte;
        in.read(&byte, 1);
        if (in.bad() || in.eof()) {
            cerr << "[receive_message] unexpected end of stream while reading length" << endl;
            return false;
        }
        bytes |= byte << 8*i;
    }
#ifdef DEBUG
    cerr << "[receive_message] message length in bytes: " << bytes << endl;
#endif
    if (bytes == 0) {
        // expected end of stream
        return false;
    }
    try {
        char *encoded_message = new char[bytes];
        in.read(encoded_message, bytes);
        if (in.bad() || in.eof()) {
            cerr << "[receive_message] unexpected end of stream while reading message" << endl;
            return false;
        }
    #ifdef DEBUG
        cerr << "[receive_message] bytes of encoded message: ";
        print_byte_array(encoded_message, bytes);
    #endif
        if (!message.ParseFromArray(encoded_message, bytes)) {
            cerr << "[receive_message] failed to parse message" << endl;
            return false;
        }
    }
    catch (...) {
        cerr << "[receive_message] exception while receiving message"<< endl;
        return false;
    }
    return true;
}

template <class MessageType>
bool send_message(ostream& out, const MessageType& message)
{
    // write a message to the output stream
    string encoded_message;
    if (!message.SerializeToString(&encoded_message)) {
        return false;
    }
    // encode length
    unsigned int bytes = encoded_message.length();
#ifdef DEBUG
    cerr << "[send_message] message length in bytes: " << bytes << endl;
#endif
    for (int i = LENGTH_BYTES-1; i >= 0; i--) {
        char byte = (bytes >> 8*i) & 0xFF;
        out << byte;
    }
    // output length and message on the stream
    out << encoded_message << flush;
    return true;
}

bool send_terminator(ostream& out)
{
    // terminate a stream
    char c = '\0';
    for(size_t i = 0; i < LENGTH_BYTES; ++i)
    {
      out << c; 
    }
}
