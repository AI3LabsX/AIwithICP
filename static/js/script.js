function showButtons() {
    const filename = document.getElementById('filename').value;
    const language = document.getElementById('language').value;
    if(filename && language) {
        document.getElementById('generate-summary-link').style.display = 'block';
        document.getElementById('qa-link').style.display = 'block';
    } else {
        document.getElementById('generate-summary-link').style.display = 'none';
        document.getElementById('qa-link').style.display = 'none';
    }
}

function clearChat() {
    document.getElementById('chat-box').innerHTML = '';
}

document.getElementById('generate-summary-link').addEventListener('click', function(e) {
    const filename = document.getElementById('filename').value;
    const language = document.getElementById('language').value;
    if(!filename || !language) return alert('Please select a document and a language.');
    e.preventDefault(); // Prevent the default action of the anchor tag
    window.location.href = `/generate_summary_page?filename=${filename}&language=${language}`;
});

document.getElementById('qa-link').addEventListener('click', function(e) {
    const filename = document.getElementById('filename').value;
    const language = document.getElementById('language').value;
    if(!filename || !language) return alert('Please select a document and a language.');
    e.preventDefault(); // Prevent the default action of the anchor tag
    window.location.href = `/qa_page?filename=${filename}&language=${language}`;
});


function generateSummary(filename, language) {
    // Now filename and language are normal JavaScript variables with actual values
    document.querySelector('.loading-spinner').style.display = 'block';
    fetch('/generate_summary', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ filename: filename, language: language }),
        cache: 'no-cache'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.response;
        document.querySelector('.loading-spinner').style.display = 'none';
    })
    .catch(error => {
        console.error('Error during fetch operation: ', error);
        document.querySelector('.loading-spinner').style.display = 'none';
    });
}

function generateResponse(filename, language) {
    const query = document.getElementById('user-input').value;
    if (!query.trim()) return; // Prevent sending empty messages

    const chatBox = document.getElementById('chat-box');

    // Create and append user message
    const userMessage = document.createElement('p');
    userMessage.className = 'message user';
    userMessage.textContent = `User: ${query}`;
    chatBox.appendChild(userMessage); // Append user message to the chat box

    document.getElementById('user-input').value = ''; // Clear the input box
    document.querySelector('.loading-spinner').style.display = 'block'; // Show loading spinner

    fetch('/generate_response', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ query: query, filename: filename, language: language }),
        cache: 'no-cache'
    })
    .then(response => response.json())
    .then(data => {
        // Create and append bot message
        const botMessage = document.createElement('p');
        botMessage.className = 'message bot';
        botMessage.textContent = `Bot: ${data.response}`;
        chatBox.appendChild(botMessage); // Append bot message to the chat box

        document.querySelector('.loading-spinner').style.display = 'none'; // Hide loading spinner
        chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom of the chat box
    })
    .catch(error => {
        console.error('Error during fetch operation: ', error);
        document.querySelector('.loading-spinner').style.display = 'none'; // Hide loading spinner
    });
}



//document.getElementById('send-btn').addEventListener('click', function() {
//    const userInput = document.getElementById('user-input');
//    const chatBox = document.getElementById('chat-box');
//    if(userInput.value.trim() !== "") {
//        chatBox.innerHTML += `<div class="user-message">${userInput.value}</div>`;
//        userInput.value = ''; // Clear the input box
//    }
//});

function clearChat() {
    const chatBox = document.getElementById('chat-box');
    if(chatBox) {
        chatBox.innerHTML = '';
    }
}

function showButtons() {
    const filename = document.getElementById('filename').value;
    const language = document.getElementById('language').value;
    const project = document.getElementById('project').value;

    if(filename && language) {
        document.getElementById('generate-summary-link').style.display = 'block';
        document.getElementById('qa-link').style.display = 'block';
    } else {
        document.getElementById('generate-summary-link').style.display = 'none';
        document.getElementById('qa-link').style.display = 'none';
    }

    if(project && language) {
        document.getElementById('build-link').style.display = 'block';
    } else {
        document.getElementById('build-link').style.display = 'none';
    }
}

function showBuildButton() {
    showButtons(); // Call showButtons function to handle the display of build button
}

document.getElementById('build-link').addEventListener('click', function(e) {
    const project = document.getElementById('project').value;
    const language = document.getElementById('language').value;
    if(!project || !language) return alert('Please select a project and a language.');
    e.preventDefault(); // Prevent the default action of the anchor tag
    window.location.href = `/build_page?project=${project}&language=${language}`;
});

function icpBuild(project, language) {
    document.querySelector('.loading-spinner').style.display = 'block';
    fetch('/icp_build', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ project: project, language: language }),
        cache: 'no-cache'
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('response').innerText = data.response;
        document.querySelector('.loading-spinner').style.display = 'none';
    })
    .catch(error => {
        console.error('Error during fetch operation: ', error);
        document.querySelector('.loading-spinner').style.display = 'none';
    });
}
