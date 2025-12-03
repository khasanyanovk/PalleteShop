function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = window.CSRF_TOKEN || getCookie('csrftoken');

function updateBasketCount() {
    fetch('/basket/count/')
        .then(response => response.json())
        .then(data => {
            const badge = document.querySelector('.basket-count');
            if (badge) {
                badge.textContent = data.count;
                badge.style.display = data.count > 0 ? 'inline-block' : 'none';
            }

            const floatingBasket = document.querySelector('.floating-basket');
            const floatingBadge = document.querySelector('.floating-basket-count');
            
            if (floatingBasket) {
                if (data.count > 0) {
                    floatingBasket.style.display = 'flex';
                    floatingBasket.style.opacity = '1';
                    floatingBasket.style.transform = 'scale(1)';
                } else {
                    floatingBasket.style.opacity = '0';
                    floatingBasket.style.transform = 'scale(0.5)';
                    setTimeout(() => {
                        floatingBasket.style.display = 'none';
                    }, 300);
                }
            }
            
            if (floatingBadge) {
                floatingBadge.textContent = data.count;
                floatingBadge.style.display = data.count > 0 ? 'flex' : 'none';
            }
        })
        .catch(error => console.error('Error updating basket count:', error));
}

function addToBasket(productId, orderBtn) {
    fetch(`/basket/add/${productId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            orderBtn.classList.add('d-none');
            const quantitySelector = document.querySelector(`.quantity-selector[data-product-id="${productId}"]`);
            if (quantitySelector) {
                quantitySelector.classList.remove('d-none');
                quantitySelector.dataset.itemId = data.item_id;
                const quantityInput = quantitySelector.querySelector('.quantity-input');
                if (quantityInput) {
                    quantityInput.value = data.quantity;
                }
            }

            updateBasketCount();
        } else {
            if (typeof showToast === 'function') {
                showToast(data.error || 'Ошибка при добавлении товара', 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (typeof showToast === 'function') {
            showToast('Произошла ошибка при добавлении товара', 'error');
        }
    });
}

function updateQuantity(itemId, quantity, quantityElement) {
    fetch(`/basket/update/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ quantity: quantity })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            quantityElement.value = data.quantity;
            updateBasketCount();
        } else {
            if (typeof showToast === 'function') {
                showToast(data.error || 'Ошибка при обновлении количества', 'error');
            }
            fetch('/basket/count/')
                .then(r => r.json())
                .then(d => quantityElement.value = d.count);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function removeFromBasket(itemId, selector) {
    fetch(`/basket/remove/${itemId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            selector.classList.add('d-none');
            const productId = selector.dataset.productId;
            const orderBtn = document.querySelector(`.order-btn[data-product-id="${productId}"]`);
            if (orderBtn) {
                orderBtn.classList.remove('d-none');
            }
            
            updateBasketCount();
        } else {
            if (typeof showToast === 'function') {
                showToast(data.error || 'Ошибка при удалении товара', 'error');
            }
        }
    })
    .catch(error => {
        console.error('Error:', error);
        if (typeof showToast === 'function') {
            showToast('Произошла ошибка при удалении товара', 'error');
        }
    });
}

document.addEventListener('DOMContentLoaded', function() {
    updateBasketCount();
    document.addEventListener('click', function(e) {
        const clickableCard = e.target.closest('.clickable-card');
        if (clickableCard) {
            if (!e.target.closest('.order-btn') && 
                !e.target.closest('.quantity-selector') && 
                !e.target.closest('.carousel-control-prev') && 
                !e.target.closest('.carousel-control-next') &&
                !e.target.closest('a')) {
                const url = clickableCard.dataset.productUrl;
                if (url) {
                    window.location.href = url;
                }
            }
        }
    });
});

document.addEventListener('click', function(e) {
    const orderBtn = e.target.closest('.order-btn');
    if (orderBtn) {
        e.preventDefault();
        e.stopPropagation();
        const productId = orderBtn.dataset.productId;
        addToBasket(productId, orderBtn);
        return;
    }

    const increaseBtn = e.target.closest('.quantity-increase');
    if (increaseBtn) {
        e.preventDefault();
        e.stopPropagation();
        const selector = increaseBtn.closest('.quantity-selector');
        const itemId = selector.dataset.itemId;
        const quantityInput = selector.querySelector('.quantity-input');
        const newQuantity = parseInt(quantityInput.value) + 1;
        
        updateQuantity(itemId, newQuantity, quantityInput);
        return;
    }

    const decreaseBtn = e.target.closest('.quantity-decrease');
    if (decreaseBtn) {
        e.preventDefault();
        e.stopPropagation();
        const selector = decreaseBtn.closest('.quantity-selector');
        const itemId = selector.dataset.itemId;
        const quantityInput = selector.querySelector('.quantity-input');
        const currentQuantity = parseInt(quantityInput.value);
        
        if (currentQuantity > 1) {
            updateQuantity(itemId, currentQuantity - 1, quantityInput);
        } else {
            if (confirm('Удалить товар из корзины?')) {
                removeFromBasket(itemId, selector);
            }
        }
        return;
    }
});

document.addEventListener('change', function(e) {
    const quantityInput = e.target.closest('.quantity-input');
    if (quantityInput) {
        const selector = quantityInput.closest('.quantity-selector');
        const itemId = selector.dataset.itemId;
        let newQuantity = parseInt(quantityInput.value);

        if (isNaN(newQuantity) || newQuantity < 1) {
            newQuantity = 1;
            quantityInput.value = 1;
        }
        
        updateQuantity(itemId, newQuantity, quantityInput);
    }
});
