// Admin chat functionality

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.getElementById('adminChatMessages');
    if (chatMessages) {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    const textarea = document.querySelector('textarea');
    if (textarea) {
        textarea.addEventListener('input', function() {
            this.style.height = 'auto';
            this.style.height = Math.min(this.scrollHeight, 120) + 'px';
        });
    }
});
