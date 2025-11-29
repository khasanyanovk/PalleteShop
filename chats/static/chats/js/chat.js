document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('chatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    const urlParams = new URLSearchParams(window.location.search);
    const prefillMessage = urlParams.get('message');

    const textarea = document.querySelector('textarea');
    if (textarea) {
        if (prefillMessage) {
            textarea.value = decodeURIComponent(prefillMessage);
            textarea.style.height = 'auto';
            textarea.style.height = Math.min(textarea.scrollHeight, 120) + 'px';
            window.history.replaceState({}, document.title, window.location.pathname);
        }
        
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
        
        textarea.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                const form = document.getElementById('chatForm');
                if (form) {
                    form.submit();
                }
            }
        });
    }
});

setInterval(function() {
    const lastMessage = document.querySelector('.message:last-child');
    const chatId = document.querySelector('[data-chat-id]');
    
    if (lastMessage && chatId) {

    }
}, 10000);
