document.addEventListener('DOMContentLoaded', function () {
    const roomName = document.getElementById('chat').dataset.room;
    const chatInput = document.getElementById('chat-input');
    const chatForm = document.getElementById('chat-form');

    const socket = new WebSocket(`ws://${window.location.host}/ws/chat/${roomName}/`);

    socket.onopen = function (event) {
        console.log('WebSocket connection opened:', event);
    };

    socket.onmessage = function (event) {
        const message = JSON.parse(event.data);
        console.log('WebSocket message received:', message);

        // Handle incoming messages, e.g., append them to the chat window
        appendMessage(message.message);
    };

    socket.onclose = function (event) {
        console.log('WebSocket connection closed:', event);
    };

    // Add event listener for the form submission
    chatForm.addEventListener('submit', function (event) {
        event.preventDefault();
        const message = chatInput.value.trim();

        if (message !== '') {
            // Send the message to the server
            socket.send(JSON.stringify({
                'message': message
            }));

            // Optionally, append the message to the chat window immediately
            appendMessage(message);

            // Clear the input field
            chatInput.value = '';
        }
    });

    // Function to append a message to the chat window
    function appendMessage(message) {
        // Customize this function based on how you want to display messages in your chat window
        const chatWindow = document.getElementById('chat-window');
        const messageElement = document.createElement('div');
        messageElement.textContent = message;
        chatWindow.appendChild(messageElement);
    }
});
