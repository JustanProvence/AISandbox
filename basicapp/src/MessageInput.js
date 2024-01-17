import React from 'react';

function MessageInput({ onSendMessage }) {
  const [message, setMessage] = React.useState('');

  function handleSubmit(event) {
    event.preventDefault();
    if (message) {
      onSendMessage(message);
      setMessage(''); // Clear the input field after sending a message
      console.log('DEBUG:', "submitted data");
    }
  }

  return (
    <form className="message-input-form" onSubmit={handleSubmit}>
      <input
        type="text"
        value={message}
        onChange={(event) => setMessage(event.target.value)}
      />
      <button type="submit">Send</button>
    </form>
  );
}

export default MessageInput;