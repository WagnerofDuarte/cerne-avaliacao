// Asserções "proxy": consulta /check do addon. Variaveis: PROXY_CONTROL, QUERY (ex.: regra=contagem&fn=chat-insight-create&igual=1).
// `output.ok` alimenta `assertTrue`. `MARCA_MS` (opcional) = instante lido por /agora (ultima tecla do debounce).
var q = QUERY + (typeof MARCA_MS !== 'undefined' && MARCA_MS ? '&ultima_tecla_ms=' + MARCA_MS : '');
var r = http.get(PROXY_CONTROL + '/check?' + q);
var j = JSON.parse(r.body);
output.ok = j.ok === true;
output.detalhe = r.body;
