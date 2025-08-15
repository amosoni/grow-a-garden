// 测试 Yandex Games SDK 可访问性
console.log('Testing Yandex Games SDK accessibility...');

// 测试SDK文件
const sdkUrl = 'https://games.s3.yandex.net/sdk/_/v2.c68e1234372250dd975a.js';

fetch(sdkUrl)
  .then(response => {
    if (response.ok) {
      console.log('✅ SDK file accessible:', response.status);
      return response.text();
    } else {
      console.log('❌ SDK file not accessible:', response.status);
      throw new Error('SDK not accessible');
    }
  })
  .then(content => {
    console.log('✅ SDK content loaded, size:', content.length, 'characters');
    console.log('SDK first 200 chars:', content.substring(0, 200));
  })
  .catch(error => {
    console.error('❌ SDK loading failed:', error.message);
  });

// 测试游戏主页面
const gameUrl = 'https://www.growagardenoffline.online/Ya_Prod/';

fetch(gameUrl)
  .then(response => {
    if (response.ok) {
      console.log('✅ Game page accessible:', response.status);
      return response.text();
    } else {
      console.log('❌ Game page not accessible:', response.status);
      throw new Error('Game page not accessible');
    }
  })
  .then(content => {
    console.log('✅ Game page loaded, size:', content.length, 'characters');
    console.log('Page first 200 chars:', content.substring(0, 200));
  })
  .catch(error => {
    console.error('❌ Game page loading failed:', error.message);
  });

// 测试网络连接
console.log('Testing network connectivity...');
console.log('User Agent:', navigator.userAgent);
console.log('Online status:', navigator.onLine);
console.log('Connection type:', navigator.connection ? navigator.connection.effectiveType : 'Unknown'); 