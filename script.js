document.addEventListener('DOMContentLoaded', () => {
  const grid = document.getElementById('hikaku-grid');
  if (!grid) return;

  const cards = Array.from(grid.querySelectorAll('.hikaku-card'));
  const totalCount = cards.length;
  const MAX_COMPARE = 3;

  const priceMinSelect = document.getElementById('f-price-min');
  const priceMaxSelect = document.getElementById('f-price-max');
  const startSelect = document.getElementById('f-start');
  const serviceSelect = document.getElementById('f-service');
  const twoPaxSelect = document.getElementById('f-twopax');
  const checkInputs = Array.from(document.querySelectorAll('#filter-checks input[type="checkbox"]'));
  const resetBtn = document.getElementById('filter-reset');
  const resultCount = document.getElementById('result-count');

  const tray = document.getElementById('compare-tray');
  const trayTableWrap = document.getElementById('compare-table-wrap');
  const trayEmpty = document.getElementById('compare-empty');

  let compareIds = [];

  function inPriceRange(price, min, max) {
    if (!price) return false;
    return price >= min && price <= max;
  }

  function matchesRoom(card, roomRequired) {
    if (!roomRequired) return true;
    return card.dataset.room === 'yes';
  }

  function matchesStart(card, value) {
    if (value === 'all') return true;
    return card.dataset.startHour === value;
  }

  function matchesService(card, value) {
    if (value === 'all') return true;
    return card.dataset.service === value;
  }

  function inTwoPaxRange(twoPaxNum, rangeValue) {
    if (rangeValue === 'all') return true;
    if (rangeValue === 'unknown') return !twoPaxNum;
    if (!twoPaxNum) return false;
    const ranges = {
      t1: [0, 39999],
      t2: [40000, 54999],
      t3: [55000, Infinity],
    };
    const [min, max] = ranges[rangeValue];
    return twoPaxNum >= min && twoPaxNum <= max;
  }

  function matchesFeatures(card, wantedFeatures) {
    if (wantedFeatures.length === 0) return true;
    const cardFeatures = (card.dataset.features || '').split('|').filter(Boolean);
    return wantedFeatures.some(f => cardFeatures.includes(f));
  }

  function applyFilters() {
    const roomRequired = checkInputs.some(cb => cb.dataset.filter === 'room' && cb.checked);
    const wantedFeatures = checkInputs
      .filter(cb => cb.dataset.filter === 'feature' && cb.checked)
      .map(cb => cb.value);
    const min = Number(priceMinSelect.value);
    const max = Number(priceMaxSelect.value);

    let visibleCount = 0;
    cards.forEach(card => {
      const price = Number(card.dataset.price) || null;
      const twoPaxNum = Number(card.dataset.twoPaxNum) || null;
      const show =
        inPriceRange(price, min, max) &&
        matchesRoom(card, roomRequired) &&
        matchesStart(card, startSelect.value) &&
        matchesService(card, serviceSelect.value) &&
        inTwoPaxRange(twoPaxNum, twoPaxSelect.value) &&
        matchesFeatures(card, wantedFeatures);
      card.style.display = show ? '' : 'none';
      if (show) visibleCount++;
    });
    resultCount.textContent = `${totalCount}件中${visibleCount}件を表示`;
  }

  function renderTray() {
    if (compareIds.length === 0) {
      tray.hidden = true;
      return;
    }
    tray.hidden = false;
    trayEmpty.hidden = true;

    const selectedCards = compareIds.map(id => cards.find(c => c.dataset.id === id)).filter(Boolean);

    const rows = [
      { label: 'コース料金', key: 'coursePrice' },
      { label: 'サービス料', key: 'serviceLabel' },
      { label: '2名・料理利用額', key: 'twoPax' },
      { label: '個室', key: 'roomLabel' },
      { label: 'コース開始時間', key: 'startLabel' },
      { label: '特徴', key: 'features', isTags: true },
      { label: '予約', key: 'reserveUrl', isReserve: true },
    ];

    let html = '<table class="compare-table"><thead><tr><th></th>';
    selectedCards.forEach(card => {
      html += `<th><div class="compare-th-row"><span>${card.dataset.name}</span><button type="button" class="compare-remove" data-remove="${card.dataset.id}" aria-label="比較から外す">×</button></div></th>`;
    });
    html += '</tr></thead><tbody>';

    rows.forEach(row => {
      html += `<tr><th>${row.label}</th>`;
      selectedCards.forEach(card => {
        if (row.isReserve) {
          const url = card.dataset.reserveUrl;
          html += `<td><span class="cell-reserve"><a class="btn-reserve" href="${url}" target="_blank" rel="noopener">予約する</a></span></td>`;
        } else if (row.isTags) {
          const tags = (card.dataset.features || '').split('|').filter(Boolean);
          html += `<td><span class="cell-tags">${tags.map(t => `<span class="feature-pill">${t}</span>`).join('')}</span></td>`;
        } else {
          const val = card.dataset[row.key] || '情報なし(要確認)';
          const unknown = val.includes('情報なし') ? ' is-unknown' : '';
          html += `<td class="${unknown}">${val}</td>`;
        }
      });
      html += '</tr>';
    });

    html += '</tbody></table>';
    trayTableWrap.innerHTML = html;
    trayTableWrap.hidden = false;

    trayTableWrap.querySelectorAll('[data-remove]').forEach(btn => {
      btn.addEventListener('click', () => toggleCompare(btn.dataset.remove));
    });
  }

  function updateCardButtons() {
    cards.forEach(card => {
      const btn = card.querySelector('.btn-add-compare');
      const id = card.dataset.id;
      const isAdded = compareIds.includes(id);
      btn.classList.toggle('is-added', isAdded);
      btn.textContent = isAdded ? '比較を解除' : '比較に追加 ＋';
      btn.disabled = !isAdded && compareIds.length >= MAX_COMPARE;
      card.classList.toggle('is-added', isAdded);
    });
  }

  function toggleCompare(id) {
    if (compareIds.includes(id)) {
      compareIds = compareIds.filter(x => x !== id);
    } else {
      if (compareIds.length >= MAX_COMPARE) return;
      compareIds.push(id);
    }
    updateCardButtons();
    renderTray();
  }

  cards.forEach(card => {
    const btn = card.querySelector('.btn-add-compare');
    btn.addEventListener('click', (e) => {
      e.preventDefault();
      toggleCompare(card.dataset.id);
    });
  });

  priceMinSelect.addEventListener('change', () => {
    if (Number(priceMinSelect.value) > Number(priceMaxSelect.value)) {
      priceMaxSelect.value = priceMinSelect.value;
    }
    applyFilters();
  });
  priceMaxSelect.addEventListener('change', () => {
    if (Number(priceMaxSelect.value) < Number(priceMinSelect.value)) {
      priceMinSelect.value = priceMaxSelect.value;
    }
    applyFilters();
  });
  [startSelect, serviceSelect, twoPaxSelect].forEach(sel => {
    if (sel) sel.addEventListener('change', applyFilters);
  });
  checkInputs.forEach(cb => cb.addEventListener('change', applyFilters));

  resetBtn.addEventListener('click', () => {
    priceMinSelect.value = '15000';
    priceMaxSelect.value = '40000';
    if (startSelect) startSelect.value = 'all';
    serviceSelect.value = 'all';
    twoPaxSelect.value = 'all';
    checkInputs.forEach(cb => { cb.checked = false; });
    applyFilters();
  });

  applyFilters();
  updateCardButtons();
});
