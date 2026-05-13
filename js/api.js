async function getBins() {

    // EXEMPLO MOCKADO
    return [
        {
            id: 1,
            nome: "Lixeira Central",
            lat: -28.265374,
            lng: -52.397234,
            ocupacao: 80,
            tampa: "fechada"
        },

        {
            id: 2,
            nome: "Lixeira Praça",
            lat: -28.263911,
            lng: -52.398060,
            ocupacao: 45,
            tampa: "aberta"
        }
    ];

    /*
    FUTURAMENTE:

    const response = await fetch("http://localhost:5000/bins");
    return await response.json();
    */
}