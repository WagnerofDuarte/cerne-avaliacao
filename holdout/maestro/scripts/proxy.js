// Fala com a API de controle do addon do mitmproxy (holdout/proxy/cerne_holdout.py).
// Variaveis de ambiente do Maestro: PROXY_CONTROL (ex.: http://127.0.0.1:8099), ACAO (arm|disarm|reset), CENARIO.
var url = PROXY_CONTROL + '/' + ACAO + (typeof CENARIO !== 'undefined' && CENARIO ? '?cenario=' + CENARIO : '');
var r = http.get(url);
output.ok = JSON.parse(r.body).ok === true;
