const API_BASE = "http://localhost:5000";

async function getBins() {
    const response = await fetch(`${API_BASE}/bins`);
    return await response.json();
}

async function addBin(bin) {
    const response = await fetch(`${API_BASE}/bins`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(bin)
    });
    return await response.json();
}

async function deleteBin(id) {
    const response = await fetch(`${API_BASE}/bins/${id}`, {
        method: 'DELETE'
    });
    return await response.json();
}

async function updateBin(id, data) {
    const response = await fetch(`${API_BASE}/bins/${id}`, {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)
    });
    return await response.json();
}
