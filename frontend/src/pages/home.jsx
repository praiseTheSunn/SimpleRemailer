import React, { useState } from 'react';
import serverRequestService from '../services/serverRequestService';

const Home = () => {
    const [email, setEmail] = useState('');
    const [subject, setSubject] = useState('');
    const [message, setMessage] = useState('');

    const [encryptionAlgorithm, setEncryptionAlgorithm] = useState('rsa_encryption');
    const [symmetricAlgorithm, setSymmetricAlgorithm] = useState('aes_encryption');
    const [mixPathAlgorithm, setMixPathAlgorithm] = useState('probabilistic');
    const [mixSendingStrategy, setMixSendingStrategy] = useState('timed');

    const [settingsVisible, setSettingsVisible] = useState(false);

    var url = "http://127.0.0.1:8001/";

    const handleSubmit = (e) => {
        e.preventDefault();
        // alert(`Email: ${email}\nSubject: ${subject}\nMessage: ${message}\nEncryption: ${encryptionAlgorithm}\nMix Path: ${mixPathAlgorithm}\nMix Strategy: ${mixSendingStrategy}`);
        updateAsymmetricAlgorithm(encryptionAlgorithm);
        // updateSymmetricAlgorithm(symmetricAlgorithm);
        updateMixPathAlgorithm(mixPathAlgorithm);
        updateMixSendingStrategy(mixSendingStrategy);
        serverRequestService.sendToSendingServer(url, email, subject, message, encryptionAlgorithm, mixPathAlgorithm, mixSendingStrategy);
        
        // Here you can add the logic to send the email, e.g., using an API call
    };

    const toggleSettingsVisibility = () => {
        setSettingsVisible(!settingsVisible);
    };

    const handleAsymmetricAlgorithmChange = (e) => {
        setEncryptionAlgorithm(e.target.value);
    };

    const updateAsymmetricAlgorithm = async (algorithm) => {
        try {
            const response = await fetch(`${url}updateAsymmetricAlgorithm?algorithm_name=${algorithm}`);
            const result = await response.json();
            if (response.ok) {
                console.log(result.message);
            } else {
                console.error(result.detail);
            }
        } catch (error) {
            console.error("Error updating algorithm:", error);
        }
    };

    const updateSymmetricAlgorithm = async (algorithm) => {
        try {
            const response = await fetch(`${url}updateSymmetricAlgorithm?algorithm_name=${algorithm}`);
            const result = await response.json();
            if (response.ok) {
                console.log(result.message);
            } else {
                console.error(result.detail);
            }
        } catch (error) {
            console.error("Error updating algorithm:", error);
        }
    }

    const updateMixPathAlgorithm = async (algorithm) => {
        try {
            const response = await fetch(`${url}updatePathStrategy?strategy_name=${algorithm}`);
            const result = await response.json();
            if (response.ok) {
                console.log(result.message);
            } else {
                console.error(result.detail);
            }
        } catch (error) {
            console.error("Error updating algorithm:", error);
        }
    }

    const updateMixSendingStrategy = async (strategy) => {
        try {
            const response = await fetch(`${url}updateSendStrategy?strategy_name=${strategy}`);
            const result = await response.json();
            if (response.ok) {
                console.log(result.message);
            } else {
                console.error(result.detail);
            }
        } catch (error) {
            console.error("Error updating strategy:", error);
        }
    }

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
                        <h2 className="text-2xl font-semibold mb-6">User Settings</h2>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Asymmetric Encryption Algorithm</label>
                            <select
                                value={encryptionAlgorithm}
                                onChange={handleAsymmetricAlgorithmChange}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="rsa_encryption">RSA</option>
                                <option value="ecc_encryption">ECC</option>
                                <option value="elgamal_encryption">Elgamal</option>
                            </select>
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Symmetric Encryption Algorithm</label>
                            <select
                                value={symmetricAlgorithm}
                                onChange={(e) => setSymmetricAlgorithm(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="aes_encryption">AES</option>
                                <option value="des_encryption">DES</option>
                                <option value="blowfish_encryption">Blowfish</option>
                            </select>
                        </div>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Mix Path Determinator Algorithm</label>
                            <select
                                value={mixPathAlgorithm}
                                onChange={(e) => setMixPathAlgorithm(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="probabilistic">Probabilistic Stategy</option>
                                <option value="non_probabilistic">Non-probabilistic Strategy</option>
                                {/* <option value="Algorithm 3">Algorithm 3</option> */}
                            </select>
                        </div>
                        <h2 className="text-2xl font-semibold mb-6">Admin Settings</h2>
                        <div className="mb-4">
                            <label className="block text-gray-700 mb-2">Mix Sending Strategy</label>
                            <select
                                value={mixSendingStrategy}
                                onChange={(e) => setMixSendingStrategy(e.target.value)}
                                className="w-full px-3 py-2 border border-gray-300 rounded-md"
                            >
                                <option value="threshold">Threshold Strategy</option>
                                <option value="timed">Timed Strategy</option>
                                {/* <option value="Strategy 3">Strategy 3</option> */}
                            </select>
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
}

export default Home;
