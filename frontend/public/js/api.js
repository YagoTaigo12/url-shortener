const API = {
    headers: () => {
        return {
            'Authorization': `Bearer ${Auth.getToken()}`,
            'Content-Type': 'application/json'
        };
    },

    handleError: (response) => {
        if (response.status === 401) {
            Auth.logout();
            throw new Error('Sessão expirada');
        }
        return response;
    },

    shortenUrl: async (originalUrl) => {
        const response = await fetch(`${API_BASE}/urls/`, {
            method: 'POST',
            headers: API.headers(),
            body: JSON.stringify({ original_url: originalUrl })
        });
        API.handleError(response);
        if (!response.ok) throw new Error('Erro ao encurtar URL');
        return await response.json();
    },

    listUrls: async () => {
        const response = await fetch(`${API_BASE}/urls/`, {
            method: 'GET',
            headers: API.headers()
        });
        API.handleError(response);
        if (!response.ok) throw new Error('Erro ao listar URLs');
        return await response.json();
    },

    deleteUrl: async (shortCode) => {
        const response = await fetch(`${API_BASE}/urls/${shortCode}`, {
            method: 'DELETE',
            headers: API.headers()
        });
        API.handleError(response);
        if (!response.ok) throw new Error('Erro ao deletar URL');
        return true;
    }
};
