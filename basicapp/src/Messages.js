import React from 'react';

function Messages({ messages }) {
    return (
      <div className="messages">
        {messages.map((message, index) => (
          <div key={index} className={`message ${message.user ? 'user' : 'bot'}`}>
            {message.user ? message.message : `Bot: ${message.message}`}
          </div>
        ))}
      </div>
    );
  }

export default Messages;