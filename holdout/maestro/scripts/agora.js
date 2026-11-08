// Guarda em output.ms o instante (ms) do addon; usado no debounce (H06-2) logo depois da ultima tecla.
output.ms = JSON.parse(http.get(PROXY_CONTROL + '/agora').body).ms;
