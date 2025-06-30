// 全局变量
let map;
let heatmapLayer;
let playerCountHistory = [];
let currentPlayerCount = 21347891;

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

// 初始化页面
document.addEventListener('DOMContentLoaded', function() {
    initializePlayerCounter();
    initializeTimelineChart();
    initializeHeatmap();
    initializeSmoothScrolling();
    startRealTimeUpdates();
    
    // 获取用户位置并添加到热力图
    getUserLocationAndAddToMap();
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
                <strong>📍 你的位置</strong><br>
                ${userLocation.city}, ${userLocation.countryName}<br>
                <small>欢迎加入 ${ROBLOX_CONFIG.GAME_NAME} 社区！</small>
            </div>
        `);
        
        console.log('用户位置已添加到地图:', userLocation);
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
            console.log('获取到真实Roblox数据:', realData);
        } else {
            // 使用模拟数据作为备用
            const variation = Math.floor(Math.random() * 10000) - 5000;
            currentPlayerCount = Math.max(20000000, currentPlayerCount + variation);
            console.log('使用模拟数据');
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
        console.error('更新玩家数量失败:', error);
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
    console.warn('历史数据获取失败，使用模拟数据');
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
    console.warn('热力图数据获取失败，使用模拟数据');
    return globalPlayerData;
  }
}

// ====== 3. 初始化时间线图表（自动数据&loading/error） ======
let timelineChart;
async function initializeTimelineChart() {
  const ctx = document.getElementById('timeline-chart').getContext('2d');
  const loadingEl = document.createElement('div');
  loadingEl.textContent = '加载中...';
  loadingEl.style.textAlign = 'center';
  ctx.canvas.parentNode.appendChild(loadingEl);
  let history = [];
  try {
    history = await fetchPlayerHistory();
    loadingEl.remove();
  } catch {
    loadingEl.textContent = '加载失败，显示模拟数据';
    history = mockPlayerData.history;
  }
  timelineChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: history.map(item => item.date),
      datasets: [{
        label: '玩家数量',
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
                        return `玩家数量: ${context.parsed.y.toLocaleString()}`;
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
  loadingEl.textContent = '加载中...';
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
    loadingEl.textContent = '加载失败，显示模拟数据';
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
            活跃玩家: ${Math.floor(point.intensity * 1000000).toLocaleString()}
        </div>
    `);
  });
  
  // 更新地图统计
  updateMapStats();
}

// 获取国家名称
function getCountryName(countryCode) {
    const countries = {
        'US': '美国', 'GB': '英国', 'FR': '法国', 'JP': '日本',
        'CN': '中国', 'RU': '俄罗斯', 'AU': '澳大利亚', 'IN': '印度',
        'KR': '韩国', 'AE': '阿联酋', 'BR': '巴西', 'MX': '墨西哥',
        'IT': '意大利', 'DE': '德国', 'SE': '瑞典', 'NO': '挪威', 'FI': '芬兰'
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
        'US': '北美', 'CA': '北美', 'MX': '北美',
        'GB': '欧洲', 'FR': '欧洲', 'DE': '欧洲', 'IT': '欧洲', 'SE': '欧洲', 'NO': '欧洲', 'FI': '欧洲', 'RU': '欧洲',
        'JP': '亚洲', 'CN': '亚洲', 'KR': '亚洲', 'IN': '亚洲', 'AE': '亚洲',
        'AU': '大洋洲', 'BR': '南美'
    };
    return regions[countryCode] || '其他';
}

// 初始化平滑滚动
function initializeSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
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
        console.log('页面完全加载完成');
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
    console.error('页面错误:', e.error);
    // 可以在这里添加错误上报逻辑
});

// 添加性能监控
window.addEventListener('load', function() {
    // 页面加载性能监控
    if ('performance' in window) {
        const perfData = performance.getEntriesByType('navigation')[0];
        console.log('页面加载时间:', perfData.loadEventEnd - perfData.loadEventStart, 'ms');
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