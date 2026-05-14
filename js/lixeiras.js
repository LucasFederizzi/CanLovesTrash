async function loadLixeiras() {
    const bins = await getBins();
    renderLixeiras(bins);
}

function renderLixeiras(bins) {
    const tbody = document.querySelector("#binTable tbody");
    tbody.innerHTML = "";

    if (bins.length === 0) {
        tbody.innerHTML = `
            <tr>
                <td colspan="6" class="text-center">Nenhuma lixeira registrada.</td>
            </tr>
        `;
        return;
    }

    bins.forEach(bin => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${bin.nome}</td>
            <td>${bin.lat}</td>
            <td>${bin.lng}</td>
            <td>${bin.ocupacao}%</td>
            <td>${bin.tampa}</td>
            <td>
                <button class="btn btn-sm btn-danger" onclick="handleDeleteBin(${bin.id})">Excluir</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function handleDeleteBin(id) {
    await deleteBin(id);
    loadLixeiras();
}

loadLixeiras();
