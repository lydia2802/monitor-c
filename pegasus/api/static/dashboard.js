(() => {
  const API_BASE = '/api/v1';
  const state = {
    token: sessionStorage.getItem('pegasus_token') || null,
    role: sessionStorage.getItem('pegasus_role') || null,
    username: sessionStorage.getItem('pegasus_username') || null,
  };

  const $ = (id) => document.getElementById(id);

  function authHeaders(json = true) {
    const headers = {};
    if (json) headers['Content-Type'] = 'application/json';
    if (state.token) headers['Authorization'] = `Bearer ${state.token}`;
    return headers;
  }

  async function apiGet(path) {
    const res = await fetch(API_BASE + path, { headers: authHeaders(false) });
    return { ok: res.ok, body: await res.json().catch(() => ({})) };
  }

  async function apiPost(path, payload) {
    const res = await fetch(API_BASE + path, {
      method: 'POST',
      headers: authHeaders(true),
      body: JSON.stringify(payload || {}),
    });
    return { ok: res.ok, body: await res.json().catch(() => ({})) };
  }

  function showApp() {
    $('login-view').classList.add('hidden');
    $('app-view').classList.remove('hidden');
    $('whoami').textContent = `${state.username} (${state.role})`;
    document.querySelectorAll('.admin-only').forEach((el) => {
      el.classList.toggle('hidden', state.role !== 'admin');
    });
    refreshHealth();
    loadOverview();
  }

  function showLogin(message) {
    sessionStorage.clear();
    state.token = null;
    $('app-view').classList.add('hidden');
    $('login-view').classList.remove('hidden');
    $('login-error').textContent = message || '';
  }

  // ---- Login ----
  $('login-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = $('login-username').value.trim();
    const password = $('login-password').value;
    const { ok, body } = await apiPost('/auth/login', { username, password });
    if (ok && body.success) {
      state.token = body.token;
      state.role = body.user.role;
      state.username = body.user.username;
      sessionStorage.setItem('pegasus_token', state.token);
      sessionStorage.setItem('pegasus_role', state.role);
      sessionStorage.setItem('pegasus_username', state.username);
      showApp();
    } else {
      $('login-error').textContent = body.error || 'Login gagal';
    }
  });

  $('logout-btn').addEventListener('click', () => showLogin());

  // ---- Tabs ----
  document.querySelectorAll('.tab-btn').forEach((btn) => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach((b) => b.classList.remove('active'));
      document.querySelectorAll('.tab-panel').forEach((p) => p.classList.remove('active'));
      btn.classList.add('active');
      $(`tab-${btn.dataset.tab}`).classList.add('active');
      if (btn.dataset.tab === 'history') loadHistory();
      if (btn.dataset.tab === 'users') loadUsers();
    });
  });

  // ---- Health (online status) ----
  async function refreshHealth() {
    const badge = $('server-status');
    try {
      const { ok, body } = await apiGet('/health');
      if (ok && body.status === 'healthy') {
        badge.textContent = `online v${body.version}`;
        badge.className = 'badge badge-online';
      } else {
        throw new Error('unhealthy');
      }
    } catch (e) {
      badge.textContent = 'offline';
      badge.className = 'badge badge-offline';
    }
  }

  // ---- Overview ----
  function renderBars(container, rows, max) {
    container.innerHTML = '';
    if (!rows.length) {
      container.innerHTML = '<div class="bar-row"><span class="bar-label">Tidak ada data</span></div>';
      return;
    }
    rows.forEach(([label, count]) => {
      const pct = max > 0 ? Math.round((count / max) * 100) : 0;
      const row = document.createElement('div');
      row.className = 'bar-row';
      row.innerHTML = `
        <span class="bar-label" title="${label}">${label}</span>
        <span class="bar-track"><span class="bar-fill" style="width:${pct}%"></span></span>
        <span class="bar-count">${count}</span>`;
      container.appendChild(row);
    });
  }

  async function loadOverview() {
    const { ok, body } = await apiGet('/analytics/stats');
    if (ok && body.success) {
      const s = body.data;
      $('stat-cards').innerHTML = [
        ['Searches (1 jam)', s.searches_last_hour],
        ['Searches (hari ini)', s.searches_today],
        ['Total Searches', s.total_searches],
        ['Unique Targets', s.unique_targets],
        ['API Success Rate', `${Number(s.api_success_rate).toFixed(1)}%`],
        ['Phone / NIK', `${s.phone_count} / ${s.nik_count}`],
      ].map(([label, value]) => `
        <div class="card"><div class="value">${value}</div><div class="label">${label}</div></div>
      `).join('');

      const locs = (s.top_locations || []);
      const maxLoc = Math.max(1, ...locs.map(([, c]) => c));
      renderBars($('location-list'), locs, maxLoc);
    }

    const trendRes = await apiGet('/analytics/trends?hours=24');
    if (trendRes.ok && trendRes.body.success) {
      const trend = trendRes.body.data.trend;
      const rows = trend.map((c, i) => [`${trend.length - i}j lalu`, c]);
      renderBars($('trend-chart'), rows, Math.max(1, ...trend));
    }

    const opRes = await apiGet('/analytics/operators');
    if (opRes.ok && opRes.body.success) {
      const entries = Object.entries(opRes.body.data).sort((a, b) => b[1] - a[1]);
      renderBars($('operator-chart'), entries, Math.max(1, ...entries.map(([, c]) => c)));
    }
  }

  // ---- Search ----
  $('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const type = $('search-type').value;
    const target = $('search-target').value.trim();
    const out = $('search-result');
    out.textContent = 'Mencari...';
    const { ok, body } = await apiPost(`/search/${type}`, { [type]: target });
    if (ok && body.success) {
      out.textContent = JSON.stringify(body.data, null, 2);
    } else {
      out.textContent = `Error: ${body.error || 'Tidak ditemukan'}`;
    }
  });

  // ---- History ----
  $('refresh-history').addEventListener('click', loadHistory);
  async function loadHistory() {
    const { ok, body } = await apiGet('/history?limit=50');
    const tbody = $('history-body');
    tbody.innerHTML = '';
    if (ok && body.success) {
      body.data.forEach((row) => {
        const result = row.result || row.result_json || {};
        const parsed = typeof result === 'string' ? safeParse(result) : result;
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${row.target || '-'}</td>
          <td>${row.timestamp || '-'}</td>
          <td>${(parsed && parsed.Source) || '-'}</td>`;
        tbody.appendChild(tr);
      });
    }
  }

  function safeParse(s) {
    try { return JSON.parse(s); } catch (e) { return {}; }
  }

  // ---- Anomalies ----
  $('refresh-anomalies').addEventListener('click', loadAnomalies);
  async function loadAnomalies() {
    const out = $('anomalies-output');
    out.textContent = 'Loading...';
    const { ok, body } = await apiGet('/analytics/anomalies');
    out.textContent = ok && body.success ? JSON.stringify(body.data, null, 2) : (body.error || 'Gagal memuat');
  }

  // ---- Users (admin) ----
  async function loadUsers() {
    const { ok, body } = await apiGet('/users');
    const tbody = $('users-body');
    tbody.innerHTML = '';
    if (ok && body.success) {
      body.data.forEach((u) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
          <td>${u.username}</td>
          <td>${u.role}</td>
          <td>${u.last_login || '-'}</td>
          <td>${u.is_active ? 'Ya' : 'Tidak'}</td>`;
        tbody.appendChild(tr);
      });
    }
  }

  $('create-user-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = $('new-username').value.trim();
    const password = $('new-password').value;
    const role = $('new-role').value;
    const { ok, body } = await apiPost('/users', { username, password, role });
    if (ok && body.success) {
      $('create-user-form').reset();
      loadUsers();
    } else {
      alert(body.error || 'Gagal membuat user');
    }
  });

  // ---- Init ----
  if (state.token) {
    showApp();
  } else {
    showLogin();
  }
  setInterval(refreshHealth, 30000);
})();
