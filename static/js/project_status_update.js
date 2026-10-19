
document.addEventListener('DOMContentLoaded', () => {
    const confirmBtn = document.getElementById('confirm-btn');
    const statusSelect = document.getElementById('status');
    console.log(statusSelect)

    if (confirmBtn && statusSelect) {
        confirmBtn.addEventListener('click', async () => {
            const selectedStatus = statusSelect.value;
            const projectId = statusSelect.dataset.projectId;

            try {
                const response = await API.post(
                    `project/status/update/${projectId}`, 
                    JSON.stringify({
                        status: selectedStatus,
                    }),
                     {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                    
                       
                        
                    )
                ;

                const data = await response.json();

                if (response.ok) {
                     
              
                    // Display response message from Django
                    showToast(data.message);

                    if (data.update){
                    
                  
                   setTimeout(() => {
                        location.reload();
                    }, 3300);
                }
                   
                } else {
                    console.error('Failed to update status:', response.statusText);
                }
            } catch (error) {
                console.error('Error sending request:', error);
            }
        });
    }
});



// Helper function to extract Django CSRF token
function getCookie(name) {
    let value = `; ${document.cookie}`;
    let parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}