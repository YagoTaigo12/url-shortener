const API_BASE = '/api';

const Auth = {
    isAuthenticated: () => {
        const token = localStorage.getItem('token');
        if (!token) return false;
        
        // Opcional: Verificar expiração do token se for JWT decodificável
        // Por simplicidade do MVP, apenas verifica existência
        return true;
    },

    getToken: () => {
        return localStorage.getItem('token');
    },

    login: async (username, password) => {
        const formData = new FormData();
        formData.append('username', username);
        formData.append('password', password);

        try {
            const response = await fetch(`${API_BASE}/auth/token`, {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Falha no login');
            }

            const data = await response.json();
            localStorage.setItem('token', data.access_token);
            localStorage.setItem('username', username); // Salva usuário para exibição
            return true;
        } catch (error) {
            console.error('Login error:', error);
            throw error;
        }
    },

    logout: () => {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        window.location.href = '/login.html';
    },

    checkAuthAndRedirect: () => {
        // Se não estiver na tela de login e não tiver token -> vai pro login
        if (!Auth.isAuthenticated() && !window.location.pathname.includes('login.html')) {
            window.location.href = '/login.html';
        }
        // Se estiver no login e tiver token -> vai pra home
        if (Auth.isAuthenticated() && window.location.pathname.includes('login.html')) {
            window.location.href = '/';
        }
    }
};
