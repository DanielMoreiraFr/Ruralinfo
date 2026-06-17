document.addEventListener('DOMContentLoaded', function () { // só carrega o js quando o html todo carrega
    
    function atualizarInterfaceCircular() {
        fetch('/circular/api/ao-vivo/')
            .then(response => response.json())
            .then(data => { // setta "data" como o nome do dicionário que recebe os dados da API
                
                // Atualiza a parte do AO VIVO
                const relogioBanner = document.querySelector('.live-relogio');
                const infoPonto = document.querySelector('.live-proxima');
                const infoTempo = document.querySelector('.live-tempo');

                // esse if serve pra checar se o elemento realmente existe na tela, evitando erros 
                if (relogioBanner) relogioBanner.textContent = data.relogio_atual;

                // tira os destaques antigos
                document.querySelectorAll('.tabela-horarios th, .tabela-horarios td').forEach(celula => {
                    celula.classList.remove('col-ativa', 'proximo-ponto');
                });

                // coloca os novos destaques se o ônibus estiver rodando
                if (data.operando) {
                    if (infoPonto) infoPonto.textContent = `Próximo ponto: ${data.ponto} (${data.horario})`;
                    if (infoTempo) infoTempo.textContent = `Em ${data.minutos_restantes} min`;

                    const tabela = document.querySelector('.tabela-horarios');
                    if (tabela) {
                        
                        // destaca a célula exata da próxima parada
                        const linhaHTML = tabela.rows[data.linha_index + 1];
                        if (linhaHTML) {
                            const celulaHTML = linhaHTML.cells[data.coluna_index + 1];
                            if (celulaHTML) {
                                celulaHTML.classList.add('proximo-ponto');
                            }
                        }

                        // destaca a coluna inteira da viagem
                        for (let i = 0; i < tabela.rows.length; i++) {
                            const celulaColuna = tabela.rows[i].cells[data.coluna_index + 1];
                            if (celulaColuna) {
                                celulaColuna.classList.add('col-ativa');
                            }
                        }
                    }
                } else {
                    // Se o circular parou de rodar
                    if (infoPonto) infoPonto.textContent = 'Sem mais saídas hoje';
                    if (infoTempo) infoTempo.textContent = data.mensagem;
                }
            })
            .catch(error => console.error('Erro ao sincronizar dados:', error));
    }

    // O Temporizador
    atualizarInterfaceCircular();
    setInterval(atualizarInterfaceCircular, 30000);
});