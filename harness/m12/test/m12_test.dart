import 'package:m12/m12.dart';
import 'package:test/test.dart';

int cc(String body) => analyzeSource('class A { void m() { $body } }', 'a.dart').single.cc;

void main() {
  test('vazio = 1', () => expect(cc(''), 1));
  test('if / else if contam cada um', () => expect(cc('if (a) {} else if (b) {}'), 3));
  test('operadores logicos, ternario e ??', () => expect(cc('var x = a && b || c ? d ?? e : f;'), 5));
  test('lacos', () => expect(cc('for (;;) {} for (var i in l) {} while (a) {} do {} while (b);'), 5));
  test('catch conta, finally nao', () => expect(cc('try {} catch (e) {} on X {} finally {}'), 3));
  test('switch: cada case, default nao', () => expect(cc('switch (a) { case 1: break; case 2: break; default: break; }'), 3));
  test('if de colecao conta, for de colecao nao', () => expect(cc('var l = [for (var x in y) x, if (c) 1];'), 2));
  test('closure conta no metodo', () => expect(cc('f((x) => x > 0 && x < 9);'), 2));
  test('sem corpo fica de fora', () {
    final r = analyzeSource('abstract class A { void m(); A(); }', 'a.dart');
    expect(r, isEmpty);
  });
  test('getter e funcao de topo', () {
    final r = analyzeSource('int f(a) => a ? 1 : 2;\nclass B { int get g => 1; }', 'a.dart');
    expect(r.map((m) => '${m.name}:${m.cc}').toList(), ['f:2', 'B.g:1']);
  });
}
