let bins = [];

async function loadDashboard() {
    bins = await getBins();
    renderDashboard();
}

function renderDashboard() {
    document.getElementById("totalBins").innerText = bins.length;

    const fullBins = bins.filter(bin => bin.ocupacao >= 70);
    document.getElementById("fullBins").innerText = fullBins.length;

    const alerts = bins.filter(bin => bin.tampa === "aberta");
    document.getElementById("alerts").innerText = alerts.length;

    addBinsToMap(bins);
}

function handleNewBin(event) {
    event.preventDefault();

    const name = document.getElementById("binName").value.trim();
    const lat = parseFloat(document.getElementById("binLat").value);
    const lng = parseFloat(document.getElementById("binLng").value);
    const ocupacao = parseInt(document.getElementById("binOccupancy").value, 10);
    const tampa = document.getElementById("binLid").value;

    if (!name || Number.isNaN(lat) || Number.isNaN(lng) || Number.isNaN(ocupacao)) {
        alert("Preencha todos os campos corretamente.");
        return;
    }

    const newBin = {
        id: Date.now(),
        nome: name,
        lat,
        lng,
        ocupacao,
        tampa
    };

    addBin(newBin);
    bins.push(newBin);
    renderDashboard();

    document.getElementById("newBinForm").reset();
}

loadDashboard();

document.getElementById("newBinForm")?.addEventListener("submit", handleNewBin);