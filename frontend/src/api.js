
// Configurable API Base URL
const BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

async function request(path, options = {}) {
    const url = `${BASE_URL}${path}`;
    const res = await fetch(url, {
        headers: { 'Content-Type': 'application/json' },
        ...options,
    });

    if (!res.ok) throw new Error(`Error: ${res.status}`);
    
    return res.json();
}

// 1. Health Endpoint
export const fetchHealth = () => request('/health');

// 2. Main API Endpoint
export const fetchTasks = () => request('/api/v1/tasks');