
function showToast(message, type = 'success') {
    const toastContainer = document.querySelector('.toast-container');
    const toastId = 'toast-' + Date.now();
    
    const iconMap = {
        'success': 'bi-check-circle-fill',
        'error': 'bi-exclamation-triangle-fill',
        'danger': 'bi-exclamation-triangle-fill',
        'warning': 'bi-exclamation-circle-fill'
    };
    
    const toastHtml = `
        <div id="${toastId}" class="toast align-items-center bg-${type}" role="alert" aria-live="assertive" aria-atomic="true" data-bs-autohide="true" data-bs-delay="3000">
            <div class="d-flex">
                <div class="toast-body">
                    <i class="bi ${iconMap[type] || iconMap.success} me-2"></i>
                    ${message}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>
    `;
    
    toastContainer.insertAdjacentHTML('beforeend', toastHtml);
    const toastElement = document.getElementById(toastId);
    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    toastElement.addEventListener('hidden.bs.toast', function() {
        toastElement.remove();
    });
}

document.addEventListener('DOMContentLoaded', function() {
    var toastElList = [].slice.call(document.querySelectorAll('.toast'));
    var toastList = toastElList.map(function(toastEl) {
        var toast = new bootstrap.Toast(toastEl);
        toast.show();
        return toast;
    });
});
