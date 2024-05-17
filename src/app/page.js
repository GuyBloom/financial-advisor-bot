import React from 'react';
import MessagingSystem from './modules/Message';

import './style.css';

export default function RootLayout({ children }) {
    return (
        <div style={{fontFamily: 'Optimist, sans-serif'}}>
            <div className="banner">
                <img src="./images/enologo.png" alt="logo" />
            </div>

            <h1 align="center">Welcome to the ONE Chatbot!</h1>

            <MessagingSystem />

        </div>
    );
}
