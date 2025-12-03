document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('adminChatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const active = document.activeElement;
            if (active && (active.tagName === 'TEXTAREA' || active.tagName === 'INPUT')) {
                return;
            }
            const backButton = document.querySelector('a.btn-outline-light');
            if (backButton) {
                backButton.click();
            }
        }
    });
    
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });

        textarea.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                const form = document.getElementById('adminChatForm');
                if (form) {
                    form.requestSubmit();
                }
            }
        });
    }

    const form = document.getElementById('adminChatForm');
    if (form) {
        form.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(form);
            const textarea = form.querySelector('textarea');
            const messageText = textarea.value.trim();
            
            if (!messageText) return;
            
            fetch(form.action || window.location.href, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-Requested-With': 'XMLHttpRequest'
                }
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const messagesContainer = document.getElementById('adminChatMessages');
                    const messageHtml = `
                        <div class="message admin-message" data-message-id="${data.message_id}">
                            <div class="message-bubble">
                                <div>${escapeHtml(messageText)}</div>
                                <div class="message-time">
                                    Вы • ${new Date().toLocaleTimeString('ru-RU', {hour: '2-digit', minute: '2-digit'})}, ${new Date().toLocaleDateString('ru-RU')}
                                </div>
                            </div>
                        </div>
                    `;
                    messagesContainer.insertAdjacentHTML('beforeend', messageHtml);
                    messagesContainer.scrollTop = messagesContainer.scrollHeight;

                    // Обновляем ID последнего сообщения для polling
                    window.lastPolledMessageId = data.message_id;

                    textarea.value = '';
                    textarea.style.height = 'auto';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                if (typeof showToast === 'function') {
                    showToast('Ошибка при отправке сообщения', 'error');
                }
            });
        });
    }
});

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/\n/g, '<br>');
}

function pollNewMessages() {
    const chatMessages = document.getElementById('adminChatMessages');
    if (!chatMessages) return;

    const pathParts = window.location.pathname.split('/');
    const chatIndex = pathParts.indexOf('chats');
    const chatId = pathParts[chatIndex + 1];
    
    if (!chatId) return;
    
    const lastMessage = chatMessages.querySelector('.message:last-child');
    let lastMessageId = null;
    
    if (lastMessage) {
        lastMessageId = lastMessage.dataset.messageId;
        
        if (!lastMessageId) {
            if (!window.lastPolledMessageId) {
                window.lastPolledMessageId = Date.now().toString();
            }
            lastMessageId = window.lastPolledMessageId;
        }
    }
    
    const url = `/chats/${chatId}/new-messages/?last_id=${lastMessageId || ''}`;
    
    fetch(url, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.text())
    .then(html => {
        if (html.trim()) {
            const tempDiv = document.createElement('div');
            tempDiv.innerHTML = html;
            
            const newMessages = tempDiv.querySelectorAll('.message');
            if (newMessages.length > 0) {
                const wasScrolledToBottom = chatMessages.scrollHeight - chatMessages.scrollTop <= chatMessages.clientHeight + 50;
                
                newMessages.forEach(message => {
                    const messageId = message.dataset.messageId;
                    if (messageId && !chatMessages.querySelector(`[data-message-id="${messageId}"]`)) {
                        chatMessages.appendChild(message);
                        
                        if (message.dataset.messageId) {
                            window.lastPolledMessageId = message.dataset.messageId;
                        }
                    }
                });
                
                if (wasScrolledToBottom) {
                    chatMessages.scrollTop = chatMessages.scrollHeight;
                }
            }
        }
    })
    .catch(error => {
        console.error('Error polling messages:', error);
    });
}

setInterval(pollNewMessages, 2000);
