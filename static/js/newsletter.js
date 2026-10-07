
 const input = document.getElementById('image');

  const container = document.getElementById('previewContainer');
  const err_msg = document.getElementById('err-msg');


  




//const titleInput = document.getElementById('titleImage');

//const bodyInput = document.getElementById('bodyInput');

//const imageInput = document.getElementById('imageInput');

//const mail_btn = document.getElementById('mail-btn');





// Capture DOM values and send via POST
const sendBtn = document.getElementById('sendBtn');

sendBtn.addEventListener('click', async () => {
  // 1. Create an empty FormData instance
  const formData = new FormData();

  // 2. Select DOM elements and append values
  const titleVal = document.getElementById('title').value;
  const bodyVal = document.getElementById('body').value;


  // The keys ('title', 'body', 'image') MUST match your Django form field names
  formData.append('title', titleVal);
  formData.append('body', bodyVal);

  

  // 3. Get Django CSRF token from the DOM


  // 4. Send fetch POST request
  try {
    const response = await fetch('/en/newsletter/send', {
      method: 'POST',
      body: formData,
    });

    const data = await response.json();

    if (response.ok) {
      showToast(data.message);

      setTimeout(() => {
                        location.reload();
                    }, 3300);
                   }     
    else {
      console.error('Validation or Server Errors:', data.errors);
      err_msg.classList.remove('hidden');
      err_msg.classList.add('block') ;
      console.log(data.message);
      err_msg.innerHTML = data.message;
      

   
    }
  } catch (error) {
    console.error('Network Error:', error);
  }
});