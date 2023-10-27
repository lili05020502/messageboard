function sendMessage() {
    const messageInput = document.getElementById("Inputmessage");
    const imageInput = document.getElementById("Inputimage");

    const message = messageInput.value;
    const image = imageInput.files[0];

    const formData = new FormData();
    formData.append("message", message);
    formData.append("image", image);

    fetch('/upload', {
        method: 'POST',
        body: formData
    })
        .then(response => response.json())
        .then(data => {
            
            console.log(data)
            getMessages()
        })
        .catch(error => {
            
            console.log(error)
        });
}

function getMessages() {
    fetch('/getmessages', {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json',
        },
    })
    .then(response => {
        if (!response.ok) {
            console.log(response)
            // throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        console.log("data:"+data);
        console.log(data.messages);
        displayMessages(data.messages);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function displayMessages(messages) {

    console.log(messages);
    const messageList = document.getElementById("Messages");
    messageList.innerHTML = ""; 

    messages.forEach(message => {
        const messageItem = document.createElement('div');
        
        const messageId = message[0]; 
        const messageText = message[1];
        const imageUrl = message[2]; 

        
        const messageTextElement = document.createElement('p');
        messageTextElement.textContent =messageText;

        
        const imageElement = document.createElement('img');
        imageElement.src = imageUrl;
        imageElement.alt = `Image for Message #${messageId}`;
        imageElement.classList.add('messageimg');

        messageItem.appendChild(messageTextElement);
        messageItem.appendChild(imageElement);
        const separator = document.createElement('hr');
        messageItem.appendChild(separator);

        messageList.appendChild(messageItem);
    });
}


getMessages();


