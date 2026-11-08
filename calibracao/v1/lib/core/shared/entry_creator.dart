/// Interface compartilhada: o chat cria entradas por aqui (forma permitida).
abstract class EntryCreator {
  Future<void> createFromText(String text);
}
