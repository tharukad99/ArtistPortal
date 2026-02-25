document.addEventListener('DOMContentLoaded', function() {
    loadDashboardData();

    const syncBtn = document.getElementById('sync-now');
    if (syncBtn) {
        syncBtn.addEventListener('click', function() {
            syncBtn.disabled = true;
            syncBtn.innerText = 'Syncing...';
            
            fetch('/social/sync', { method: 'POST' })
                .then(res => res.json())
                .then(data => {
                    if (data.status === 'success') {
                        location.reload();
                    } else {
                        alert('Sync failed: ' + data.message);
                        syncBtn.disabled = false;
                        syncBtn.innerText = 'Sync Now';
                    }
                })
                .catch(err => {
                    alert('Sync error: ' + err);
                    syncBtn.disabled = false;
                    syncBtn.innerText = 'Sync Now';
                });
        });
    }
});

function loadDashboardData() {
    fetch('/social/api/data')
        .then(res => res.json())
        .then(data => {
            renderCharts(data);
            updateSummaryCards(data);
        });
}

function updateSummaryCards(data) {
    // Helper to get latest value
    const getLatest = (key) => data[key] ? data[key].values.slice(-1)[0] : 0;
    const getTrend = (key) => {
        if (!data[key] || data[key].values.length < 2) return '';
        const cur = data[key].values.slice(-1)[0];
        const prev = data[key].values.slice(-2)[0];
        const diff = cur - prev;
        const pct = prev !== 0 ? ((diff / prev) * 100).toFixed(1) : '0';
        return diff >= 0 ? `<span class="up">↑ ${pct}%</span>` : `<span class="down">↓ ${pct}%</span>`;
    };

    if (data['instagram_followers']) {
        document.getElementById('ig-followers-val').innerText = getLatest('instagram_followers').toLocaleString();
        document.getElementById('ig-followers-trend').innerHTML = getTrend('instagram_followers');
    }
    if (data['facebook_followers']) {
        document.getElementById('fb-followers-val').innerText = getLatest('facebook_followers').toLocaleString();
        document.getElementById('fb-followers-trend').innerHTML = getTrend('facebook_followers');
    }
    if (data['instagram_reach']) {
        document.getElementById('ig-reach-val').innerText = getLatest('instagram_reach').toLocaleString();
        document.getElementById('ig-reach-trend').innerHTML = getTrend('instagram_reach');
    }
    if (data['facebook_reach']) {
        document.getElementById('fb-reach-val').innerText = getLatest('facebook_reach').toLocaleString();
        document.getElementById('fb-reach-trend').innerHTML = getTrend('facebook_reach');
    }
}

function renderCharts(data) {
    const ctxFollowers = document.getElementById('followersChart');
    const ctxReach = document.getElementById('reachChart');

    if (!ctxFollowers || !ctxReach) return;

    // Followers Chart
    new Chart(ctxFollowers, {
        type: 'line',
        data: {
            labels: data['instagram_followers'] ? data['instagram_followers'].labels : [],
            datasets: [
                {
                    label: 'IG Followers',
                    data: data['instagram_followers'] ? data['instagram_followers'].values : [],
                    borderColor: '#4f46e5',
                    tension: 0.3,
                    fill: false
                },
                {
                    label: 'FB Followers',
                    data: data['facebook_followers'] ? data['facebook_followers'].values : [],
                    borderColor: '#10b981',
                    tension: 0.3,
                    fill: false
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } },
            scales: { y: { beginAtZero: false } }
        }
    });

    // Reach Chart
    new Chart(ctxReach, {
        type: 'bar',
        data: {
            labels: data['instagram_reach'] ? data['instagram_reach'].labels : [],
            datasets: [
                {
                    label: 'IG Reach',
                    data: data['instagram_reach'] ? data['instagram_reach'].values : [],
                    backgroundColor: '#818cf8'
                },
                {
                    label: 'FB Reach',
                    data: data['facebook_reach'] ? data['facebook_reach'].values : [],
                    backgroundColor: '#34d399'
                }
            ]
        },
        options: {
            responsive: true,
            plugins: { legend: { position: 'bottom' } },
            scales: { y: { beginAtZero: true } }
        }
    });
}
