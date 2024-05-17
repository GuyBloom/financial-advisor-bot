'use client';

import React, { useState } from 'react';

const MessagingSystem = () => {
    const [messages, setMessages] = useState([]);
    const [inputValue, setInputValue] = useState('');

    const createChatMessageElement = (message) => {
         if (message.sender != "ONE") {
            return( 
            <div className="message">
                <div className='message-sender'>{message.sender}</div>
                <div className="message-text">{message.text}</div>
            </div> 
            )
        } else {
            return(
                <div className='message blue-bg'>
                    <div className='message-sender'>ONE</div>
                    <div className='message-text'>{message.text}</div>
                </div> 
            )
        }
    }

    const sendMessage = async (e) => {
        e.preventDefault()

        const userMessage = {
            sender : 'User',
            text: inputValue,
        }

        // Update the state with the user's message first
        setMessages(prevMessages => [...prevMessages, userMessage]);

        setInputValue('')

        // Then make the API call and update the state with the bot's message
        const fetchAPIResponse = async (userMessage) => {
            const response = await fetch("http://127.0.0.1:5000/api/message",{
                method:'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body : JSON.stringify({question: userMessage.text})
            });
            const data = await response.json()
            return data;
        }

        const apiResponse = await fetchAPIResponse(userMessage)

        console.log(apiResponse)

        const botMessage = {
            sender: 'ONE',
            text : apiResponse
        }

        console.log(botMessage)

        setMessages(prevMessages => [...prevMessages, botMessage])
    }

    return (
        <div>
            <div className='chat-container'>
                <div className="chat-messages">
                    <div className='message blue-bg'>
                        <div className='message-sender'>ONE</div>
                        <div className='message-text'>Hello! I am Capital One's virtual assistant ONE, counterpart to eno. I am here to answer any financial questions or concerns you may have.</div>
                    </div>
                    {messages.map(message => createChatMessageElement(message))}
                </div>
            </div>
            <div className='input-parent'>
                <form className='chat-input-form' onSubmit={sendMessage}>
                    <input type='text' className='chat-input' required placeholder='Ask me a question...' value={inputValue} onChange={e => setInputValue(e.target.value)} />
                    <button type='submit' className='button send-button'>Send</button>
                </form>
            </div>
        </div>
    );
}

export default MessagingSystem;
