document.getElementById('themeToggle').addEventListener('click', function () {
    const body = document.body;
    body.classList.toggle('dark-mode');
    body.classList.toggle('light-mode');
    const isDarkMode = body.classList.contains('dark-mode');
    this.textContent = isDarkMode ? 'Switch to Light Mode' : 'Switch to Dark Mode';
});

document.getElementById('content').addEventListener('dblclick', async function () {
    const selection = window.getSelection();
    const word = selection.toString().trim();

    if (word) {
        showLoading();
        const timeoutId = setTimeout(() => {
            hideLoading();
            alert('Request timed out. Please try again.');
        }, 5000); // 5 seconds timeout

        await fetchAndDisplayWord(word);
        clearTimeout(timeoutId);
        hideLoading();
    }
});
document.addEventListener('click', function (event) {
    const popup = document.getElementById('popup');
    const isClickInsidePopup = popup.contains(event.target);
    const isClickInsideSearchButton = document.getElementById('searchButton').contains(event.target);

    if (!isClickInsidePopup && !isClickInsideSearchButton) {
        popup.style.display = 'none';
    }
});


async function fetchAndDisplayWord(word) {
    try {
        document.getElementById('searchBox').value = '';
        const response = await fetch(`./dictionary/${word}`);
        if (response.ok) {
            const data = await response.json();
            document.getElementById('term').textContent = data.term || "N/A";
            formatWordDetails(data);
            document.getElementById('popup').style.display = 'block';
        } else {
            document.getElementById('popupContent').innerHTML = '<p>Word not found.</p>';
            document.getElementById('popup').style.display = 'block';
        }
    } catch (error) {
        console.error('Error fetching word:', error);
        document.getElementById('popupContent').innerHTML = '<p>An error occurred.</p>';
    }
}

function playUtterance(text) {
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.lang = 'en-US';
    speechSynthesis.speak(utterance);
}

function formatWordDetails(data) {
    if (data.us_phonetic || data.uk_phonetic) {
        document.getElementById('phoneticsList').innerHTML = `
                    ${data.us_phonetic ? `<li>US: ${data.us_phonetic.text} 
                        <span class="voice-icon">
                            <img src="../static/images/speaker.png" onclick="playAudio('${data.us_phonetic.audio_url}')">
                        </span>
                    </li>` : ''}
                    ${data.uk_phonetic ? `<li>UK: ${data.uk_phonetic.text} 
                        <span class="voice-icon">
                            <img src="../static/images/speaker.png" onclick="playAudio('${data.uk_phonetic.audio_url}')">
                        </span>
                    </li>` : ''}
                `;
    } else {
        if ('speechSynthesis' in window) {
            document.getElementById('phoneticsList').innerHTML = `
                        <li>
                            TTS: <span class="voice-icon">
                                <img src="../static/images/speaker.png" onclick="playUtterance('${data.term}')">
                            </span>
                        </li>
                    `;
        } else {
            document.getElementById('phoneticsList').innerHTML = '<li>Phonetics not available</li>';
        }
    }




    document.getElementById('meaningsList').innerHTML = data.meanings
        ? data.meanings.map(meaning => `
                    <li>
                        <span style="color: blue;"><strong>${meaning.partOfSpeech}:</strong></span>
                        <ul>
                            ${meaning.definitions.map(def => `
                                <li>
                                    ${def.definition}
                                    ${def.example ? `<br><em class="example-label">Example:</em> 
                                    <span class="voice-icon">
                                        <img src="../static/images/speaker.png" onclick="playUtterance('${def.example}')">
                                    </span> <span class="example-content">${def.example.replace(new RegExp(data.term, 'gi'), match => `<span class="example-term">${match}</span>`)}</span>` : ''}
                                </li>
                            `).join('')}
                        </ul>
                    </li>
                `).join('')
        : '<li>No meanings available</li>';

    document.getElementById('synonymsList').textContent = data.synonyms?.join(', ') || 'No synonyms available';
    document.getElementById('antonymsList').textContent = data.antonyms?.join(', ') || 'No antonyms available';
}

function playAudio(url) {
    if (url) {
        const audio = new Audio(url);
        audio.play();
    }
}

function showLoading() {
    document.getElementById('loading').style.display = 'block';
    document.getElementById('mainContent').classList.add('blurred');
}

function hideLoading() {
    document.getElementById('loading').style.display = 'none';
    document.getElementById('mainContent').classList.remove('blurred');
}

function handleSearchClick() {
    const searchWord = document.getElementById('searchBox').value.trim();
    if (searchWord) {
        showLoading();
        fetchAndDisplayWord(searchWord).then(hideLoading);
    }
}

document.getElementById('searchButton').addEventListener('click', function () {
    handleSearchClick();
});