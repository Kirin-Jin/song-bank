const input = document.getElementById('sn');

let songbank = [];

// Instantiate Function
function displaySongs(songs) {
    const resultsContainer = document.getElementById('song-results');
    if (!resultsContainer)
        console.error("error : resultContiner is null");
    const totalSpan = document.getElementById('total-songs');

    resultsContainer.innerHTML = '';
    totalSpan.textContent = songs.length;

    songs.forEach(song => {
        const encodedTitle = encodeURIComponent(song.title);
        const songcard = document.createElement('a');
        songcard.className = 'song-card';

        songcard.href = 'show.html?title=' + encodedTitle;
        songcard.style.textDecoration = 'none';
        songcard.style.display = 'block';

        songcard.innerHTML = "<h2>" + song.title + "</h2>";
        resultsContainer.appendChild(songcard);
    });
}

async function initDatabase() {
    try {
        const response = await fetch('database.json');
        songbank = await response.json();
        displaySongs(songbank);
    } catch (err) {
        console.error("error : Failed to load database -> ", err);
    }
}

// Main Function
initDatabase();

input.addEventListener('input', (event) => {
    const query = event.target.value.toLowerCase().trim();

    if (!songbank.length)
        return;

    const filteredSongs = songbank.filter(song => {
        return song.title.toLowerCase().includes(query);
    });

    displaySongs(filteredSongs);
});
