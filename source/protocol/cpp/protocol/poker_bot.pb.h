// Generated by the protocol buffer compiler.  DO NOT EDIT!

#ifndef PROTOBUF_protocol_2fpoker_5fbot_2eproto__INCLUDED
#define PROTOBUF_protocol_2fpoker_5fbot_2eproto__INCLUDED

#include <string>

#include <google/protobuf/stubs/common.h>

#if GOOGLE_PROTOBUF_VERSION < 2000003
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please update
#error your headers.
#endif
#if 2000003 < GOOGLE_PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers.  Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/repeated_field.h>
#include <google/protobuf/extension_set.h>

namespace poker_bot {

// Internal implementation detail -- do not call these.
void  protobuf_BuildDesc_protocol_2fpoker_5fbot_2eproto();
void protobuf_BuildDesc_protocol_2fpoker_5fbot_2eproto_AssignGlobalDescriptors(
    ::google::protobuf::FileDescriptor* file);

class Action;
class Event;
class Event_Card;

enum Action_Type {
  Action_Type_FOLD = 0,
  Action_Type_CALL = 1,
  Action_Type_RAISE = 2,
  Action_Type_CHECK = 3
};
const ::google::protobuf::EnumDescriptor* Action_Type_descriptor();
bool Action_Type_IsValid(int value);
const Action_Type Action_Type_Type_MIN = Action_Type_FOLD;
const Action_Type Action_Type_Type_MAX = Action_Type_CHECK;

enum Event_Card_Suit {
  Event_Card_Suit_DIAMONDS = 0,
  Event_Card_Suit_SPADES = 1,
  Event_Card_Suit_HEARTS = 2,
  Event_Card_Suit_CLUBS = 3
};
const ::google::protobuf::EnumDescriptor* Event_Card_Suit_descriptor();
bool Event_Card_Suit_IsValid(int value);
const Event_Card_Suit Event_Card_Suit_Suit_MIN = Event_Card_Suit_DIAMONDS;
const Event_Card_Suit Event_Card_Suit_Suit_MAX = Event_Card_Suit_CLUBS;

enum Event_Type {
  Event_Type_JOIN = 0,
  Event_Type_NEW_ROUND = 1,
  Event_Type_BUTTON = 2,
  Event_Type_BIG_BLIND = 3,
  Event_Type_SMALL_BLIND = 4,
  Event_Type_DEAL = 5,
  Event_Type_FLOP = 6,
  Event_Type_TURN = 7,
  Event_Type_RIVER = 8,
  Event_Type_ACTION = 9,
  Event_Type_ADJUST_CREDITS = 10,
  Event_Type_WIN = 11,
  Event_Type_END_OF_ROUND = 12,
  Event_Type_QUIT = 13,
  Event_Type_BAD_BOT = 14,
  Event_Type_YOUR_TURN = 15
};
const ::google::protobuf::EnumDescriptor* Event_Type_descriptor();
bool Event_Type_IsValid(int value);
const Event_Type Event_Type_Type_MIN = Event_Type_JOIN;
const Event_Type Event_Type_Type_MAX = Event_Type_YOUR_TURN;

// ===================================================================

class Action : public ::google::protobuf::Message {
 public:
  Action();
  virtual ~Action();
  
  Action(const Action& from);
  
  inline Action& operator=(const Action& from) {
    CopyFrom(from);
    return *this;
  }
  
  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }
  
  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }
  
  static const ::google::protobuf::Descriptor* descriptor();
  static const Action& default_instance();
  void Swap(Action* other);
  
  // implements Message ----------------------------------------------
  
  Action* New() const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SetCachedSize(int size) const { _cached_size_ = size; }
  public:
  
  const ::google::protobuf::Descriptor* GetDescriptor() const;
  const ::google::protobuf::Reflection* GetReflection() const;
  
  // nested types ----------------------------------------------------
  
  typedef Action_Type Type;
  static const Type FOLD = Action_Type_FOLD;
  static const Type CALL = Action_Type_CALL;
  static const Type RAISE = Action_Type_RAISE;
  static const Type CHECK = Action_Type_CHECK;
  static inline const ::google::protobuf::EnumDescriptor*
  Type_descriptor() {
    return Action_Type_descriptor();
  }
  static inline bool Type_IsValid(int value) {
    return Action_Type_IsValid(value);
  }
  static const Type Type_MIN =
    Action_Type_Type_MIN;
  static const Type Type_MAX =
    Action_Type_Type_MAX;
  
  // accessors -------------------------------------------------------
  
  // required .poker_bot.Action.Type type = 1 [default = FOLD];
  inline bool has_type() const;
  inline void clear_type();
  inline ::poker_bot::Action_Type type() const;
  inline void set_type(::poker_bot::Action_Type value);
  
  // optional int32 amount = 2 [default = 0];
  inline bool has_amount() const;
  inline void clear_amount();
  inline ::google::protobuf::int32 amount() const;
  inline void set_amount(::google::protobuf::int32 value);
  
 private:
  ::google::protobuf::UnknownFieldSet _unknown_fields_;
  mutable int _cached_size_;
  
  int type_;
  ::google::protobuf::int32 amount_;
  friend void protobuf_BuildDesc_protocol_2fpoker_5fbot_2eproto_AssignGlobalDescriptors(
      const ::google::protobuf::FileDescriptor* file);
  ::google::protobuf::uint32 _has_bits_[(2 + 31) / 32];
  
  // WHY DOES & HAVE LOWER PRECEDENCE THAN != !?
  inline bool _has_bit(int index) const {
    return (_has_bits_[index / 32] & (1u << (index % 32))) != 0;
  }
  inline void _set_bit(int index) {
    _has_bits_[index / 32] |= (1u << (index % 32));
  }
  inline void _clear_bit(int index) {
    _has_bits_[index / 32] &= ~(1u << (index % 32));
  }
  
  void InitAsDefaultInstance();
  static Action* default_instance_;
};
// -------------------------------------------------------------------

class Event_Card : public ::google::protobuf::Message {
 public:
  Event_Card();
  virtual ~Event_Card();
  
  Event_Card(const Event_Card& from);
  
  inline Event_Card& operator=(const Event_Card& from) {
    CopyFrom(from);
    return *this;
  }
  
  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }
  
  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }
  
  static const ::google::protobuf::Descriptor* descriptor();
  static const Event_Card& default_instance();
  void Swap(Event_Card* other);
  
  // implements Message ----------------------------------------------
  
  Event_Card* New() const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SetCachedSize(int size) const { _cached_size_ = size; }
  public:
  
  const ::google::protobuf::Descriptor* GetDescriptor() const;
  const ::google::protobuf::Reflection* GetReflection() const;
  
  // nested types ----------------------------------------------------
  
  typedef Event_Card_Suit Suit;
  static const Suit DIAMONDS = Event_Card_Suit_DIAMONDS;
  static const Suit SPADES = Event_Card_Suit_SPADES;
  static const Suit HEARTS = Event_Card_Suit_HEARTS;
  static const Suit CLUBS = Event_Card_Suit_CLUBS;
  static inline const ::google::protobuf::EnumDescriptor*
  Suit_descriptor() {
    return Event_Card_Suit_descriptor();
  }
  static inline bool Suit_IsValid(int value) {
    return Event_Card_Suit_IsValid(value);
  }
  static const Suit Suit_MIN =
    Event_Card_Suit_Suit_MIN;
  static const Suit Suit_MAX =
    Event_Card_Suit_Suit_MAX;
  
  // accessors -------------------------------------------------------
  
  // required int32 value = 1;
  inline bool has_value() const;
  inline void clear_value();
  inline ::google::protobuf::int32 value() const;
  inline void set_value(::google::protobuf::int32 value);
  
  // required .poker_bot.Event.Card.Suit suit = 2;
  inline bool has_suit() const;
  inline void clear_suit();
  inline ::poker_bot::Event_Card_Suit suit() const;
  inline void set_suit(::poker_bot::Event_Card_Suit value);
  
 private:
  ::google::protobuf::UnknownFieldSet _unknown_fields_;
  mutable int _cached_size_;
  
  ::google::protobuf::int32 value_;
  int suit_;
  friend void protobuf_BuildDesc_protocol_2fpoker_5fbot_2eproto_AssignGlobalDescriptors(
      const ::google::protobuf::FileDescriptor* file);
  ::google::protobuf::uint32 _has_bits_[(2 + 31) / 32];
  
  // WHY DOES & HAVE LOWER PRECEDENCE THAN != !?
  inline bool _has_bit(int index) const {
    return (_has_bits_[index / 32] & (1u << (index % 32))) != 0;
  }
  inline void _set_bit(int index) {
    _has_bits_[index / 32] |= (1u << (index % 32));
  }
  inline void _clear_bit(int index) {
    _has_bits_[index / 32] &= ~(1u << (index % 32));
  }
  
  void InitAsDefaultInstance();
  static Event_Card* default_instance_;
};
// -------------------------------------------------------------------

class Event : public ::google::protobuf::Message {
 public:
  Event();
  virtual ~Event();
  
  Event(const Event& from);
  
  inline Event& operator=(const Event& from) {
    CopyFrom(from);
    return *this;
  }
  
  inline const ::google::protobuf::UnknownFieldSet& unknown_fields() const {
    return _unknown_fields_;
  }
  
  inline ::google::protobuf::UnknownFieldSet* mutable_unknown_fields() {
    return &_unknown_fields_;
  }
  
  static const ::google::protobuf::Descriptor* descriptor();
  static const Event& default_instance();
  void Swap(Event* other);
  
  // implements Message ----------------------------------------------
  
  Event* New() const;
  int GetCachedSize() const { return _cached_size_; }
  private:
  void SetCachedSize(int size) const { _cached_size_ = size; }
  public:
  
  const ::google::protobuf::Descriptor* GetDescriptor() const;
  const ::google::protobuf::Reflection* GetReflection() const;
  
  // nested types ----------------------------------------------------
  
  typedef Event_Card Card;
  
  typedef Event_Type Type;
  static const Type JOIN = Event_Type_JOIN;
  static const Type NEW_ROUND = Event_Type_NEW_ROUND;
  static const Type BUTTON = Event_Type_BUTTON;
  static const Type BIG_BLIND = Event_Type_BIG_BLIND;
  static const Type SMALL_BLIND = Event_Type_SMALL_BLIND;
  static const Type DEAL = Event_Type_DEAL;
  static const Type FLOP = Event_Type_FLOP;
  static const Type TURN = Event_Type_TURN;
  static const Type RIVER = Event_Type_RIVER;
  static const Type ACTION = Event_Type_ACTION;
  static const Type ADJUST_CREDITS = Event_Type_ADJUST_CREDITS;
  static const Type WIN = Event_Type_WIN;
  static const Type END_OF_ROUND = Event_Type_END_OF_ROUND;
  static const Type QUIT = Event_Type_QUIT;
  static const Type BAD_BOT = Event_Type_BAD_BOT;
  static const Type YOUR_TURN = Event_Type_YOUR_TURN;
  static inline const ::google::protobuf::EnumDescriptor*
  Type_descriptor() {
    return Event_Type_descriptor();
  }
  static inline bool Type_IsValid(int value) {
    return Event_Type_IsValid(value);
  }
  static const Type Type_MIN =
    Event_Type_Type_MIN;
  static const Type Type_MAX =
    Event_Type_Type_MAX;
  
  // accessors -------------------------------------------------------
  
  // required .poker_bot.Event.Type type = 1;
  inline bool has_type() const;
  inline void clear_type();
  inline ::poker_bot::Event_Type type() const;
  inline void set_type(::poker_bot::Event_Type value);
  
  // optional uint32 player_id = 2;
  inline bool has_player_id() const;
  inline void clear_player_id();
  inline ::google::protobuf::uint32 player_id() const;
  inline void set_player_id(::google::protobuf::uint32 value);
  
  // optional uint32 credits = 3;
  inline bool has_credits() const;
  inline void clear_credits();
  inline ::google::protobuf::uint32 credits() const;
  inline void set_credits(::google::protobuf::uint32 value);
  
  // optional int32 amount = 4;
  inline bool has_amount() const;
  inline void clear_amount();
  inline ::google::protobuf::int32 amount() const;
  inline void set_amount(::google::protobuf::int32 value);
  
  // repeated .poker_bot.Event.Card cards = 5;
  inline int cards_size() const;
  inline void clear_cards();
  inline const ::google::protobuf::RepeatedPtrField< ::poker_bot::Event_Card >& cards() const;
  inline ::google::protobuf::RepeatedPtrField< ::poker_bot::Event_Card >* mutable_cards();
  inline const ::poker_bot::Event_Card& cards(int index) const;
  inline ::poker_bot::Event_Card* mutable_cards(int index);
  inline ::poker_bot::Event_Card* add_cards();
  
  // optional .poker_bot.Event.Card card = 6;
  inline bool has_card() const;
  inline void clear_card();
  inline const ::poker_bot::Event_Card& card() const;
  inline ::poker_bot::Event_Card* mutable_card();
  
  // optional .poker_bot.Action action = 7;
  inline bool has_action() const;
  inline void clear_action();
  inline const ::poker_bot::Action& action() const;
  inline ::poker_bot::Action* mutable_action();
  
  // optional uint32 rank = 8;
  inline bool has_rank() const;
  inline void clear_rank();
  inline ::google::protobuf::uint32 rank() const;
  inline void set_rank(::google::protobuf::uint32 value);
  
  // optional string message = 10;
  inline bool has_message() const;
  inline void clear_message();
  inline const ::std::string& message() const;
  inline void set_message(const ::std::string& value);
  inline void set_message(const char* value);
  inline ::std::string* mutable_message();
  
 private:
  ::google::protobuf::UnknownFieldSet _unknown_fields_;
  mutable int _cached_size_;
  
  int type_;
  ::google::protobuf::uint32 player_id_;
  ::google::protobuf::uint32 credits_;
  ::google::protobuf::int32 amount_;
  ::google::protobuf::RepeatedPtrField< ::poker_bot::Event_Card > cards_;
  ::poker_bot::Event_Card* card_;
  ::poker_bot::Action* action_;
  ::google::protobuf::uint32 rank_;
  ::std::string* message_;
  static const ::std::string _default_message_;
  friend void protobuf_BuildDesc_protocol_2fpoker_5fbot_2eproto_AssignGlobalDescriptors(
      const ::google::protobuf::FileDescriptor* file);
  ::google::protobuf::uint32 _has_bits_[(9 + 31) / 32];
  
  // WHY DOES & HAVE LOWER PRECEDENCE THAN != !?
  inline bool _has_bit(int index) const {
    return (_has_bits_[index / 32] & (1u << (index % 32))) != 0;
  }
  inline void _set_bit(int index) {
    _has_bits_[index / 32] |= (1u << (index % 32));
  }
  inline void _clear_bit(int index) {
    _has_bits_[index / 32] &= ~(1u << (index % 32));
  }
  
  void InitAsDefaultInstance();
  static Event* default_instance_;
};
// ===================================================================


// ===================================================================


// ===================================================================

// Action

// required .poker_bot.Action.Type type = 1 [default = FOLD];
inline bool Action::has_type() const {
  return _has_bit(0);
}
inline void Action::clear_type() {
  type_ = 0;
  _clear_bit(0);
}
inline ::poker_bot::Action_Type Action::type() const {
  return static_cast< ::poker_bot::Action_Type >(type_);
}
inline void Action::set_type(::poker_bot::Action_Type value) {
  GOOGLE_DCHECK(::poker_bot::Action_Type_IsValid(value));
  _set_bit(0);
  type_ = value;
}

// optional int32 amount = 2 [default = 0];
inline bool Action::has_amount() const {
  return _has_bit(1);
}
inline void Action::clear_amount() {
  amount_ = 0;
  _clear_bit(1);
}
inline ::google::protobuf::int32 Action::amount() const {
  return amount_;
}
inline void Action::set_amount(::google::protobuf::int32 value) {
  _set_bit(1);
  amount_ = value;
}

// -------------------------------------------------------------------

// Event_Card

// required int32 value = 1;
inline bool Event_Card::has_value() const {
  return _has_bit(0);
}
inline void Event_Card::clear_value() {
  value_ = 0;
  _clear_bit(0);
}
inline ::google::protobuf::int32 Event_Card::value() const {
  return value_;
}
inline void Event_Card::set_value(::google::protobuf::int32 value) {
  _set_bit(0);
  value_ = value;
}

// required .poker_bot.Event.Card.Suit suit = 2;
inline bool Event_Card::has_suit() const {
  return _has_bit(1);
}
inline void Event_Card::clear_suit() {
  suit_ = 0;
  _clear_bit(1);
}
inline ::poker_bot::Event_Card_Suit Event_Card::suit() const {
  return static_cast< ::poker_bot::Event_Card_Suit >(suit_);
}
inline void Event_Card::set_suit(::poker_bot::Event_Card_Suit value) {
  GOOGLE_DCHECK(::poker_bot::Event_Card_Suit_IsValid(value));
  _set_bit(1);
  suit_ = value;
}

// -------------------------------------------------------------------

// Event

// required .poker_bot.Event.Type type = 1;
inline bool Event::has_type() const {
  return _has_bit(0);
}
inline void Event::clear_type() {
  type_ = 0;
  _clear_bit(0);
}
inline ::poker_bot::Event_Type Event::type() const {
  return static_cast< ::poker_bot::Event_Type >(type_);
}
inline void Event::set_type(::poker_bot::Event_Type value) {
  GOOGLE_DCHECK(::poker_bot::Event_Type_IsValid(value));
  _set_bit(0);
  type_ = value;
}

// optional uint32 player_id = 2;
inline bool Event::has_player_id() const {
  return _has_bit(1);
}
inline void Event::clear_player_id() {
  player_id_ = 0u;
  _clear_bit(1);
}
inline ::google::protobuf::uint32 Event::player_id() const {
  return player_id_;
}
inline void Event::set_player_id(::google::protobuf::uint32 value) {
  _set_bit(1);
  player_id_ = value;
}

// optional uint32 credits = 3;
inline bool Event::has_credits() const {
  return _has_bit(2);
}
inline void Event::clear_credits() {
  credits_ = 0u;
  _clear_bit(2);
}
inline ::google::protobuf::uint32 Event::credits() const {
  return credits_;
}
inline void Event::set_credits(::google::protobuf::uint32 value) {
  _set_bit(2);
  credits_ = value;
}

// optional int32 amount = 4;
inline bool Event::has_amount() const {
  return _has_bit(3);
}
inline void Event::clear_amount() {
  amount_ = 0;
  _clear_bit(3);
}
inline ::google::protobuf::int32 Event::amount() const {
  return amount_;
}
inline void Event::set_amount(::google::protobuf::int32 value) {
  _set_bit(3);
  amount_ = value;
}

// repeated .poker_bot.Event.Card cards = 5;
inline int Event::cards_size() const {
  return cards_.size();
}
inline void Event::clear_cards() {
  cards_.Clear();
}
inline const ::google::protobuf::RepeatedPtrField< ::poker_bot::Event_Card >&
Event::cards() const {
  return cards_;
}
inline ::google::protobuf::RepeatedPtrField< ::poker_bot::Event_Card >*
Event::mutable_cards() {
  return &cards_;
}
inline const ::poker_bot::Event_Card& Event::cards(int index) const {
  return cards_.Get(index);
}
inline ::poker_bot::Event_Card* Event::mutable_cards(int index) {
  return cards_.Mutable(index);
}
inline ::poker_bot::Event_Card* Event::add_cards() {
  return cards_.Add();
}

// optional .poker_bot.Event.Card card = 6;
inline bool Event::has_card() const {
  return _has_bit(5);
}
inline void Event::clear_card() {
  if (card_ != NULL) card_->::poker_bot::Event_Card::Clear();
  _clear_bit(5);
}
inline const ::poker_bot::Event_Card& Event::card() const {
  return card_ != NULL ? *card_ : *default_instance_->card_;
}
inline ::poker_bot::Event_Card* Event::mutable_card() {
  _set_bit(5);
  if (card_ == NULL) card_ = new ::poker_bot::Event_Card;
  return card_;
}

// optional .poker_bot.Action action = 7;
inline bool Event::has_action() const {
  return _has_bit(6);
}
inline void Event::clear_action() {
  if (action_ != NULL) action_->::poker_bot::Action::Clear();
  _clear_bit(6);
}
inline const ::poker_bot::Action& Event::action() const {
  return action_ != NULL ? *action_ : *default_instance_->action_;
}
inline ::poker_bot::Action* Event::mutable_action() {
  _set_bit(6);
  if (action_ == NULL) action_ = new ::poker_bot::Action;
  return action_;
}

// optional uint32 rank = 8;
inline bool Event::has_rank() const {
  return _has_bit(7);
}
inline void Event::clear_rank() {
  rank_ = 0u;
  _clear_bit(7);
}
inline ::google::protobuf::uint32 Event::rank() const {
  return rank_;
}
inline void Event::set_rank(::google::protobuf::uint32 value) {
  _set_bit(7);
  rank_ = value;
}

// optional string message = 10;
inline bool Event::has_message() const {
  return _has_bit(8);
}
inline void Event::clear_message() {
  if (message_ != &_default_message_) {
    message_->clear();
  }
  _clear_bit(8);
}
inline const ::std::string& Event::message() const {
  return *message_;
}
inline void Event::set_message(const ::std::string& value) {
  _set_bit(8);
  if (message_ == &_default_message_) {
    message_ = new ::std::string;
  }
  message_->assign(value);
}
inline void Event::set_message(const char* value) {
  _set_bit(8);
  if (message_ == &_default_message_) {
    message_ = new ::std::string;
  }
  message_->assign(value);
}
inline ::std::string* Event::mutable_message() {
  _set_bit(8);
  if (message_ == &_default_message_) {
    message_ = new ::std::string;
  }
  return message_;
}


}  // namespace poker_bot
#endif  // PROTOBUF_protocol_2fpoker_5fbot_2eproto__INCLUDED