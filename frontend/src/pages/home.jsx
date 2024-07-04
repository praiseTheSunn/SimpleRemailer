import React, { useState } from 'react';
import serverRequestService from '../services/serverRequestService';

const Home = () => {
    const [email, setEmail] = useState('');
    const [subject, setSubject] = useState('');
    const [message, setMessage] = useState('');

    const [encryptionAlgorithm, setEncryptionAlgorithm] = useState('AES');
    const [mixPathAlgorithm, setMixPathAlgorithm] = useState('Algorithm 1');
    const [mixSendingStrategy, setMixSendingStrategy] = useState('Strategy 1');

    const [settingsVisible, setSettingsVisible] = useState(false);

    const handleSubmit = (e) => {
        e.preventDefault();
        alert(`Email: ${email}\nSubject: ${subject}\nMessage: ${message}\nEncryption: ${encryptionAlgorithm}\nMix Path: ${mixPathAlgorithm}\nMix Strategy: ${mixSendingStrategy}`);
        serverRequestService.sendToSendingServer(email, subject, message, encryptionAlgorithm, mixPathAlgorithm, mixSendingStrategy);
        // Here you can add the logic to send the email, e.g., using an API call
    };

    const toggleSettingsVisibility = () => {
        setSettingsVisible(!settingsVisible);
    };

    return (
        <div className="min-h-screen flex flex-col items-center justify-center bg-gray-100 p-4">
            <h1 className="text-4xl font-bold mb-8">Simple Remailer</h1>
            <div className="flex w-full max-w-4xl justify-center">
                <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md">
                    <h2 className="text-2xl font-semibold mb-6">Mailing Form</h2>
                    <form onSubmit={handleSubmit}>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Recipient email</label>
                            <input
                                type="email"
                                value={email}
                                onChange={(e) => setEmail(e.target.value)}
                                required
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Subject</label>
                            <input
                                type="text"
                                value={subject}
                                onChange={(e) => setSubject(e.target.value)}
                                required
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            />
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Message</label>
                            <textarea
                                value={message}
                                onChange={(e) => setMessage(e.target.value)}
                                required
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            />
                        </div>
                        <button type="submit" className="w-full bg-blue-500 text-white py-2 rounded-md hover:bg-blue-600 transition duration-300">Send</button>
                    </form>
                    <button onClick={toggleSettingsVisibility} className="w-full mt-4 bg-gray-500 text-white py-2 rounded-md hover:bg-gray-600 transition duration-300">
                        {settingsVisible ? 'Hide Settings' : 'Show Settings'}
                    </button>
                </div>
                {settingsVisible && (
                    <div className="bg-white p-8 rounded-lg shadow-md w-full max-w-md ml-8">
                        <h2 className="text-2xl font-semibold mb-6">Settings</h2>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Encryption Algorithm</label>
                            <select
                                value={encryptionAlgorithm}
                                onChange={(e) => setEncryptionAlgorithm(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="AES">AES</option>
                                <option value="RSA">RSA</option>
                                <option value="DES">DES</option>
                            </select>
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Mix Path Determinator Algorithm</label>
                            <select
                                value={mixPathAlgorithm}
                                onChange={(e) => setMixPathAlgorithm(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="Algorithm 1">Algorithm 1</option>
                                <option value="Algorithm 2">Algorithm 2</option>
                                <option value="Algorithm 3">Algorithm 3</option>
                            </select>
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Mix Sending Strategy</label>
                            <select
                                value={mixSendingStrategy}
                                onChange={(e) => setMixSendingStrategy(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="Strategy 1">Strategy 1</option>
                                <option value="Strategy 2">Strategy 2</option>
                                <option value="Strategy 3">Strategy 3</option>
                            </select>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Home;
