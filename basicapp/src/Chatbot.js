import React from 'react';
import MessageInput from './MessageInput';
import Messages from './Messages'; // Import the Messages component

function Chatbot() {
  const [messages, setMessages] = React.useState([]);

  
  async function handleSendMessage(message) {
    const response = await fetch('http://localhost:11434/api/generate', {
        method: 'POST', // Use the POST method to send new messages
        headers: {
          'Content-Type': 'application/json' // Set the content type to JSON
        },
        body: JSON.stringify({ 
            model: 'mistral',
            prompt: message, 
            stream: false
         })
    });

    const data = await response.json(); // Parse the API response
    console.log('DEBUG:', data);

    if (data && data.response) { // If the API returns a 'message' property, display it as a response
        console.log('DEBUG:', "Received a response!");
        setMessages([...messages, { user: true, message: message }, { user: false, message: data.response }]);
    }
  }

  return (
    <div className="chatbot">
      <h1 className="chatbot-header">Chatbot</h1>
      <Messages messages={messages} />
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
}

export default Chatbot;