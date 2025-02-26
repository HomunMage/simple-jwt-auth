// Demo/home.tsx

import React, { useState } from 'react';

const HomePage: React.FC = () => {
    const [username, setUsername] = useState<string>('');
    const [password, setPassword] = useState<string>('');
    const [error, setError] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(false);
    const [accessToken, setAccessToken] = useState<string | null>(null);
    const [fileList, setFileList] = useState<string | null>(null);  // Changed state variable

    const SERVER_URL = import.meta.env.VITE_BACKEND_URL;

    const login = async () => {
        setIsLoading(true);
        setError(null);
        try {
            const formData = new URLSearchParams();
            formData.append('username', username);
            formData.append('password', password);

            const response = await fetch(`${SERVER_URL}/auth/token`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                body: formData.toString(),
            });

            if (!response.ok) {
                throw new Error(`Login failed: ${response.status}`);
            }

            const data = await response.json();
            setAccessToken(data.access_token);
            console.log("Access Token:", data.access_token);

        } catch (err) {
            setError(`Login Error: ${err}`);
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const fetchFileList = async () => {  // Changed function name
        setIsLoading(true);
        setError(null);
        try {
            if (!accessToken) {
                throw new Error("No access token available. Please log in.");
            }

            const response = await fetch(`${SERVER_URL}/auth/files`, {  // Changed URL
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${accessToken}`,
                },
            });

            if (!response.ok) {
                throw new Error(`Failed to fetch file list: ${response.status}`);
            }

            const data = await response.text(); // Expecting a string now
            setFileList(data); // Update state with file list string
            console.log("File List:", data);

        } catch (err) {
            setError(`File List Error: ${err}`);
            console.error(err);
        } finally {
            setIsLoading(false);
        }
    };

    const handleUsernameChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(event.target.value);
    };

    const handlePasswordChange = (event: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(event.target.value);
    };


    return (
        <div>
            <h2>Welcome to the Demo Page!</h2>

            {error && (
                <div style={{ color: 'red' }}>
                    Error: {error}
                </div>
            )}

            {isLoading && (
                <div>
                    Loading...
                </div>
            )}

            <label>
                Username:
                <input type="text" value={username} onChange={handleUsernameChange} />
            </label>
            <br />
            <label>
                Password:
                <input type="password" value={password} onChange={handlePasswordChange} />
            </label>
            <br />

            <button onClick={login} disabled={isLoading}>
                {isLoading ? 'Logging in...' : 'Get Access Token'}
            </button>

            {accessToken && (
                <div>
                    <strong>Access Token:</strong> <pre>{accessToken}</pre>
                    <button onClick={fetchFileList} disabled={isLoading}> {/* Changed function call */}
                        {isLoading ? 'Fetching...' : 'Get File List'}
                    </button>
                </div>
            )}

            {fileList && (  // Changed conditional rendering
                <div>
                    <strong>File List:</strong> {fileList}
                </div>
            )}
        </div>
    );
};

export default HomePage;