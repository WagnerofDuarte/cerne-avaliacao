import 'dart:io';

import 'package:args/args.dart';
import 'package:m12/m12.dart';

/// Uso: dart run bin/m12.dart --root <copia-temporaria-da-tag> [--sub lib] [--all]
/// Escreve JSON no stdout; nada e gravado no repositorio medido.
void main(List<String> args) {
  final p = ArgParser()
    ..addOption('root', mandatory: true, help: 'raiz do app (copia temporaria da tag)')
    ..addOption('sub', defaultsTo: 'lib')
    ..addFlag('all', negatable: false, help: 'nao restringir ao dominio (so para testes)');
  final r = p.parse(args);
  final ms = analyzeDir(r['root'] as String, sub: r['sub'] as String, onlyDomain: !(r['all'] as bool));
  stdout.writeln(toJsonString(ms));
}
