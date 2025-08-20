// API Configuration
const API_BASE_URL = 'https://maratona-zghv.onrender.com/api/inscricoes';


// Global variables
let currentInscricao = null;
let paymentCheckInterval = null;

// Simple scroll function for the main button
function scrollToInscricao(event) {
    if (event) event.preventDefault();
    
    console.log('🖱️ Botão clicado! Função scrollToInscricao chamada');
    
    const target = document.getElementById('inscricao');
    if (target) {
        console.log('✅ Seção encontrada, fazendo scroll');
        target.scrollIntoView({
            behavior: 'smooth',
            block: 'start'
        });
    } else {
        console.error('❌ Seção #inscricao não encontrada');
    }
}

// DOM Elements
const inscricaoForm = document.getElementById('inscricaoForm');
const categoriaSelect = document.getElementById('categoria');
const idadeInput = document.getElementById('idade');
const sexoSelect = document.getElementById('sexo');
const pagamentoModal = new bootstrap.Modal(document.getElementById('pagamentoModal'));
const loadingModal = new bootstrap.Modal(document.getElementById('loadingModal'));

// Initialize application
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 Maratona 2025 - Sistema carregado');
    
    // Test if inscricao section exists
    const inscricaoSection = document.getElementById('inscricao');
    if (inscricaoSection) {
        console.log('✅ Seção de inscrição encontrada');
    } else {
        console.error('❌ Seção de inscrição não encontrada');
    }
    
    // Test if button exists
    const inscrevaButton = document.querySelector('a[href="#inscricao"]');
    if (inscrevaButton) {
        console.log('✅ Botão "Inscreva-se" encontrado');
        // Add direct click handler as backup
        inscrevaButton.addEventListener('click', function(e) {
            console.log('🖱️ Botão "Inscreva-se" clicado');
        });
    } else {
        console.error('❌ Botão "Inscreva-se" não encontrado');
    }
    
    loadCategorias();
    setupFormValidation();
    setupEventListeners();
});

// Load categories from API
async function loadCategorias() {
    try {
        const response = await fetch(`${API_BASE_URL}/categorias/`);
        const data = await response.json();
        
        if (data.success) {
            populateCategorias(data.categorias);
        }
    } catch (error) {
        console.error('Erro ao carregar categorias:', error);
        // Fallback categories
        const fallbackCategorias = [
            { value: 'M_15_29', label: 'Masculino 15 a 29 anos' },
            { value: 'M_30_39', label: 'Masculino 30 a 39 anos' },
            { value: 'M_40_49', label: 'Masculino 40 a 49 anos' },
            { value: 'M_50_PLUS', label: 'Masculino acima de 50 anos' },
            { value: 'F_15_30', label: 'Mulheres 15 a 30 anos' },
            { value: 'F_32_PLUS', label: 'Mulheres acima de 32 anos' },
            { value: 'VISITANTES', label: 'Categoria Geral Visitantes' }
        ];
        populateCategorias(fallbackCategorias);
    }
}

// Populate category select
function populateCategorias(categorias) {
    categoriaSelect.innerHTML = '<option value="">Selecione sua categoria...</option>';
    categorias.forEach(categoria => {
        const option = document.createElement('option');
        option.value = categoria.value;
        option.textContent = categoria.label;
        categoriaSelect.appendChild(option);
    });
}

// Setup form validation and dynamic category filtering
function setupFormValidation() {
    // Update categories based on age and gender
    function updateCategorias() {
        const idade = parseInt(idadeInput.value);
        const sexo = sexoSelect.value;
        
        if (!idade || !sexo) return;
        
        // Clear current selection
        categoriaSelect.value = '';
        
        // Filter and highlight appropriate categories
        Array.from(categoriaSelect.options).forEach(option => {
            if (option.value === '') return;
            
            let isAppropriate = false;
            
            if (sexo === 'M') {
                if (idade >= 15 && idade <= 29 && option.value === 'M_15_29') isAppropriate = true;
                else if (idade >= 30 && idade <= 39 && option.value === 'M_30_39') isAppropriate = true;
                else if (idade >= 40 && idade <= 49 && option.value === 'M_40_49') isAppropriate = true;
                else if (idade >= 50 && option.value === 'M_50_PLUS') isAppropriate = true;
            } else if (sexo === 'F') {
                if (idade >= 15 && idade <= 30 && option.value === 'F_15_30') isAppropriate = true;
                else if (idade >= 32 && option.value === 'F_32_PLUS') isAppropriate = true;
            }
            
            if (option.value === 'VISITANTES') isAppropriate = true;
            
            // Style appropriate options
            if (isAppropriate) {
                option.style.backgroundColor = '#e3f2fd';
                option.style.fontWeight = 'bold';
            } else {
                option.style.backgroundColor = '';
                option.style.fontWeight = '';
            }
        });
    }
    
    idadeInput.addEventListener('input', updateCategorias);
    sexoSelect.addEventListener('change', updateCategorias);
}

// Setup event listeners
function setupEventListeners() {
    inscricaoForm.addEventListener('submit', handleFormSubmit);
    
    // Smooth scrolling for navigation - more robust version
    document.addEventListener('click', function(e) {
        // Check if clicked element is an anchor with hash
        if (e.target.tagName === 'A' && e.target.getAttribute('href') && e.target.getAttribute('href').startsWith('#')) {
            e.preventDefault();
            const targetId = e.target.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                // Scroll to target with offset for better positioning
                const offsetTop = target.offsetTop - 80; // 80px offset for better visibility
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }
        
        // Also handle clicks on child elements (like icons inside buttons)
        if (e.target.closest('a[href^="#"]')) {
            e.preventDefault();
            const anchor = e.target.closest('a[href^="#"]');
            const targetId = anchor.getAttribute('href');
            const target = document.querySelector(targetId);
            
            if (target) {
                const offsetTop = target.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
        }
    });
}

// Handle form submission
async function handleFormSubmit(e) {
    e.preventDefault();
    
    if (!validateForm()) return;
    
    const formData = new FormData(inscricaoForm);
    const inscricaoData = Object.fromEntries(formData.entries());
    
    // Convert idade to integer
    inscricaoData.idade = parseInt(inscricaoData.idade);
    
    try {
        showLoading(true);
        
        // Create registration
        const response = await fetch(`${API_BASE_URL}/criar/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(inscricaoData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            currentInscricao = data.inscricao;
            showLoading(false);
            processarPagamento(currentInscricao.id);
        } else {
            showLoading(false);
            showAlert('danger', 'Erro na inscrição: ' + formatErrors(data.errors));
        }
    } catch (error) {
        showLoading(false);
        showAlert('danger', 'Erro ao processar inscrição. Tente novamente.');
        console.error('Erro:', error);
    }
}

// Validate form
function validateForm() {
    const requiredFields = ['nome', 'idade', 'email', 'sexo', 'cidade', 'categoria'];
    let isValid = true;
    
    requiredFields.forEach(fieldName => {
        const field = document.getElementById(fieldName);
        if (!field.value.trim()) {
            field.classList.add('is-invalid');
            isValid = false;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    // Check terms acceptance
    const termos = document.getElementById('termos');
    if (!termos.checked) {
        showAlert('warning', 'Você deve concordar com os termos e condições.');
        isValid = false;
    }
    
    // Validate age
    const idade = parseInt(idadeInput.value);
    if (idade < 15 || idade > 100) {
        idadeInput.classList.add('is-invalid');
        showAlert('warning', 'A idade deve estar entre 15 e 100 anos.');
        isValid = false;
    }
    
    return isValid;
}

// Process payment
async function processarPagamento(inscricaoId) {
    try {
        showLoading(true);
        
        const response = await fetch(`${API_BASE_URL}/pagamento/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                inscricao_id: inscricaoId,
                valor: 1.00
            })
        });
        
        const data = await response.json();
        
        showLoading(false);
        
        if (data.success) {
            showPaymentModal(data);
            startPaymentCheck(data.payment_id);
        } else {
            showAlert('danger', 'Erro ao processar pagamento: ' + data.error);
        }
    } catch (error) {
        showLoading(false);
        showAlert('danger', 'Erro ao processar pagamento. Tente novamente.');
        console.error('Erro:', error);
    }
}

// Show payment modal
function showPaymentModal(paymentData) {
    const content = `
        <div class="payment-info">
            <div class="text-center mb-4">
                <h4 class="text-success">
                    <i class="fas fa-check-circle"></i> Inscrição Criada com Sucesso!
                </h4>
                <p class="mb-2">Número da inscrição: <strong>${currentInscricao.numero_inscricao}</strong></p>
                <p class="text-muted">Complete o pagamento para confirmar sua participação</p>
            </div>
            
            <div class="qr-code-container">
                <h5 class="mb-3">Escaneie o QR Code para pagar</h5>
                <img src="${paymentData.qr_code}" alt="QR Code PIX" class="img-fluid">
                <div class="payment-amount">R$ ${paymentData.valor.toFixed(2)}</div>
            </div>
            
            <div class="payment-instructions">
                <h6><i class="fas fa-mobile-alt"></i> Como pagar:</h6>
                <ol>
                    <li>Abra o app do seu banco</li>
                    <li>Escolha a opção PIX</li>
                    <li>Escaneie o QR Code acima</li>
                    <li>Confirme o pagamento de R$ ${paymentData.valor.toFixed(2)}</li>
                    <li>Aguarde a confirmação automática</li>
                </ol>
            </div>
            
            <div class="text-center">
                <div id="paymentStatus" class="status-badge status-pending">
                    <i class="fas fa-clock"></i> Aguardando Pagamento
                </div>
                <p class="mt-3 text-muted small">
                    O status será atualizado automaticamente após a confirmação do pagamento
                </p>
            </div>
        </div>
    `;
    
    document.getElementById('pagamentoContent').innerHTML = content;
    pagamentoModal.show();
}

// Start payment status checking
function startPaymentCheck(paymentId) {
    paymentCheckInterval = setInterval(async () => {
        try {
            const response = await fetch(`${API_BASE_URL}/pagamento/${paymentId}/verificar/`);
            const data = await response.json();
            
            if (data.success) {
                updatePaymentStatus(data.status);
                
                if (data.status === 'approved') {
                    clearInterval(paymentCheckInterval);
                    showPaymentSuccess();
                }
            }
        } catch (error) {
            console.error('Erro ao verificar pagamento:', error);
        }
    }, 5000); // Check every 5 seconds
}

// Update payment status
function updatePaymentStatus(status) {
    const statusElement = document.getElementById('paymentStatus');
    if (!statusElement) return;
    
    switch (status) {
        case 'approved':
            statusElement.className = 'status-badge status-paid';
            statusElement.innerHTML = '<i class="fas fa-check"></i> Pagamento Confirmado';
            break;
        case 'pending':
            statusElement.className = 'status-badge status-pending';
            statusElement.innerHTML = '<i class="fas fa-clock"></i> Aguardando Pagamento';
            break;
        case 'cancelled':
        case 'rejected':
            statusElement.className = 'status-badge status-cancelled';
            statusElement.innerHTML = '<i class="fas fa-times"></i> Pagamento Cancelado';
            break;
    }
}

// Show payment success
function showPaymentSuccess() {
    const content = `
        <div class="payment-info">
            <div class="text-center">
                <div class="mb-4">
                    <i class="fas fa-check-circle text-success" style="font-size: 4rem;"></i>
                </div>
                <h3 class="text-success mb-3">Pagamento Confirmado!</h3>
                <p class="lead mb-4">Sua inscrição foi confirmada com sucesso!</p>
                
                <div class="alert alert-success">
                    <h5><i class="fas fa-info-circle"></i> Informações da Inscrição</h5>
                    <p><strong>Número:</strong> ${currentInscricao.numero_inscricao}</p>
                    <p><strong>Nome:</strong> ${currentInscricao.nome}</p>
                    <p><strong>Categoria:</strong> ${getCategoriaLabel(currentInscricao.categoria)}</p>
                    <p class="mb-0"><strong>Status:</strong> <span class="status-badge status-paid">Pago</span></p>
                </div>
                
                <div class="mt-4">
                    <p class="text-muted">
                        <i class="fas fa-envelope"></i> 
                        Você receberá um e-mail de confirmação em breve.
                    </p>
                    <button type="button" class="btn btn-primary" data-bs-dismiss="modal">
                        <i class="fas fa-times"></i> Fechar
                    </button>
                </div>
            </div>
        </div>
    `;
    
    document.getElementById('pagamentoContent').innerHTML = content;
    
    // Reset form
    inscricaoForm.reset();
    currentInscricao = null;
}

// Get category label
function getCategoriaLabel(categoria) {
    const categorias = {
        'M_15_29': 'Masculino 15 a 29 anos',
        'M_30_39': 'Masculino 30 a 39 anos',
        'M_40_49': 'Masculino 40 a 49 anos',
        'M_50_PLUS': 'Masculino acima de 50 anos',
        'F_15_30': 'Mulheres 15 a 30 anos',
        'F_32_PLUS': 'Mulheres acima de 32 anos',
        'VISITANTES': 'Categoria Geral Visitantes'
    };
    return categorias[categoria] || categoria;
}

// Show loading modal
function showLoading(show) {
    const loadingModalElement = document.getElementById('loadingModal');
    if (show) {
        loadingModalElement.style.display = 'block';
        loadingModalElement.classList.add('show');
        loadingModalElement.setAttribute('aria-hidden', 'false');
        document.body.classList.add('modal-open');
    } else {
        loadingModalElement.style.display = 'none';
        loadingModalElement.classList.remove('show');
        loadingModalElement.setAttribute('aria-hidden', 'true');
        document.body.classList.remove('modal-open');
    }
}

// Show alert
function showAlert(type, message) {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert alert at the top of the registration section
    const inscricaoSection = document.getElementById('inscricao');
    inscricaoSection.insertBefore(alertDiv, inscricaoSection.firstChild);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Format validation errors
function formatErrors(errors) {
    if (typeof errors === 'string') return errors;
    
    let errorMessage = '';
    for (const field in errors) {
        errorMessage += `${field}: ${errors[field].join(', ')}\n`;
    }
    return errorMessage || 'Erro desconhecido';
}

// Clean up on page unload
window.addEventListener('beforeunload', function() {
    if (paymentCheckInterval) {
        clearInterval(paymentCheckInterval);
    }
});

// Add form animations
function addFormAnimations() {
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    });
    
    document.querySelectorAll('.category-card, .prize-card, .registration-form').forEach(el => {
        observer.observe(el);
    });
}

// Initialize animations when DOM is ready
document.addEventListener('DOMContentLoaded', addFormAnimations);
