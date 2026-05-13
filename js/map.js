const map = L.map('map').setView([-28.2628, -52.4064], 13);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap'
}).addTo(map);

function addBinsToMap(bins) {

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
        ).addTo(map);

        marker.bindPopup(`
            <b>${bin.nome}</b><br>
            Ocupação: ${bin.ocupacao}%<br>
            Tampa: ${bin.tampa}
        `);
    });

}