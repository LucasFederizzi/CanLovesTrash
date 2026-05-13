const STORAGE_KEY = "lixeiras_inteligentes";

const defaultBins = [
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

function loadBinsFromStorage() {
    const stored = localStorage.getItem(STORAGE_KEY);
    if (!stored) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultBins));
        return defaultBins.slice();
    }

    try {
        return JSON.parse(stored);
    } catch (error) {
        localStorage.setItem(STORAGE_KEY, JSON.stringify(defaultBins));
        return defaultBins.slice();
    }
}

function saveBinsToStorage(bins) {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(bins));
}

async function getBins() {
    return loadBinsFromStorage();
}

function addBin(bin) {
    const bins = loadBinsFromStorage();
    bins.push(bin);
    saveBinsToStorage(bins);
}

function deleteBin(id) {
    const bins = loadBinsFromStorage().filter(bin => bin.id !== id);
    saveBinsToStorage(bins);
}
