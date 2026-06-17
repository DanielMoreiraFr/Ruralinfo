document.addEventListener('DOMContentLoaded', function () {
// saidas da zootecnia pq é onde começa toda rota
    const SAIDAS_ZOOTECNIA = [
        '07:00', '08:05', '09:10', '10:15', '11:00', '11:45',
        '12:30', '13:15', '14:00', '15:05', '16:10', '17:15',
        '18:20', '19:25'
    ];

    //Converte string "HH:MM" em minutos desde meia-noite
    function toMin(str) {
        if (!str || str === '—') return null;
        const partes = str.trim().split(':');
        return parseInt(partes[0]) * 60 + parseInt(partes[1]);
    }

    //Retorna horário atual em minutos
    function agora() {
        const d = new Date();
        return d.getHours() * 60 + d.getMinutes();
    }

    // Formata minutos em "HH:MM"
    function formatarHora(min) {
        const h = String(Math.floor(min / 60)).padStart(2, '0');
        const m = String(min % 60).padStart(2, '0');
        return h + ':' + m;
    }

    // Determina qual viagem está ativa ou é a próxima 
    function calcularViagemAtual() {
        const minAgora = agora();
        const minSaidas = SAIDAS_ZOOTECNIA.map(toMin);

        // Encontra a próxima saída
        for (let i = 0; i < minSaidas.length; i++) {
            if (minSaidas[i] > minAgora) {
                return {
                    indice: i,          // índice da coluna (0-based)
                    proxSaida: SAIDAS_ZOOTECNIA[i],
                    minRestantes: minSaidas[i] - minAgora,
                    passada: false,
                };
            }
        }

        // Após o último horário do dia
        return {
            indice: minSaidas.length - 1,
            proxSaida: null,
            minRestantes: null,
            passada: true,
        };
    }

    //  Atualiza o relógio no banner
    function atualizarRelogio() {
        const el = document.getElementById('live-hora');
        if (!el) return;
        const d = new Date();
        el.textContent = d.toLocaleTimeString('pt-BR', {
            hour: '2-digit', minute: '2-digit'
        });
    }

    // ── Atualiza o texto do banner ──
    function atualizarBanner(info) {
        const textoProxima = document.getElementById('live-proxima');
        const textoTempo   = document.getElementById('live-tempo');
        if (!textoProxima || !textoTempo) return;

        if (info.passada) {
            textoProxima.textContent = 'Sem mais saídas hoje';
            textoTempo.textContent   = 'O circular encerrou as operações';
        } else {
            textoProxima.textContent = 'Próxima saída de Zootecnia: ' + info.proxSaida;
            if (info.minRestantes <= 0) {
                textoTempo.textContent = 'Partindo agora';
            } else if (info.minRestantes === 1) {
                textoTempo.textContent = 'Em 1 minuto';
            } else {
                textoTempo.textContent = 'Em ' + info.minRestantes + ' minutos';
            }
        }
    }

    // Destaca a coluna ativa
    function destacarColuna(indiceViagem) {
        // Remove destaques anteriores
        document.querySelectorAll('.col-ativa').forEach(function (el) {
            el.classList.remove('col-ativa');
        });

        const colunaAlvo = indiceViagem + 1;

        document.querySelectorAll('.tabela-horarios tr').forEach(function (linha) {
            const celulas = linha.querySelectorAll('th, td');
            if (celulas[colunaAlvo]) {
                celulas[colunaAlvo].classList.add('col-ativa');
            }
        });
    }

    // Destaca o próximo horário em cada linha
    function destacarProximoPorLinha() {
        const minAgora = agora();

        // Remove destaques anteriores
        document.querySelectorAll('.proximo-ponto').forEach(function (el) {
            el.classList.remove('proximo-ponto');
        });
        document.querySelectorAll('.horario-passado').forEach(function (el) {
            el.classList.remove('horario-passado');
        });

        // Percorre cada linha de dados (pula o cabeçalho)
        document.querySelectorAll('.tabela-horarios tbody tr').forEach(function (linha) {
            const celulas = linha.querySelectorAll('td');
            if (celulas.length === 0) return;

            let encontrou = false;

            for (let i = 1; i < celulas.length; i++) {
                const texto = celulas[i].textContent.trim();
                const min   = toMin(texto);

                if (min === null) continue; // célula "—"

                if (!encontrou && min > minAgora) {
                    // Primeiro horário futuro desta linha
                    celulas[i].classList.add('proximo-ponto');
                    encontrou = true;
                } else if (min <= minAgora) {
                    // Horário já passou
                    celulas[i].classList.add('horario-passado');
                }
            }
        });
    }

    // ── Função principal de atualização ──
    function atualizar() {
        const info = calcularViagemAtual();
        atualizarRelogio();
        atualizarBanner(info);
        destacarColuna(info.indice);
        destacarProximoPorLinha();
    }

    // Roda imediatamente e depois a cada 30 segundos
    atualizar();
    setInterval(atualizar, 30000);
});