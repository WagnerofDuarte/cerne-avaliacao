class Message {
  const Message(this.author, this.text);

  final String author;
  final String text;

  bool get fromUser => author == 'user';
}
