package poker_messaging;

import java.io.InputStream;
import java.io.PrintStream;
import java.io.IOException;

import com.google.protobuf.Message;

import poker_bot.PokerBot.Event;
import poker_bot.PokerBot.Action;
      
public final class PokerMessaging {
    public static final int LENGTH_BYTES = 4;
    
    public static boolean read_bytes(InputStream in, byte[] byte_array) throws IOException {
        // read as many bytes as can be fit in the byte array
        // return true on success, false on failure
        
        for (int i = 0; i < byte_array.length; i++) {
            int read =  in.read(byte_array, i, 1);
            if (read == 0) {
                // EOF
                return false;
            }
        }
        return true;
    }
    
    public static boolean receive_message(InputStream in, Message.Builder message_builder) throws IOException {
        // get a message of the specified type from the input stream, return true
        // on success, false on failure
        
        message_builder.clear();
        byte[] length_byte_array = new byte[LENGTH_BYTES];
        if (!read_bytes(in, length_byte_array)) {
            throw new IOException("Unexpected end of stream while reading length");
        }
        int bytes = 0;
        for (int i = 0; i < LENGTH_BYTES; i++) {
            bytes <<= 8;
            bytes |= length_byte_array[i];
        }
        if (bytes == 0) {
            return false;
        }
        byte[] event_byte_array = new byte[bytes];
        if (!read_bytes(in, event_byte_array)) {
            throw new IOException("Unexpected end of stream while reading message");
        }
        message_builder.mergeFrom(event_byte_array);
        return true;
    }
    
    public static void send_message(PrintStream out, Message message) throws IOException {
        // write a message to the output stream
        byte[] event_byte_array = message.toByteArray();
        int bytes = event_byte_array.length;
        byte[] length_byte_array = new byte[LENGTH_BYTES];
        for (int i = 0; i < LENGTH_BYTES; i++) {
            length_byte_array[i] = (byte) ((bytes >> 8*(LENGTH_BYTES-1-i)) & 0xFF);
        }
        out.write(length_byte_array);
        out.write(event_byte_array);
    }
    
    public static void send_terminator(PrintStream out) throws IOException {
        // terminate a stream
        byte[] terminator = new byte[LENGTH_BYTES];
        out.write(terminator);
    }
}