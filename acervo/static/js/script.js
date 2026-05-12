document.addEventListener('DOMContentLoaded', () => {

    // LÓGICA DE ALTO CONTRASTE PERSISTENTE
    const btnContraste = document.getElementById('btn-contraste');
    const body = document.body;

    // Verifica no localStorage se o modo de alto contraste já estava ativo
    if (localStorage.getItem('altoContraste') === 'ativado') {
        body.classList.add('alto-contraste');
    }

    if (btnContraste) {
        btnContraste.addEventListener('click', () => {
            body.classList.toggle('alto-contraste');
            // Salva a preferência do usuário no localStorage
            if (body.classList.contains('alto-contraste')) {
                localStorage.setItem('altoContraste', 'ativado');
            } else {
                localStorage.setItem('altoContraste', 'desativado');
            }
        });
    }

    // LÓGICA DO DASHBOARD
    const ctxGeneros = document.getElementById('graficoGeneros');
    if (ctxGeneros) {
        Chart.register(ChartDataLabels);
        Chart.defaults.font.family = "'Inter', sans-serif";
        
        const getChartColors = () => {
            const isHighContrast = body.classList.contains('alto-contraste');
            return {
                corDestaque: getComputedStyle(document.documentElement).getPropertyValue('--brand-highlight').trim(),
                corNeutra: getComputedStyle(document.documentElement).getPropertyValue('--border-light').trim(),
                corTexto: getComputedStyle(document.documentElement).getPropertyValue('--text-muted').trim(),
                corTextoDestaque: isHighContrast ? '#000000' : '#FFFFFF',
            };
        };

        const colors = getChartColors();
        Chart.defaults.color = colors.corTexto;

        new Chart(ctxGeneros.getContext('2d'), { 
            type: 'bar', 
            data: { 
                labels: labelsGeneros, 
                datasets:[{ 
                    data: dadosGeneros, 
                    backgroundColor: labelsGeneros.map((_, i) => i === 0 ? colors.corDestaque : colors.corNeutra), 
                    borderRadius: 4, 
                    borderSkipped: false 
                }] 
            }, 
            options: { 
                indexAxis: 'y', 
                responsive: true, 
                maintainAspectRatio: false, 
                plugins: { 
                    legend: { display: false }, 
                    datalabels: { 
                        color: (context) => context.dataIndex === 0 ? colors.corTextoDestaque : colors.corTexto, 
                        anchor: 'end', 
                        align: 'start', 
                        offset: 10, 
                        font: { weight: 'bold' } 
                    } 
                }, 
                scales: { 
                    x: { display: false, beginAtZero: true }, 
                    y: { grid: { display: false }, border: { display: false } } 
                } 
            } 
        });

        const ctxEmprestimos = document.getElementById('graficoEmprestimos');
        new Chart(ctxEmprestimos.getContext('2d'), { 
            type: 'bar', 
            data: { 
                labels: labelsEmprestimos, 
                datasets:[{ 
                    data: dadosEmprestimos, 
                    backgroundColor: labelsEmprestimos.map((_, i) => i === 0 ? colors.corDestaque : colors.corNeutra), 
                    borderRadius: { topLeft: 6, topRight: 6 }, 
                    borderSkipped: false 
                }] 
            }, 
            options: { 
                responsive: true, 
                maintainAspectRatio: false, 
                plugins: { 
                    legend: { display: false }, 
                    datalabels: { 
                        color: (context) => context.dataIndex === 0 ? colors.corTextoDestaque : colors.corTexto, 
                        anchor: 'end', 
                        align: 'start', 
                        offset: -20, 
                        font: { weight: 'bold' } 
                    } 
                }, 
                scales: { 
                    x: { grid: { display: false }, border: { display: false } }, 
                    y: { display: false, beginAtZero: true } 
                } 
            } 
        });
    }

    // LEITOR DE CONTEÚDO ACESSÍVEL USANDO API NATIVA DO NAVEGADOR
    const btnLeitura = document.getElementById('btn-leitura');
    const btnPararLeitura = document.getElementById('btn-parar-leitura');
    const synth = window.speechSynthesis;
    let utterance;

    if (btnLeitura && btnPararLeitura && synth) {
        const AcoesLeitura = {
            iniciar: () => {
                const conteudo = document.getElementById('conteudo-principal').innerText;
                if (synth.speaking) {
                    synth.cancel();
                }
                if (conteudo) {
                    utterance = new SpeechSynthesisUtterance(conteudo);
                    utterance.lang = 'pt-BR';
                    utterance.onstart = () => {
                        btnLeitura.style.display = 'none';
                        btnPararLeitura.style.display = 'inline-block';
                    };
                    utterance.onend = () => {
                        btnLeitura.style.display = 'inline-block';
                        btnPararLeitura.style.display = 'none';
                    };
                    utterance.onerror = () => {
                        console.error('Ocorreu um erro na síntese de fala.');
                        AcoesLeitura.parar();
                    };
                    synth.speak(utterance);
                }
            },
            parar: () => {
                synth.cancel();
                btnLeitura.style.display = 'inline-block';
                btnPararLeitura.style.display = 'none';
            }
        };

        btnLeitura.addEventListener('click', AcoesLeitura.iniciar);
        btnPararLeitura.addEventListener('click', AcoesLeitura.parar);
    }
});