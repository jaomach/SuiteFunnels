export async function loginUser() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const errorMessage = document.getElementById('errorMessage');

    const data = { email, password };

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
        });

        const result = await response.json();

        if (response.ok) {
            window.location.href = '/dashboard';
            criarCookie('token', result.token, 1);
            document.getElementById('loginForm').reset();
        } else {
            errorMessage.textContent = result.message;
            errorMessage.style.display = 'block';
        }
    } catch (error) {
        errorMessage.textContent = 'Erro ao conectar com o servidor';
        errorMessage.style.display = 'block';
    }
}

export function criarCookie(nome, valor, dias) {
    let dataExpiracao = "";
    if (dias) {
        const data = new Date();
        data.setTime(data.getTime() + dias * 24 * 60 * 60 * 1000);
        dataExpiracao = "; expires=" + data.toUTCString();
    }
    document.cookie = nome + "=" + encodeURIComponent(valor) + dataExpiracao + "; path=/";
}
