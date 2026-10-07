const comment_btn = document.getElementById('comment-btn');
const comment_inp = document.getElementById('comment-inp');
const new_comment_container = document.getElementById('new-comment');



post_id = comment_inp.getAttribute('data-post-id');


comment_btn.addEventListener('click',async () =>{
       
        try {
            const response = await fetch('/en/blog/comment/save', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    post_id:post_id,
                    comment_body:comment_inp.value,
                 
                })
            });
            
         
            if(response.ok){
                const data = await response.json();
                console.log('Django Response:', data);
                const comment_body = document.createElement('p');
                
                comment_body.classList.add('animate-slide-in');
                comment_body.classList.add('bg-red-900');
                comment_body.textContent = data.message;
               
                
        
           
         
             
              
                new_comment_container.appendChild(comment_body);
                
                

                comment_inp.value = '';
                
          
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