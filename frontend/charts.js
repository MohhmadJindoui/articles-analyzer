const API = 'http://localhost:8000/api';

const COLORS = [
    '#3d5afe', '#00bcd4', '#ff4081', '#69f0ae',
    '#ffab40', '#e040fb', '#40c4ff', '#b2ff59'
];

async function fetchJSON(url) {
    try {
        const res = await fetch(url);
        return await res.json();
    } catch (e) {
        console.error('Error fetching', url, e);
        return null;
    }
}

async function loadStats() {
    const total = await fetchJSON(`${API}/stats/total`);
    if (total) document.getElementById('total-count').textContent = total.total;

    const sources = await fetchJSON(`${API}/stats/by-source`);
    if (sources) document.getElementById('sources-count').textContent = sources.length;

    const categories = await fetchJSON(`${API}/stats/by-category`);
    if (categories) document.getElementById('categories-count').textContent = categories.length;

    const languages = await fetchJSON(`${API}/stats/by-language`);
    if (languages) document.getElementById('languages-count').textContent = languages.length;

    // Chart 1: By Source
    if (sources) {
        new Chart(document.getElementById('sourceChart'), {
            type: 'bar',
            data: {
                labels: sources.map(s => s.source),
                datasets: [{
                    label: 'מאמרים',
                    data: sources.map(s => s.count),
                    backgroundColor: COLORS
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#aaa' } },
                    y: { ticks: { color: '#aaa' } }
                }
            }
        });
    }

    // Chart 2: By Category
    if (categories) {
        new Chart(document.getElementById('categoryChart'), {
            type: 'doughnut',
            data: {
                labels: categories.map(c => c.category),
                datasets: [{
                    data: categories.map(c => c.count),
                    backgroundColor: COLORS
                }]
            },
            options: {
                plugins: { legend: { labels: { color: '#aaa' } } }
            }
        });
    }

    // Chart 3: By Language
    if (languages) {
        new Chart(document.getElementById('languageChart'), {
            type: 'pie',
            data: {
                labels: languages.map(l => l.language),
                datasets: [{
                    data: languages.map(l => l.count),
                    backgroundColor: COLORS
                }]
            },
            options: {
                plugins: { legend: { labels: { color: '#aaa' } } }
            }
        });
    }

    // Chart 4: By Date
    const dates = await fetchJSON(`${API}/stats/by-date`);
    if (dates) {
        new Chart(document.getElementById('dateChart'), {
            type: 'line',
            data: {
                labels: dates.map(d => d.date).reverse(),
                datasets: [{
                    label: 'מאמרים',
                    data: dates.map(d => d.count).reverse(),
                    borderColor: '#3d5afe',
                    backgroundColor: 'rgba(61,90,254,0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {
                plugins: { legend: { display: false } },
                scales: {
                    x: { ticks: { color: '#aaa' } },
                    y: { ticks: { color: '#aaa' } }
                }
            }
        });
    }
}

async function loadWordCloud() {
    const words = await fetchJSON(`${API}/stats/wordcloud`);
    const container = document.getElementById('wordcloud-container');

    if (!words || words.length === 0) {
        container.innerHTML = '<div class="loading">אין נתונים</div>';
        return;
    }

    const maxCount = words[0].count;
    container.innerHTML = '';

    words.forEach((w, i) => {
        const size = 12 + (w.count / maxCount) * 28;
        const span = document.createElement('span');
        span.className = 'word-tag';
        span.textContent = w.word;
        span.style.fontSize = size + 'px';
        span.style.background = COLORS[i % COLORS.length] + '33';
        span.style.color = COLORS[i % COLORS.length];
        span.style.border = `1px solid ${COLORS[i % COLORS.length]}55`;
        container.appendChild(span);
    });
}

async function loadArticles() {
    const articles = await fetchJSON(`${API}/articles?limit=10`);
    const tbody = document.getElementById('articles-tbody');

    if (!articles || articles.length === 0) {
        tbody.innerHTML = '<tr><td colspan="5" class="loading">אין מאמרים</td></tr>';
        return;
    }

    tbody.innerHTML = articles.map(a => `
        <tr>
            <td>
                <a href="${a.url || '#'}" target="_blank" style="color:#3d5afe;text-decoration:none">
                    ${a.title || '-'}
                </a>
            </td>
            <td>${a.source || '-'}</td>
            <td><span class="badge badge-${a.category || ''}">${a.category || '-'}</span></td>
            <td>${a.language || '-'}</td>
            <td>${a.published_date || '-'}</td>
        </tr>
    `).join('');
}

// Load on page ready
document.addEventListener('DOMContentLoaded', () => {
    loadStats();
    loadWordCloud();
    loadArticles();
});