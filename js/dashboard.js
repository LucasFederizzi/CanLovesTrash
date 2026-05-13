async function loadDashboard() {

    const bins = await getBins();

    // Atualiza cards
    document.getElementById("totalBins").innerText = bins.length;

    const fullBins = bins.filter(bin => bin.ocupacao >= 70);
    document.getElementById("fullBins").innerText = fullBins.length;

    const alerts = bins.filter(bin => bin.tampa === "aberta");
    document.getElementById("alerts").innerText = alerts.length;

    // Atualiza mapa
    addBinsToMap(bins);
}

loadDashboard();