// 立即防止自动滚动
preventAutoScroll();

// 完整的变异数据
const mutations = [
  // 普通变异
  { key: "rainbow", name: "Rainbow", multiplier: 50, admin: false, desc: "Obtained from fruit growth or butterfly event" },
  { key: "gold", name: "Gold", multiplier: 20, admin: false, desc: "Obtained from fruit growth or dragonfly event" },
  { key: "wet", name: "Wet", multiplier: 2, admin: false, desc: "Rainy weather or pet" },
  { key: "chilled", name: "Chilled", multiplier: 2, admin: false, desc: "Snowy weather or spray" },
  { key: "frozen", name: "Frozen", multiplier: 10, admin: false, desc: "Wet + Frozen" },
  { key: "choc", name: "Choc", multiplier: 2, admin: false, desc: "Spray/Sprinkler" },
  { key: "moonlit", name: "Moonlit", multiplier: 2, admin: false, desc: "Night event" },
  { key: "bloodlit", name: "Bloodlit", multiplier: 4, admin: false, desc: "Blood moon event" },
  { key: "windstruck", name: "Windstruck", multiplier: 2, admin: false, desc: "Wind event or pterosaur" },
  { key: "twisted", name: "Twisted", multiplier: 5, admin: false, desc: "Tornado event or pterosaur" },
  { key: "sandy", name: "Sandy", multiplier: 3, admin: false, desc: "Sandstorm weather" },
  { key: "clay", name: "Clay", multiplier: 5, admin: false, desc: "Wet + Sandy" },
  { key: "pollinated", name: "Pollinated", multiplier: 3, admin: false, desc: "Bee swarm/bee" },
  { key: "honeyglazed", name: "Honeyglazed", multiplier: 5, admin: false, desc: "Honey sprinkler/bumblebee" },
  { key: "drenched", name: "Drenched", multiplier: 5, admin: false, desc: "Tropical rain weather" },
  { key: "cloudtouched", name: "Cloudtouched", multiplier: 5, admin: false, desc: "Hyacinth parrot or spray" },
  { key: "amber", name: "Amber", multiplier: 10, admin: false, desc: "Raptor or amber spray" },
  { key: "oldamber", name: "OldAmber", multiplier: 20, admin: false, desc: "Let amber age" },
  { key: "ancientamber", name: "AncientAmber", multiplier: 50, admin: false, desc: "Let old amber continue to age" },
  { key: "friendbound", name: "Friendbound", multiplier: 70, admin: false, desc: "W.I.P" },
  { key: "tempestous", name: "Tempestous", multiplier: 12, admin: false, desc: "Wind + Twisted" },
  
  // 管理员变异
  { key: "shocked", name: "Shocked", multiplier: 100, admin: true, desc: "Thunderstorm/special event" },
  { key: "disco", name: "Disco", multiplier: 125, admin: true, desc: "Disco admin event" },
  { key: "celestial", name: "Celestial", multiplier: 120, admin: true, desc: "Meteor shower event" },
  { key: "zombified", name: "Zombified", multiplier: 25, admin: true, desc: "Zombie chicken passive" },
  { key: "plasma", name: "Plasma", multiplier: 5, admin: true, desc: "Admin laser event" },
  { key: "voidtouched", name: "Void Touched", multiplier: 135, admin: true, desc: "Admin black hole event" },
  { key: "burnt", name: "Burnt", multiplier: 4, admin: true, desc: "Roasted owl pet or spray" },
  { key: "molten", name: "Molten", multiplier: 25, admin: true, desc: "Admin volcano event" },
  { key: "meteoric", name: "Meteoric", multiplier: 125, admin: true, desc: "Meteor impact event" },
  { key: "heavenly", name: "Heavenly", multiplier: 5, admin: true, desc: "Jandel admin event" },
  { key: "sundried", name: "Sundried", multiplier: 85, admin: true, desc: "Heatwave weather" },
  { key: "verdant", name: "Verdant", multiplier: 4, admin: true, desc: "Scarlet macaw" },
  { key: "paradisal", name: "Paradisal", multiplier: 100, admin: true, desc: "Sundried + Verdant" },
  { key: "galactic", name: "Galactic", multiplier: 120, admin: true, desc: "Admin event" },
  { key: "aurora", name: "Aurora", multiplier: 90, admin: true, desc: "Aurora weather" },
  { key: "alienlike", name: "Alienlike", multiplier: 100, admin: true, desc: "Alien admin event" },
  { key: "fried", name: "Fried", multiplier: 8, admin: true, desc: "Fried rain admin event" },
  { key: "cooked", name: "Cooked", multiplier: 10, admin: true, desc: "Roasted owl" },
  { key: "ceramic", name: "Ceramic", multiplier: 30, admin: true, desc: "Clay + Roasted/Sundried" },
  { key: "dawnbound", name: "Dawnbound", multiplier: 150, admin: true, desc: "Sun god event, hold 4 sunflowers" },
  { key: "infected", name: "Infected", multiplier: 75, admin: true, desc: "Zombie admin mutation" }
];

// 分类数据
const categories = [
  { key: "all", name: "All" },
  { key: "BaseValue", name: "BaseValue" },
  { key: "Exotic Seed Pack", name: "Exotic Seed Pack" },
  { key: "Prehistoric Event", name: "Prehistoric Event" },
  { key: "Event Seed Pack", name: "Event Seed Pack" }
];

// 全局变量
let map;
let heatmapLayer;
let playerCountHistory = [];
let currentPlayerCount = 21347891;
let selectedPlant = plants[0];
let selectedMutations = [];
let plantHistory = [];
let hideAdminMutations = false;
let mutationSortBy = 'value'; // 'value' or 'alphabetical'

// Roblox 游戏配置 - 已根据实际信息修正
const ROBLOX_CONFIG = {
    GAME_ID: 126884695634066,      // 游戏ID (placeId)
    UNIVERSE_ID: 7436755782,      // universeId
    GAME_NAME: 'Grow a Garden'    // 游戏名称
};

// 模拟的玩家数据（作为备用数据）
const mockPlayerData = {
    current: 21347891,
    trend: 1234,
    history: [
        { date: '2024-01-10', count: 15000000 },
        { date: '2024-01-11', count: 16500000 },
        { date: '2024-01-12', count: 17800000 },
        { date: '2024-01-13', count: 18234567 },
        { date: '2024-01-14', count: 19876543 },
        { date: '2024-01-15', count: 21347891 }
    ]
};

// 全球玩家分布数据（模拟）
const globalPlayerData = [
    { lat: 40.7128, lng: -74.0060, intensity: 0.9, country: 'US' }, // 纽约
    { lat: 34.0522, lng: -118.2437, intensity: 0.8, country: 'US' }, // 洛杉矶
    { lat: 51.5074, lng: -0.1278, intensity: 0.7, country: 'GB' }, // 伦敦
    { lat: 48.8566, lng: 2.3522, intensity: 0.6, country: 'FR' }, // 巴黎
    { lat: 35.6762, lng: 139.6503, intensity: 0.8, country: 'JP' }, // 东京
    { lat: 39.9042, lng: 116.4074, intensity: 0.7, country: 'CN' }, // 北京
    { lat: 37.7749, lng: -122.4194, intensity: 0.6, country: 'US' }, // 旧金山
    { lat: 55.7558, lng: 37.6176, intensity: 0.5, country: 'RU' }, // 莫斯科
    { lat: -33.8688, lng: 151.2093, intensity: 0.4, country: 'AU' }, // 悉尼
    { lat: 19.0760, lng: 72.8777, intensity: 0.5, country: 'IN' }, // 孟买
    { lat: 23.1291, lng: 113.2644, intensity: 0.6, country: 'CN' }, // 广州
    { lat: 37.5665, lng: 126.9780, intensity: 0.7, country: 'KR' }, // 首尔
    { lat: 25.2048, lng: 55.2708, intensity: 0.3, country: 'AE' }, // 迪拜
    { lat: -23.5505, lng: -46.6333, intensity: 0.4, country: 'BR' }, // 圣保罗
    { lat: 19.4326, lng: -99.1332, intensity: 0.5, country: 'MX' }, // 墨西哥城
    { lat: 41.9028, lng: 12.4964, intensity: 0.4, country: 'IT' }, // 罗马
    { lat: 52.5200, lng: 13.4050, intensity: 0.5, country: 'DE' }, // 柏林
    { lat: 59.3293, lng: 18.0686, intensity: 0.3, country: 'SE' }, // 斯德哥尔摩
    { lat: 59.9139, lng: 10.7522, intensity: 0.3, country: 'NO' }, // 奥斯陆
    { lat: 60.1699, lng: 24.9384, intensity: 0.3, country: 'FI' } // 赫尔辛基
];

// 加载植物图片映射
let plantImgMap = {};
fetch('plant_img_map_final.json')
  .then(res => res.json())
  .then(data => {
    plantImgMap = data;
    renderPlants(); // 图片映射加载后渲染
  });

// 渲染作物列表
function renderPlants(category = 'all', searchTerm = '') {
  const plantList = document.getElementById('plant-list');
  let filteredPlants = plants;
  
  // 按分类筛选
  if (category !== 'all') {
    filteredPlants = plants.filter(plant => plant.category === category);
  }
  
  // 按搜索词筛选
  if (searchTerm) {
    filteredPlants = filteredPlants.filter(plant => 
      plant.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }
  
  plantList.innerHTML = filteredPlants.map(plant => `
    <div class="plant-item ${selectedPlant.key === plant.key ? 'selected' : ''}" data-plant="${plant.key}">
      <div class="plant-icon">
        <img src="${plantImgMap[plant.key] || 'https://your-cdn.com/default-plant.png'}" alt="${plant.name}" style="width:32px;height:32px;object-fit:contain;">
      </div>
      <span>${plant.name}</span>
      <div class="plant-value">$${plant.value}</div>
    </div>
  `).join('');
  
  // 添加点击事件
  document.querySelectorAll('.plant-item').forEach(item => {
    item.addEventListener('click', function() {
      const plantKey = this.dataset.plant;
      selectedPlant = plants.find(p => p.key === plantKey);
      
      // 更新选中状态
      document.querySelectorAll('.plant-item').forEach(i => i.classList.remove('selected'));
      this.classList.add('selected');
      
      // 重新计算
      calculateValue();
    });
  });
}

// 渲染变异列表
function renderMutations(searchTerm = '') {
  const mutationList = document.getElementById('mutation-list');
  let filteredMutations = mutations;
  
  // 隐藏管理员变异
  if (hideAdminMutations) {
    filteredMutations = mutations.filter(m => !m.admin);
  }
  
  // 按搜索词筛选
  if (searchTerm) {
    filteredMutations = filteredMutations.filter(m => 
      m.name.toLowerCase().includes(searchTerm.toLowerCase())
    );
  }
  
  // 排序
  if (mutationSortBy === 'value') {
    filteredMutations.sort((a, b) => b.multiplier - a.multiplier);
  } else {
    filteredMutations.sort((a, b) => a.name.localeCompare(b.name));
  }
  
  mutationList.innerHTML = filteredMutations.map(mutation => `
    <button class="mutation-chip ${selectedMutations.includes(mutation.key) ? 'selected' : ''} ${mutation.admin ? 'admin' : ''}" 
            data-key="${mutation.key}" 
            title="${mutation.desc}">
      ${mutation.name} (${mutation.multiplier}x)
    </button>
  `).join('');
  
  // 添加点击事件
  document.querySelectorAll('.mutation-chip').forEach(btn => {
    btn.addEventListener('click', function() {
      const key = this.dataset.key;
      const index = selectedMutations.indexOf(key);
      
      if (index > -1) {
        selectedMutations.splice(index, 1);
        this.classList.remove('selected');
      } else {
        selectedMutations.push(key);
        this.classList.add('selected');
      }
      
      // 重新计算
      calculateValue();
    });
  });
}

// 计算价值
function calculateValue() {
  const weight = parseFloat(document.getElementById('crop-weight').value) || 0;
  const amount = parseInt(document.getElementById('crop-amount').value) || 1;
  const friendBoost = parseInt(document.getElementById('friend-boost').value) || 0;
  
  // 基础价值
  let baseValue = selectedPlant.value * weight * amount;
  
  // 变异倍率
  let multiplier = 1;
  selectedMutations.forEach(key => {
    const mutation = mutations.find(m => m.key === key);
    if (mutation) {
      multiplier *= mutation.multiplier;
    }
  });
  
  // 好友加成
  const friendMultiplier = 1 + (friendBoost / 100);
  
  // 总价值
  const totalValue = baseValue * multiplier * friendMultiplier;
  
  // 显示结果
  const resultElement = document.getElementById('calc-result');
  const unitElement = document.getElementById('calc-result-unit');
  
  if (totalValue >= 1000000) {
    resultElement.textContent = `$${(totalValue / 1000000).toFixed(3)} Million`;
    unitElement.textContent = `(${(totalValue / 1000000).toFixed(3)} Million)`;
  } else if (totalValue >= 1000) {
    resultElement.textContent = `$${(totalValue / 1000).toFixed(3)} Thousand`;
    unitElement.textContent = `(${(totalValue / 1000).toFixed(3)} Thousand)`;
  } else {
    resultElement.textContent = `$${totalValue.toFixed(2)}`;
    unitElement.textContent = '';
  }
}

// 反向计算重量
function calculateWeight() {
  const targetValue = parseFloat(document.getElementById('target-value').value) || 0;
  const amount = parseInt(document.getElementById('crop-amount').value) || 1;
  const friendBoost = parseInt(document.getElementById('friend-boost').value) || 0;
  
  // 变异倍率
  let multiplier = 1;
  selectedMutations.forEach(key => {
    const mutation = mutations.find(m => m.key === key);
    if (mutation) {
      multiplier *= mutation.multiplier;
    }
  });
  
  // 好友加成
  const friendMultiplier = 1 + (friendBoost / 100);
  
  // 计算所需重量
  const requiredWeight = targetValue / (selectedPlant.value * amount * multiplier * friendMultiplier);
  
  // 显示结果
  const weightResult = document.getElementById('weight-result');
  if (requiredWeight > 0) {
    weightResult.textContent = `≈${requiredWeight.toFixed(3)} kg`;
  } else {
    weightResult.textContent = `≈0 kg`;
  }
}

// 添加到历史记录
function addToHistory() {
  const weight = parseFloat(document.getElementById('crop-weight').value) || 0;
  const amount = parseInt(document.getElementById('crop-amount').value) || 1;
  const friendBoost = parseInt(document.getElementById('friend-boost').value) || 0;
  
  // 计算价值
  let baseValue = selectedPlant.value * weight * amount;
  let multiplier = 1;
  selectedMutations.forEach(key => {
    const mutation = mutations.find(m => m.key === key);
    if (mutation) {
      multiplier *= mutation.multiplier;
    }
  });
  const friendMultiplier = 1 + (friendBoost / 100);
  const totalValue = baseValue * multiplier * friendMultiplier;
  
  // 创建历史记录
  const historyItem = {
    id: Date.now(),
    plant: selectedPlant.name,
    mutations: selectedMutations.map(key => mutations.find(m => m.key === key).name).join(', '),
    weight: weight,
    amount: amount,
    friendBoost: friendBoost,
    value: totalValue
  };
  
  plantHistory.unshift(historyItem);
  renderHistory();
}

// 渲染历史记录
function renderHistory() {
  const historyList = document.getElementById('history-list');
  
  if (plantHistory.length === 0) {
    historyList.innerHTML = '<p style="text-align: center; color: #666;">No history yet</p>';
    return;
  }
  
  historyList.innerHTML = plantHistory.map(item => `
    <div class="history-item">
      <div class="history-info">
        <div class="history-plant">${item.plant}</div>
        <div class="history-mutations">${item.mutations || 'No mutations'}</div>
      </div>
      <div class="history-value">$${item.value.toFixed(2)}</div>
      <button class="history-delete" onclick="deleteHistory(${item.id})">×</button>
    </div>
  `).join('');
}

// 删除历史记录
function deleteHistory(id) {
  plantHistory = plantHistory.filter(item => item.id !== id);
  renderHistory();
}

// 清空变异
function clearMutations() {
  selectedMutations = [];
  renderMutations();
  calculateValue();
}

// 最大化变异
function maxMutations() {
  selectedMutations = mutations.filter(m => !m.admin || !hideAdminMutations).map(m => m.key);
  renderMutations();
  calculateValue();
}

// 切换模式
function toggleMode() {
  const reverseCalc = document.getElementById('reverse-calc');
  const isHidden = reverseCalc.style.display === 'none';
  reverseCalc.style.display = isHidden ? 'block' : 'none';
}

// 初始化计算器
function initializeCalculator() {
  // 渲染初始数据
  renderPlants();
  renderMutations();
  
  // 分类Tab事件
  document.querySelectorAll('.plant-tabs .tab').forEach(tab => {
    tab.addEventListener('click', function() {
      document.querySelectorAll('.plant-tabs .tab').forEach(t => t.classList.remove('active'));
      this.classList.add('active');
      renderPlants(this.dataset.category);
    });
  });
  
  // 作物搜索
  document.querySelector('.plant-search').addEventListener('input', function() {
    const activeTab = document.querySelector('.plant-tabs .tab.active');
    renderPlants(activeTab.dataset.category, this.value);
  });
  
  // 变异搜索
  document.querySelector('.mutation-search').addEventListener('input', function() {
    renderMutations(this.value);
  });
  
  // 变异排序
  document.querySelectorAll('.mutation-sort-btn').forEach(btn => {
    btn.addEventListener('click', function() {
      document.querySelectorAll('.mutation-sort-btn').forEach(b => b.classList.remove('active'));
      this.classList.add('active');
      mutationSortBy = this.dataset.sort;
      renderMutations();
    });
  });
  
  // 隐藏管理员变异
  document.getElementById('hide-admin-btn').addEventListener('click', function() {
    hideAdminMutations = !hideAdminMutations;
    const t = (window.__gagTranslate ? window.__gagTranslate : null);
    const showText = (t && t('mutation.showAdmin')) || 'Show Admin Mutations';
    const hideText = (t && t('mutation.hideAdmin')) || 'Hide Admin Mutations';
    this.textContent = hideAdminMutations ? showText : hideText;
    renderMutations();
  });
  
  // 输入变化事件
  document.getElementById('crop-weight').addEventListener('input', calculateValue);
  document.getElementById('crop-amount').addEventListener('input', calculateValue);
  document.getElementById('friend-boost').addEventListener('input', function() {
    document.getElementById('friend-boost-value').textContent = this.value + '%';
    calculateValue();
  });
  
  // 操作按钮事件
  document.getElementById('add-to-list').addEventListener('click', addToHistory);
  document.getElementById('clear-mutations').addEventListener('click', clearMutations);
  document.getElementById('max-mutations').addEventListener('click', maxMutations);
  document.getElementById('toggle-mode').addEventListener('click', toggleMode);
  
  // 反向计算
  document.getElementById('update-weight').addEventListener('click', calculateWeight);
  document.getElementById('target-value').addEventListener('input', calculateWeight);
  
  // 初始计算
  calculateValue();
  renderHistory();

  // 变异帮助按钮事件
  document.querySelector('.mutation-help-btn').addEventListener('click', function() {
    const t = (window.__gagTranslate ? window.__gagTranslate : null);
    const title = (t && t('mutation.helpTitle')) || 'How to get each mutation?';
    const closeText = (t && t('common.close')) || 'Close';
    let html = `<h3>${title}</h3><ul style="text-align:left;">`;
    mutations.forEach(m => {
      html += `<li><b>${m.name}</b>: ${m.desc}</li>`;
    });
    html += '</ul>';
    const modal = document.createElement('div');
    modal.style.position = 'fixed';
    modal.style.left = '0'; modal.style.top = '0'; modal.style.width = '100vw'; modal.style.height = '100vh';
    modal.style.background = 'rgba(0,0,0,0.4)';
    modal.style.zIndex = 99999;
    modal.innerHTML = `<div style=\"background:#fff;padding:2em 2em 1em 2em;max-width:500px;margin:5vh auto;border-radius:12px;box-shadow:0 8px 32px rgba(0,0,0,0.2);\">${html}<div style=\"text-align:right;\"><button id=\"close-mutation-help\" style=\"margin-top:1em;\">${closeText}</button></div></div>`;
    modal.addEventListener('click', e => { if (e.target.id === 'close-mutation-help' || e.target === modal) modal.remove(); });
    document.body.appendChild(modal);
  });
}

// 滚动控制函数
function scrollToSection(sectionId) {
  const section = document.getElementById(sectionId);
  if (section) {
    const headerHeight = 60; // 导航栏高度
    const sectionTop = section.offsetTop - headerHeight - 20; // 减去导航栏高度和额外间距
    
    window.scrollTo({
      top: sectionTop,
      behavior: 'smooth'
    });
  }
}

// 防止页面加载时自动滚动到锚点
function preventAutoScroll() {
  // 立即移除URL中的锚点
  if (window.location.hash) {
    const hash = window.location.hash;
    window.history.replaceState(null, null, window.location.pathname);
    
    // 如果需要滚动到特定section，使用我们的函数
    const sectionId = hash.substring(1);
    if (sectionId && sectionId !== '') {
      setTimeout(() => {
        scrollToSection(sectionId);
      }, 100);
    }
  }
  
  // 确保页面滚动到顶部
  window.scrollTo(0, 0);
  
  // 禁用所有可能导致自动滚动的行为
  document.addEventListener('DOMContentLoaded', function() {
    // 移除所有锚点链接的默认行为
    document.querySelectorAll('a[href^="#"]').forEach(link => {
      link.addEventListener('click', function(e) {
        e.preventDefault();
        const href = this.getAttribute('href');
        if (href && href !== '#') {
          const sectionId = href.substring(1);
          scrollToSection(sectionId);
        }
      });
    });
  });
  
  // 防止浏览器自动滚动到锚点
  if ('scrollRestoration' in history) {
    history.scrollRestoration = 'manual';
  }
}

// 页面加载时初始化
document.addEventListener('DOMContentLoaded', function() {
  // 防止自动滚动
  preventAutoScroll();
  
  // 初始化地图和统计功能
    initializePlayerCounter();
    initializeTimelineChart();
    initializeHeatmap();
    initializeSmoothScrolling();
  
  // 初始化计算器
  initializeCalculator();
  
  // 立即计算初始值
  calculateValue();
  
  // 开始实时更新
    startRealTimeUpdates();
});

// 获取真实的Roblox玩家数量
async function fetchRealRobloxPlayerCount() {
    try {
        // 使用Roblox官方API获取实时玩家数
        const response = await fetch(`https://games.roblox.com/v1/games?universeIds=${ROBLOX_CONFIG.UNIVERSE_ID}`);
        const data = await response.json();
        
        if (data.data && data.data.length > 0) {
            const gameData = data.data[0];
            return {
                count: gameData.playing || 0,
                name: gameData.name || ROBLOX_CONFIG.GAME_NAME,
                visits: gameData.visits || 0,
                favoritedCount: gameData.favoritedCount || 0
            };
        }
        return null;
    } catch (error) {
        console.error('Roblox API调用失败:', error);
        return null;
    }
}

// 获取用户IP位置
async function getUserLocation() {
    try {
        const response = await fetch('http://ip-api.com/json/?fields=countryCode,lat,lon,country,region,city');
        const location = await response.json();
        
        if (location.status === 'success') {
            return {
                lat: location.lat,
                lng: location.lon,
                country: location.countryCode,
                countryName: location.country,
                region: location.region,
                city: location.city
            };
        }
        return null;
    } catch (error) {
        console.error('IP定位失败:', error);
        return null;
    }
}

// 获取用户位置并添加到热力图
async function getUserLocationAndAddToMap() {
    const userLocation = await getUserLocation();
    if (userLocation && heatmapLayer) {
        // 添加用户位置到热力图
        const heatmapData = heatmapLayer.getLatLngs();
        heatmapData.push([userLocation.lat, userLocation.lng, 0.8]);
        heatmapLayer.setLatLngs(heatmapData);
        
        // 添加用户位置标记
        const userMarker = L.circleMarker([userLocation.lat, userLocation.lng], {
            radius: 12,
            fillColor: '#e74c3c',
            color: '#fff',
            weight: 3,
            opacity: 1,
            fillOpacity: 0.8
        }).addTo(map);
        
        userMarker.bindPopup(`
            <div style="text-align: center;">
                <strong>📍 Your Location</strong><br>
                ${userLocation.city}, ${userLocation.countryName}<br>
                <small>Welcome to the ${ROBLOX_CONFIG.GAME_NAME} community!</small>
            </div>
        `);
        
        console.log('User location added to map:', userLocation);
    }
}

// 初始化实时玩家计数器
async function initializePlayerCounter() {
    await updatePlayerCount();
    updateTrendIndicator();
}

// 更新玩家数量（使用真实API）
async function updatePlayerCount() {
    const playerCountElement = document.getElementById('player-count');
    const updateTimeElement = document.getElementById('update-time');
    
    try {
        // 尝试获取真实数据
        const realData = await fetchRealRobloxPlayerCount();
        
        if (realData && realData.count > 0) {
            // 使用真实数据
            currentPlayerCount = realData.count;
            console.log('Fetched real Roblox data:', realData);
        } else {
            // 使用模拟数据作为备用
            const variation = Math.floor(Math.random() * 10000) - 5000;
            currentPlayerCount = Math.max(20000000, currentPlayerCount + variation);
            console.log('Using mock data');
        }
        
        // 格式化数字显示
        const formattedCount = currentPlayerCount.toLocaleString();
        
        // 添加数字变化动画
        animateNumberChange(playerCountElement, formattedCount);
        
        // 更新时间
        updateTimeElement.textContent = new Date().toLocaleTimeString();
        
        // 记录历史数据
        playerCountHistory.push({
            time: new Date(),
            count: currentPlayerCount
        });
        
        // 保持最近100条记录
        if (playerCountHistory.length > 100) {
            playerCountHistory.shift();
        }
        
    } catch (error) {
        console.error('Failed to update player count:', error);
        // 出错时使用模拟数据
        const variation = Math.floor(Math.random() * 10000) - 5000;
        currentPlayerCount = Math.max(20000000, currentPlayerCount + variation);
        const formattedCount = currentPlayerCount.toLocaleString();
        animateNumberChange(playerCountElement, formattedCount);
        updateTimeElement.textContent = new Date().toLocaleTimeString();
    }
}

// 数字变化动画
function animateNumberChange(element, newValue) {
    const oldValue = parseInt(element.textContent.replace(/,/g, ''));
    const targetValue = parseInt(newValue.replace(/,/g, ''));
    
    if (oldValue === targetValue) return;
    
    const duration = 1000;
    const startTime = performance.now();
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = Math.floor(oldValue + (targetValue - oldValue) * progress);
        element.textContent = currentValue.toLocaleString();
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        }
    }
    
    requestAnimationFrame(updateNumber);
}

// 更新趋势指示器
function updateTrendIndicator() {
    const trendArrow = document.getElementById('trend-arrow');
    const trendText = document.getElementById('trend-text');
    
    // 基于历史数据计算真实趋势
    if (playerCountHistory.length >= 2) {
        const recent = playerCountHistory[playerCountHistory.length - 1].count;
        const previous = playerCountHistory[playerCountHistory.length - 2].count;
        const change = recent - previous;
        
        if (change > 0) {
            trendArrow.textContent = '↗';
            trendArrow.style.color = '#f1c40f';
            trendText.textContent = `+${change.toLocaleString()}`;
            trendText.style.color = '#f1c40f';
        } else if (change < 0) {
            trendArrow.textContent = '↘';
            trendArrow.style.color = '#e74c3c';
            trendText.textContent = `${change.toLocaleString()}`;
            trendText.style.color = '#e74c3c';
        } else {
            trendArrow.textContent = '→';
            trendArrow.style.color = '#95a5a6';
            trendText.textContent = '0';
            trendText.style.color = '#95a5a6';
        }
    } else {
        // 如果没有历史数据，使用模拟趋势
        const trend = Math.random() > 0.5 ? 1 : -1;
        const change = Math.floor(Math.random() * 5000) + 100;
        
        if (trend > 0) {
            trendArrow.textContent = '↗';
            trendArrow.style.color = '#f1c40f';
            trendText.textContent = `+${change.toLocaleString()}`;
            trendText.style.color = '#f1c40f';
        } else {
            trendArrow.textContent = '↘';
            trendArrow.style.color = '#e74c3c';
            trendText.textContent = `-${change.toLocaleString()}`;
            trendText.style.color = '#e74c3c';
        }
    }
}

// ====== 1. 玩家历史趋势数据自动拉取 ======
async function fetchPlayerHistory() {
  try {
    const res = await fetch('/api/player-history');
    if (!res.ok) throw new Error('Network error');
    return await res.json(); // [{date, count}, ...]
  } catch (e) {
    console.warn('Failed to fetch history data, using mock data');
    return mockPlayerData.history;
  }
}

// ====== 2. 全球热力地图数据自动拉取 ======
async function fetchPlayerHeatmap() {
  try {
    const res = await fetch('/api/player-heatmap');
    if (!res.ok) throw new Error('Network error');
    return await res.json(); // [{lat, lng, intensity, country}, ...]
  } catch (e) {
    console.warn('Failed to fetch heatmap data, using mock data');
    return globalPlayerData;
  }
}

// ====== 3. 初始化时间线图表（自动数据&loading/error） ======
let timelineChart;
async function initializeTimelineChart() {
  const ctx = document.getElementById('timeline-chart').getContext('2d');
  const loadingEl = document.createElement('div');
  loadingEl.textContent = 'Loading...';
  loadingEl.style.textAlign = 'center';
  ctx.canvas.parentNode.appendChild(loadingEl);
  let history = [];
  try {
    history = await fetchPlayerHistory();
    loadingEl.remove();
  } catch {
    loadingEl.textContent = 'Failed to load, showing mock data';
    history = mockPlayerData.history;
  }
  timelineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: history.map(item => item.date),
      datasets: [{
        label: 'Player Count',
        data: history.map(item => item.count),
        borderColor: '#2ecc71',
        backgroundColor: 'rgba(46, 204, 113, 0.1)',
        borderWidth: 3,
        fill: true,
        tension: 0.4,
        pointBackgroundColor: '#2ecc71',
        pointBorderColor: '#fff',
        pointBorderWidth: 2,
        pointRadius: 6,
        pointHoverRadius: 8
      }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                display: false
            },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                titleColor: '#fff',
                bodyColor: '#fff',
                borderColor: '#2ecc71',
                borderWidth: 1,
                cornerRadius: 8,
                displayColors: false,
                callbacks: {
                    label: function(context) {
                        return `Player Count: ${context.parsed.y.toLocaleString()}`;
                    }
                }
            }
        },
        scales: {
            x: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                },
                ticks: {
                    color: '#7f8c8d'
                }
            },
            y: {
                grid: {
                    color: 'rgba(0, 0, 0, 0.1)'
                },
                ticks: {
                    color: '#7f8c8d',
                    callback: function(value) {
                        return (value / 1000000).toFixed(1) + 'M';
                    }
                }
            }
        },
        interaction: {
            intersect: false,
            mode: 'index'
        }
    }
  });
}

// ====== 4. 初始化热力地图（自动数据&loading/error） ======
async function initializeHeatmap() {
  map = L.map('heatmap').setView([20, 0], 2);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '© OpenStreetMap contributors'
  }).addTo(map);
  const loadingEl = document.createElement('div');
  loadingEl.textContent = 'Loading...';
  loadingEl.style.position = 'absolute';
  loadingEl.style.left = '50%';
  loadingEl.style.top = '50%';
  loadingEl.style.transform = 'translate(-50%,-50%)';
  loadingEl.style.background = 'rgba(255,255,255,0.8)';
  loadingEl.style.padding = '1rem 2rem';
  loadingEl.style.borderRadius = '1rem';
  loadingEl.style.zIndex = 10;
  document.getElementById('heatmap').appendChild(loadingEl);
  let heatData = [];
  try {
    heatData = await fetchPlayerHeatmap();
    loadingEl.remove();
  } catch {
    loadingEl.textContent = 'Failed to load, showing mock data';
    heatData = globalPlayerData;
  }
  const heatmapData = heatData.map(point => [point.lat, point.lng, point.intensity]);
  heatmapLayer = L.heatLayer(heatmapData, {
    radius: 25,
    blur: 15,
    maxZoom: 10,
    gradient: {
      0.4: '#2ecc71', 0.6: '#f1c40f', 0.8: '#e67e22', 1.0: '#e74c3c'
    }
  }).addTo(map);
  // 添加玩家分布标记
  heatData.forEach(point => {
    const marker = L.circleMarker([point.lat, point.lng], {
        radius: 8,
        fillColor: '#2ecc71',
        color: '#fff',
        weight: 2,
        opacity: 1,
        fillOpacity: 0.8
    }).addTo(map);
    
    marker.bindPopup(`
        <div style="text-align: center;">
            <strong>${getCountryName(point.country)}</strong><br>
            Active Players: ${Math.floor(point.intensity * 1000000).toLocaleString()}
        </div>
    `);
  });
  
  // 更新地图统计
  updateMapStats();
}

// 获取国家名称
function getCountryName(countryCode) {
    const countries = {
        'US': 'United States', 'GB': 'United Kingdom', 'FR': 'France', 'JP': 'Japan',
        'CN': 'China', 'RU': 'Russia', 'AU': 'Australia', 'IN': 'India',
        'KR': 'South Korea', 'AE': 'United Arab Emirates', 'BR': 'Brazil', 'MX': 'Mexico',
        'IT': 'Italy', 'DE': 'Germany', 'SE': 'Sweden', 'NO': 'Norway', 'FI': 'Finland'
    };
    return countries[countryCode] || countryCode;
}

// 更新地图统计
function updateMapStats() {
    const activeCountries = document.getElementById('active-countries');
    const topRegion = document.getElementById('top-region');
    
    // 计算活跃国家数量
    const uniqueCountries = new Set(globalPlayerData.map(point => point.country));
    activeCountries.textContent = uniqueCountries.size;
    
    // 计算最活跃地区
    const regionStats = {};
    globalPlayerData.forEach(point => {
        const region = getRegion(point.country);
        regionStats[region] = (regionStats[region] || 0) + point.intensity;
    });
    
    const topRegionName = Object.keys(regionStats).reduce((a, b) => 
        regionStats[a] > regionStats[b] ? a : b
    );
    topRegion.textContent = topRegionName;
}

// 获取地区名称
function getRegion(countryCode) {
    const regions = {
        'US': 'North America', 'CA': 'North America', 'MX': 'North America',
        'GB': 'Europe', 'FR': 'Europe', 'DE': 'Europe', 'IT': 'Europe', 'SE': 'Europe', 'NO': 'Europe', 'FI': 'Europe', 'RU': 'Europe',
        'JP': 'Asia', 'CN': 'Asia', 'KR': 'Asia', 'IN': 'Asia', 'AE': 'Asia',
        'AU': 'Oceania', 'BR': 'South America'
    };
    return regions[countryCode] || 'Other';
}

// 初始化平滑滚动
function initializeSmoothScrolling() {
    // 移除这个函数，因为我们已经用自定义的scrollToSection函数替代了
    // 这个函数会导致页面自动滚动到锚点
    console.log('Smooth scrolling disabled, using custom scroll function');
}

// ====== 5. 自动刷新所有数据 ======
function startRealTimeUpdates() {
  setInterval(updatePlayerCount, 30000);
  setInterval(updateTrendIndicator, 60000);
  setInterval(async () => {
    // 刷新趋势图
    if (timelineChart) {
      const history = await fetchPlayerHistory();
      timelineChart.data.labels = history.map(item => item.date);
      timelineChart.data.datasets[0].data = history.map(item => item.count);
      timelineChart.update();
    }
    // 刷新热力图
    if (heatmapLayer) {
      const heatData = await fetchPlayerHeatmap();
      heatmapLayer.setLatLngs(heatData.map(point => [point.lat, point.lng, point.intensity]));
    }
  }, 300000);
}

// 添加页面加载动画
window.addEventListener('load', function() {
    // 添加页面加载完成的动画效果
    document.body.classList.add('loaded');
    
    // 初始化一些延迟加载的元素
    setTimeout(() => {
        // 可以在这里添加一些延迟加载的功能
        console.log('Page fully loaded');
    }, 1000);
});

// 添加滚动动画
window.addEventListener('scroll', function() {
    const scrolled = window.pageYOffset;
    const parallax = document.querySelector('.hero');
    
    if (parallax) {
        const speed = scrolled * 0.5;
        parallax.style.transform = `translateY(${speed}px)`;
    }
});

// 添加键盘快捷键
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + R 刷新数据
    if ((e.ctrlKey || e.metaKey) && e.key === 'r') {
        e.preventDefault();
        updatePlayerCount();
        updateTrendIndicator();
    }
    
    // 空格键滚动到顶部
    if (e.key === ' ' && e.target === document.body) {
        e.preventDefault();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
});

// 添加错误处理
window.addEventListener('error', function(e) {
    console.error('Page error:', e.error);
    // 可以在这里添加错误上报逻辑
});

// 添加性能监控
window.addEventListener('load', function() {
    // 页面加载性能监控
    if ('performance' in window) {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log('Page load time:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
    }
});

// 导出一些函数供外部使用（如果需要）
window.GrowTracker = {
    updatePlayerCount,
    updateTrendIndicator,
    updateHeatmap,
    getCurrentPlayerCount: () => currentPlayerCount,
    fetchRealRobloxPlayerCount,
    getUserLocation
}; 

// 自动切换后核心区块收缩消失，Tracker区块自动顶到顶部
(function() {
  const hero = document.querySelector('.hero');
  const nextSection = document.querySelector('#stats-hero');
  if (!hero || !nextSection) return;

  let switched = false;
  hero.addEventListener('scroll', function () {
    if (switched) return;
    if (hero.scrollTop + hero.clientHeight >= hero.scrollHeight - 2) {
      switched = true;
      hero.classList.add('hide-after-scroll');
      setTimeout(() => {
        nextSection.scrollIntoView({ behavior: 'smooth' });
      }, 500); // 等动画收缩后再滚动
    }
  });
})(); 

// 攻略页面功能
(function() {
  // 检查是否在攻略页面
  if (!document.querySelector('.guides-section')) return;
  
  const searchInput = document.getElementById('guide-search');
  const filterButtons = document.querySelectorAll('.filter-btn');
  const guideItems = document.querySelectorAll('.guide-item');
  const categorySections = document.querySelectorAll('.category-section');
  
  // 搜索功能
  function filterGuides() {
    const searchTerm = searchInput.value.toLowerCase();
    const activeFilter = document.querySelector('.filter-btn.active').getAttribute('data-filter');
    
    guideItems.forEach(item => {
      const title = item.querySelector('h3').textContent.toLowerCase();
      const description = item.querySelector('p').textContent.toLowerCase();
      const category = item.closest('.category-section')?.getAttribute('data-category') || 'all';
      
      const matchesSearch = title.includes(searchTerm) || description.includes(searchTerm);
      const matchesFilter = activeFilter === 'all' || category === activeFilter;
      
      if (matchesSearch && matchesFilter) {
        item.style.display = 'block';
        item.style.animation = 'fadeIn 0.3s ease-in-out';
      } else {
        item.style.display = 'none';
      }
    });
    
    // 显示/隐藏分类标题
    categorySections.forEach(section => {
      const visibleItems = section.querySelectorAll('.guide-item[style*="block"]').length;
      const categoryTitle = section.querySelector('.category-title');
      
      if (visibleItems === 0) {
        if (categoryTitle) categoryTitle.style.display = 'none';
      } else {
        if (categoryTitle) categoryTitle.style.display = 'block';
      }
    });
  }
  
  // 筛选按钮点击事件
  filterButtons.forEach(button => {
    button.addEventListener('click', function() {
      // 移除所有active类
      filterButtons.forEach(btn => btn.classList.remove('active'));
      // 添加active类到当前按钮
      this.classList.add('active');
      // 执行筛选
      filterGuides();
    });
  });
  
  // 搜索输入事件
  if (searchInput) {
    searchInput.addEventListener('input', filterGuides);
    searchInput.addEventListener('keyup', function(e) {
      if (e.key === 'Enter') {
        // 可以在这里添加回车搜索的特殊处理
        console.log('Search submitted:', this.value);
      }
    });
  }
  
  // 添加淡入动画
  const style = document.createElement('style');
  style.textContent = `
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(10px); }
      to { opacity: 1; transform: translateY(0); }
    }
  `;
  document.head.appendChild(style);
  
  // 初始化
  filterGuides();
  
  // 添加点击统计（可选）
  guideItems.forEach(item => {
    item.addEventListener('click', function() {
      const title = this.querySelector('h3').textContent;
      console.log('Guide clicked:', title);
      // 这里可以添加统计代码
    });
  });
  
  // 添加键盘导航支持
  document.addEventListener('keydown', function(e) {
    if (e.target === searchInput) return;
    
    // Ctrl/Cmd + F 聚焦搜索框
    if ((e.ctrlKey || e.metaKey) && e.key === 'f') {
      e.preventDefault();
      searchInput.focus();
      searchInput.select();
    }
    
    // ESC 清空搜索
    if (e.key === 'Escape' && searchInput.value) {
      searchInput.value = '';
      filterGuides();
    }
  });
  
  console.log('Guides page functionality initialized');
})(); 