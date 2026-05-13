const map = L.map('map').setView([-28.2628, -52.4064], 13);
const markerGroup = L.layerGroup().addTo(map);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(map);

function addBinsToMap(bins) {
    markerGroup.clearLayers();

    bins.forEach(bin => {

        let color = "green";

        if (bin.ocupacao > 70)
            color = "red";
        else if (bin.ocupacao > 40)
            color = "orange";

        const marker = L.circleMarker(
            [bin.lat, bin.lng],
            {
                radius: 10,
                color: color
            }
        ).addTo(markerGroup);

        marker.bindPopup(`
            <b>${bin.nome}</b><br>
            Ocupação: ${bin.ocupacao}%<br>
            Tampa: ${bin.tampa}
        `);

        marker.bindTooltip(`
            <strong>${bin.nome}</strong><br>
            Ocupação: ${bin.ocupacao}%<br>
            Tampa: ${bin.tampa}
        `, {
            direction: 'top',
            offset: [0, -10],
            opacity: 0.9
        });
    });

}