window.showToast = function(message) {
    const toast = document.getElementById('toast');
    const toastMessage = document.getElementById('toast-message');
    
    if (!toast || !toastMessage) {
        console.error('Toast DOM elements not found!');
        return;
    }
    
    toastMessage.textContent = message;
    toast.classList.remove('hidden');

    setTimeout(() => toast.classList.add('opacity-100'), 10);

    setTimeout(() => {
        toast.classList.remove('opacity-100');
        setTimeout(() => toast.classList.add('hidden'), 300);
    }, 3000);
};