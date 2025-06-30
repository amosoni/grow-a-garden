exports.handler = async function(event, context) {
  // 处理CORS预检请求
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 200,
      headers: {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Headers': 'Content-Type',
        'Access-Control-Allow-Methods': 'GET, POST, OPTIONS'
      },
      body: ''
    };
  }

  try {
    // 解析请求体
    const { universeId, gameId } = JSON.parse(event.body || '{}');
    
    if (!universeId && !gameId) {
      return {
        statusCode: 400,
        headers: {
          'Content-Type': 'application/json',
          'Access-Control-Allow-Origin': '*'
        },
        body: JSON.stringify({ 
          error: '缺少必要参数',
          message: '请提供 universeId 或 gameId'
        })
      };
    }

    // 构建API URL
    let apiUrl;
    if (universeId) {
      apiUrl = `https://games.roblox.com/v1/games?universeIds=${universeId}`;
    } else {
      apiUrl = `https://games.roblox.com/v1/games/multiget-place-details?placeIds=${gameId}`;
    }

    // 调用Roblox API
    const response = await fetch(apiUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
      }
    });

    if (!response.ok) {
      throw new Error(`Roblox API 返回错误: ${response.status}`);
    }

    const data = await response.json();

    // 返回成功响应
    return {
      statusCode: 200,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
        'Cache-Control': 'public, max-age=30' // 缓存30秒
      },
      body: JSON.stringify({
        success: true,
        data: data,
        timestamp: new Date().toISOString()
      })
    };

  } catch (error) {
    console.error('API代理错误:', error);

    return {
      statusCode: 500,
      headers: {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*'
      },
      body: JSON.stringify({
        success: false,
        error: 'API调用失败',
        message: error.message,
        timestamp: new Date().toISOString()
      })
    };
  }
}; 