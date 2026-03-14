/**
 * API Service Layer
 * Handles all communication with the FastAPI backend.
 * Includes authentication and JWT token management.
 */

const API_BASE = '/api';

/**
 * Get authorization headers with JWT token.
 */
function getAuthHeaders() {
    const token = localStorage.getItem('token');
    return token ? { 'Authorization': `Bearer ${token}` } : {};
}

// ─── Auth ──────────────────────────────────────────────

export async function signupUser(email, password, fullName = '') {
    const response = await fetch(`${API_BASE}/auth/signup`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password, full_name: fullName }),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Signup failed' }));
        throw new Error(error.detail || 'Failed to create account');
    }

    return response.json();
}

export async function loginUser(email, password) {
    const response = await fetch(`${API_BASE}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Login failed' }));
        throw new Error(error.detail || 'Invalid credentials');
    }

    return response.json();
}

export async function getMe() {
    const response = await fetch(`${API_BASE}/auth/me`, {
        headers: getAuthHeaders(),
    });

    if (!response.ok) throw new Error('Not authenticated');
    return response.json();
}

// ─── Contracts ─────────────────────────────────────────

/**
 * Upload a contract file for analysis.
 */
export async function uploadContract(file, role = 'neutral') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('role', role);

    const response = await fetch(`${API_BASE}/upload`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(error.detail || 'Failed to upload contract');
    }

    return response.json();
}

/**
 * List all contracts for the current user.
 */
export async function listContracts() {
    const response = await fetch(`${API_BASE}/contracts`, {
        headers: getAuthHeaders(),
    });

    if (!response.ok) throw new Error('Failed to fetch contracts');
    return response.json();
}

/**
 * Get a previously analyzed contract.
 */
export async function getContract(contractId) {
    const response = await fetch(`${API_BASE}/contracts/${contractId}`, {
        headers: getAuthHeaders(),
    });

    if (!response.ok) throw new Error('Contract not found');
    return response.json();
}

// ─── Chat ──────────────────────────────────────────────

/**
 * Send a chat message to the AI assistant.
 */
export async function sendChatMessage(message, contractId = null) {
    const response = await fetch(`${API_BASE}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify({ message, contract_id: contractId }),
    });

    if (!response.ok) throw new Error('Failed to send message');
    return response.json();
}

/**
 * Upload a contract file within the chat context.
 */
export async function uploadAndChat(file, message = 'Analyze this contract', role = 'neutral') {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('message', message);
    formData.append('role', role);

    const response = await fetch(`${API_BASE}/chat-upload`, {
        method: 'POST',
        headers: getAuthHeaders(),
        body: formData,
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Upload failed' }));
        throw new Error(error.detail || 'Failed to analyze contract');
    }

    return response.json();
}

/**
 * Get chat history for a contract.
 */
export async function getChatHistory(contractId) {
    const response = await fetch(`${API_BASE}/chat/${contractId}/history`, {
        headers: getAuthHeaders(),
    });

    if (!response.ok) return [];
    return response.json();
}

// ─── Draft ─────────────────────────────────────────────

/**
 * Generate a contract draft.
 */
export async function generateDraft(params) {
    const response = await fetch(`${API_BASE}/draft`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            ...getAuthHeaders(),
        },
        body: JSON.stringify(params),
    });

    if (!response.ok) {
        const error = await response.json().catch(() => ({ detail: 'Draft generation failed' }));
        throw new Error(error.detail || 'Failed to generate draft');
    }

    return response.json();
}

// ─── Sessions ──────────────────────────────────────────

/**
 * List all chat sessions.
 */
export async function listSessions() {
    const response = await fetch(`${API_BASE}/sessions`, {
        headers: getAuthHeaders(),
    });

    if (!response.ok) return [];
    return response.json();
}
