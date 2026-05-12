document.addEventListener('DOMContentLoaded', () => {

    const formatarTextoEmLinhas = (texto, maxCharsPorLinha = 15) => {
        const palavras = texto.split(' ');
        let linhas = [], linhaAtual = '';
        palavras.forEach(palavra => {
            if ((linhaAtual + palavra).length > maxCharsPorLinha) {
                if (linhaAtual) linhas.push(linhaAtual.trim());
                linhaAtual = palavra + ' ';
            } else { linhaAtual += palavra + ' '; }
        });
        if (linhaAtual) linhas.push(linhaAtual.trim());
        if (linhas.length > 3) linhas = [linhas[0], linhas[1], linhas[2] + '...'];
        return linhas;
    };

    const btnContraste = document.getElementById('btn-contraste');
    const body = document.body;

    // Recupera o tema salvo ANTES de desenhar os gráficos
    if (localStorage.getItem('altoContraste') === 'ativado') {
        body.classList.add('alto-contraste');
    }

    // Função que força a cor dos textos do gráfico
    const atualizarCoresGraficos = () => {
        if (typeof Chart === 'undefined') return;
        const isHC = body.classList.contains('alto-contraste');
        const corTexto = isHC ? '#ffffff' : '#64748b'; 
        
        Chart.instances.forEach(chart => {
            if (chart.options.scales.x && chart.options.scales.x.ticks) {
                chart.options.scales.x.ticks.color = corTexto;
            }
            if (chart.options.scales.y && chart.options.scales.y.ticks) {
                chart.options.scales.y.ticks.color = corTexto;
            }
            if (chart.options.plugins.datalabels) {
                chart.options.plugins.datalabels.color = corTexto;
            }
            chart.update();
        });
    };

    // Evento de clique no botão
    if (btnContraste) {
        btnContraste.addEventListener('click', () => {
            body.classList.toggle('alto-contraste');
            localStorage.setItem('altoContraste', body.classList.contains('alto-contraste') ? 'ativado' : 'desativado');
            atualizarCoresGraficos(); 
        });
    }

    // DESENHO DOS GRÁFICOS DO DASHBOARD
    if (document.getElementById('graficoGeneros')) {
        Chart.register(ChartDataLabels);
        Chart.defaults.font.family = "'Inter', sans-serif";
        
        // Define a cor de início baseada no que está no Body AGORA
        const corTextoInicial = body.classList.contains('alto-contraste') ? '#ffffff' : '#64748b';

        new Chart(document.getElementById('graficoGeneros').getContext('2d'), { 
            type: 'bar', 
            data: { labels: labelsGeneros, datasets:[{ data: dadosGeneros, backgroundColor: '#f97316', borderRadius: 6, barThickness: 20 }] }, 
            options: { 
                indexAxis: 'y', responsive: true, maintainAspectRatio: false, layout: { padding: { right: 30 } },
                plugins: { legend: { display: false }, datalabels: { anchor: 'end', align: 'end', offset: 4, font: { weight: 'bold' }, color: corTextoInicial } }, 
                scales: { 
                    x: { display: false }, 
                    y: { border: { display: false }, grid: { display: false }, ticks: { color: corTextoInicial, font: { weight: 'bold' } } } 
                } 
            } 
        });

        new Chart(document.getElementById('graficoEmprestimos').getContext('2d'), { 
            type: 'bar', 
            data: { labels: labelsEmprestimos.map(label => formatarTextoEmLinhas(label, 20)), datasets:[{ data: dadosEmprestimos, backgroundColor: ['#0d6efd', '#3b82f6', '#60a5fa', '#93c5fd', '#bfdbfe'], borderRadius: 6, barThickness: 25 }] }, 
            options: { 
                indexAxis: 'y', responsive: true, maintainAspectRatio: false, layout: { padding: { right: 30 } },
                plugins: { legend: { display: false }, tooltip: { callbacks: { title: (ctx) => labelsEmprestimos[ctx[0].dataIndex] } }, datalabels: { anchor: 'end', align: 'end', offset: 4, font: { weight: 'bold' }, color: corTextoInicial } }, 
                scales: { 
                    x: { display: false }, 
                    y: { border: { display: false }, grid: { display: false }, ticks: { color: corTextoInicial, font: { weight: 'bold' } } } 
                } 
            } 
        });
    }

    // LEITOR DE TELA (ACESSIBILIDADE)
    const btnLeitura = document.getElementById('btn-leitura');
    const btnPararLeitura = document.getElementById('btn-parar-leitura');
    if (btnLeitura && btnPararLeitura && window.speechSynthesis) {
        btnLeitura.addEventListener('click', () => {
            const container = document.getElementById('conteudo-principal');
            if (!container) return;
            const texto = container.innerText;
            window.speechSynthesis.cancel();
            const utterance = new SpeechSynthesisUtterance(texto);
            utterance.lang = 'pt-BR';
            utterance.onstart = () => { btnLeitura.style.display = 'none'; btnPararLeitura.style.display = 'inline-block'; };
            utterance.onend = () => { btnLeitura.style.display = 'inline-block'; btnPararLeitura.style.display = 'none'; };
            window.speechSynthesis.speak(utterance);
        });
        btnPararLeitura.addEventListener('click', () => {
            window.speechSynthesis.cancel();
            btnLeitura.style.display = 'inline-block';
            btnPararLeitura.style.display = 'none';
        });
    }
});