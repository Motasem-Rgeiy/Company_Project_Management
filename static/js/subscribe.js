const sub_email = document.getElementById('sub-email');
const sub_btn = document.getElementById('sub-btn');
const msg_btn = document.getElementById('msg-btn');
const msg_container = document.getElementById('msg-container');



sub_btn.addEventListener('click',async () =>{
        const originalBtnHTML = sub_btn.innerHTML;
        sub_btn.innerHTML = '<i class="fa-solid fa-spinner fa-spin"></i><span>Loading...</span>'; // Change text to Loading
        try {
            const response = await fetch('/en/newsletter/subscribe', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    user_email:sub_email .value,
                 
                })
            });
            
            sub_btn.innerHTML = originalBtnHTML;
            if(response.ok){
                const data = await response.json();
                console.log('Django Response:', data);
                
                msg_container.classList.remove('hidden');
                msg_container.classList.add('flex');
       
                
                // Keep button disabled after successful submit
            } else {
                // Re-enable if the request failed on the server
                console.log('Error')
              
            }
        } catch (error) {
            // Re-enable if there was a network error
         
            console.log(error)
        }
})


msg_btn.addEventListener('click', ()=>{
    msg_container.classList.remove('flex');
    msg_container.classList.add('hidden');
  
})


