/// M12 — complexidade ciclomatica (McCabe, 1976) por metodo, sobre a AST do package:analyzer.
///
/// Regra: complexidade = 1 + numero de `if`, `for`, `for-in`, `while`, `do`, `case` (cada
/// rotulo; `default` nao conta), `catch`, `&&`, `||`, `?:`, `??` e `if` de colecao.
/// Interpretacoes (registradas em docs/trilha-harness-notas.md):
///  - `for` de colecao (ForElement) NAO conta (nao esta na lista);
///  - cada braco de switch-expression NAO conta (nao e 'case' do enunciado);
///  - o corpo de closures conta para o metodo que as contem;
///  - so entram declaracoes com corpo (bloco ou `=>`): metodos, getters/setters, construtores com
///    corpo e funcoes de topo; metodos abstratos e construtores sem corpo ficam de fora.
library;

import 'dart:convert';
import 'dart:io';

import 'package:analyzer/dart/analysis/utilities.dart';
import 'package:analyzer/dart/ast/ast.dart';
import 'package:analyzer/dart/ast/token.dart';
import 'package:analyzer/dart/ast/visitor.dart';

class MethodResult {
  MethodResult(this.file, this.line, this.name, this.cc);
  final String file;
  final int line;
  final String name;
  final int cc;
  Map<String, Object> toJson() => {'arquivo': file, 'linha': line, 'metodo': name, 'cc': cc};
}

class _Counter extends RecursiveAstVisitor<void> {
  int count = 0;
  @override
  void visitIfStatement(IfStatement n) { count++; super.visitIfStatement(n); }
  @override
  void visitIfElement(IfElement n) { count++; super.visitIfElement(n); }
  @override
  void visitForStatement(ForStatement n) { count++; super.visitForStatement(n); }
  @override
  void visitWhileStatement(WhileStatement n) { count++; super.visitWhileStatement(n); }
  @override
  void visitDoStatement(DoStatement n) { count++; super.visitDoStatement(n); }
  @override
  void visitSwitchCase(SwitchCase n) { count++; super.visitSwitchCase(n); }
  @override
  void visitSwitchPatternCase(SwitchPatternCase n) { count++; super.visitSwitchPatternCase(n); }
  @override
  void visitCatchClause(CatchClause n) { count++; super.visitCatchClause(n); }
  @override
  void visitConditionalExpression(ConditionalExpression n) { count++; super.visitConditionalExpression(n); }
  @override
  void visitBinaryExpression(BinaryExpression n) {
    final t = n.operator.type;
    if (t == TokenType.AMPERSAND_AMPERSAND || t == TokenType.BAR_BAR || t == TokenType.QUESTION_QUESTION) count++;
    super.visitBinaryExpression(n);
  }
}

int complexityOf(AstNode body) {
  final c = _Counter();
  body.accept(c);
  return 1 + c.count;
}

class _Collector extends RecursiveAstVisitor<void> {
  _Collector(this.file, this.unit);
  final String file;
  final CompilationUnit unit;
  final List<MethodResult> out = [];
  String? _owner;

  int _line(AstNode n) => unit.lineInfo.getLocation(n.offset).lineNumber;

  void _add(String name, AstNode node, FunctionBody body) {
    if (body is EmptyFunctionBody) return;
    out.add(MethodResult(file, _line(node), _owner == null ? name : '$_owner.$name', complexityOf(body)));
  }

  void _inOwner(String name, void Function() f) {
    final prev = _owner;
    _owner = name;
    f();
    _owner = prev;
  }

  @override
  void visitClassDeclaration(ClassDeclaration n) => _inOwner(n.name.lexeme, () => super.visitClassDeclaration(n));
  @override
  void visitMixinDeclaration(MixinDeclaration n) => _inOwner(n.name.lexeme, () => super.visitMixinDeclaration(n));
  @override
  void visitEnumDeclaration(EnumDeclaration n) => _inOwner(n.name.lexeme, () => super.visitEnumDeclaration(n));
  @override
  void visitExtensionDeclaration(ExtensionDeclaration n) => _inOwner(n.name?.lexeme ?? '<ext>', () => super.visitExtensionDeclaration(n));

  @override
  void visitMethodDeclaration(MethodDeclaration n) {
    _add(n.name.lexeme, n, n.body);
    // nao desce: closures contam para o metodo; classes locais nao existem em Dart
  }

  @override
  void visitConstructorDeclaration(ConstructorDeclaration n) {
    final name = n.name == null ? (_owner ?? '<new>') : n.name!.lexeme;
    _add(n.name == null ? 'new' : name, n, n.body);
  }

  @override
  void visitFunctionDeclaration(FunctionDeclaration n) {
    if (n.parent is CompilationUnit) {
      _add(n.name.lexeme, n, n.functionExpression.body);
    }
  }
}

List<MethodResult> analyzeSource(String source, String file) {
  final r = parseString(content: source, throwIfDiagnostics: false);
  final c = _Collector(file, r.unit);
  r.unit.accept(c);
  return c.out;
}

List<MethodResult> analyzeDir(String root, {String sub = 'lib', bool onlyDomain = true}) {
  final base = Directory('$root/$sub');
  final res = <MethodResult>[];
  if (!base.existsSync()) return res;
  final files = base.listSync(recursive: true).whereType<File>().where((f) => f.path.endsWith('.dart')).toList()
    ..sort((a, b) => a.path.compareTo(b.path));
  for (final f in files) {
    final rel = f.path.substring(root.length + 1).replaceAll(r'\', '/');
    if (onlyDomain && !rel.contains('/domain/')) continue;
    res.addAll(analyzeSource(f.readAsStringSync(), rel));
  }
  return res;
}

Map<String, Object> summary(List<MethodResult> ms) {
  final n = ms.length;
  final sum = ms.fold<int>(0, (a, m) => a + m.cc);
  return {
    'M12_media': n == 0 ? 0 : double.parse((sum / n).toStringAsFixed(6)),
    'M12_acima': ms.where((m) => m.cc > 10).length,
    'metodos': n,
    'soma': sum,
    'detalhe': ms.map((m) => m.toJson()).toList(),
  };
}

String toJsonString(List<MethodResult> ms) => const JsonEncoder.withIndent('  ').convert(summary(ms));
