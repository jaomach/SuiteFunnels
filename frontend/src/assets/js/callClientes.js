export async function callClientes() {
    const token = document.cookie.split('; ').find(row => row.startsWith('token=')).split('=')[1];
    if (token) {
        try {
            const response = await fetch("/api/call_clientes", {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`,
                },
            });
            const data = await response.json();

            if (data.clientes && Array.isArray(data.clientes)) {
                const clientesList = document.getElementById('sidebar');

                data.clientes.forEach(cliente => {
                    const actualCliente = Object.entries(cliente)[2][1];
                    const idCliente = Object.entries(cliente)[0][1];

                    // Criar router-link para cada cliente
                    const routerLink = document.createElement('router-link');
                    routerLink.textContent = actualCliente;
                    routerLink.setAttribute('to', `/dashboard/${idCliente}`);  // O idCliente é o token

                    // Adicionar o router-link à lista de clientes
                    clientesList.appendChild(routerLink);
                });
            } else {
                console.error("Nenhum cliente encontrado ou formato inválido.");
            }
        } catch (error) {
            console.error("Erro ao verificar o token:", error);
        }
    }
}
