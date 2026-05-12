document.addEventListener('DOMContentLoaded', function() {
    const scannerContainer = document.getElementById('scanner-container');
    const statusMessage = document.getElementById('status-message');
    const feedbackDiv = document.getElementById('resultado-feedback');
    let isProcessing = false; // Variável para evitar múltiplas detecções ao mesmo tempo

    function startScanner() {
        if (navigator.mediaDevices && typeof navigator.mediaDevices.getUserMedia === 'function') {
            Quagga.init({
                inputStream: {
                    name: "Live",
                    type: "LiveStream",
                    target: scannerContainer,
                    constraints: {
                        width: { min: 640 },
                        height: { min: 480 },
                        aspectRatio: { min: 1, max: 2 },
                        facingMode: "environment" // Prioriza a câmera traseira
                    },
                },
                locator: {
                    patchSize: "medium",
                    halfSample: true
                },
                numOfWorkers: navigator.hardwareConcurrency || 4,
                decoder: {
                    readers: ["ean_reader", "ean_8_reader", "code_128_reader"]
                },
                locate: true
            }, function(err) {
                if (err) {
                    console.error("Erro ao iniciar o Quagga:", err);
                    statusMessage.textContent = "Erro ao iniciar a câmera. Verifique as permissões.";
                    return;
                }
                console.log("Scanner iniciado com sucesso.");
                Quagga.start();
            });
        } else {
            statusMessage.textContent = "Seu navegador não suporta acesso à câmera.";
        }
    }

    Quagga.onDetected(function(result) {
        if (isProcessing) {
            return; // Se já estiver processando um código, ignora os novos
        }

        isProcessing = true; // Bloqueia novas detecções
        const isbn = result.codeResult.code;
        statusMessage.textContent = `Código ${isbn} detectado. Verificando...`;
        scannerContainer.classList.add('success'); // Feedback visual de sucesso na leitura

        // Chama a nossa API do Django
        fetch(`/api/livro/consulta/${isbn}/`)
            .then(response => {
                if (!response.ok) {
                    // Se a resposta for 404 (Not Found) ou outro erro
                    return response.json().then(err => Promise.reject(err));
                }
                return response.json();
            })
            .then(data => {
                if (data.sucesso) {
                    feedbackDiv.innerHTML = `<div class="alert alert-success"><strong>Encontrado:</strong> ${data.titulo}</div>`;
                    // Para a câmera e redireciona após 2 segundos
                    Quagga.stop();
                    setTimeout(() => {
                        window.location.href = `/livro/${data.id}/`;
                    }, 2000);
                }
            })
            .catch(error => {
                // Se o livro não foi encontrado (erro 404 da API) ou outro erro de fetch
                console.warn(error.mensagem || "Livro não encontrado.");
                scannerContainer.classList.remove('success');
                scannerContainer.classList.add('error');
                feedbackDiv.innerHTML = `<div class="alert alert-danger">${error.mensagem || 'Livro não cadastrado.'}</div>`;
                
                // Reinicia para uma nova leitura após um curto período
                setTimeout(() => {
                    isProcessing = false; // Libera para nova detecção
                    scannerContainer.classList.remove('error');
                    statusMessage.textContent = "Aponte a câmera para o código de barras...";
                    feedbackDiv.innerHTML = "";
                }, 2500);
            });
    });

    // Inicia o scanner assim que a página carregar
    startScanner();
});