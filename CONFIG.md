# 🔧 真实API配置指南

## 📋 配置步骤概览

1. **获取Roblox游戏信息** - 使用工具页面获取真实ID
2. **更新配置文件** - 修改script.js中的游戏ID
3. **测试API连接** - 验证数据获取是否正常
4. **部署上线** - 使用真实数据上线

---

## 🎮 第一步：获取Roblox游戏信息

### 方法一：使用内置工具（推荐）

1. **打开工具页面**
   ```bash
   # 在浏览器中打开
   http://localhost:8000/get-roblox-info.html
   ```

2. **输入游戏信息**
   - 粘贴游戏主页URL，例如：
     ```
     https://www.roblox.com/games/1234567890/Grow-a-Garden
     ```
   - 或者直接输入游戏ID：`1234567890`

3. **获取详细信息**
   - 点击"获取信息"按钮
   - 查看返回的游戏详细信息
   - 记录 `游戏ID` 和 `Universe ID`

### 方法二：手动获取

1. **访问游戏主页**
   - 打开 [Roblox Games](https://www.roblox.com/games/)
   - 搜索目标游戏（如 "Grow a Garden"）
   - 点击进入游戏主页

2. **从URL获取游戏ID**
   - 游戏主页URL格式：`https://www.roblox.com/games/1234567890/Game-Name`
   - 其中 `1234567890` 就是游戏ID（placeId）

3. **获取Universe ID**
   - 按F12打开开发者工具
   - 切换到Network标签页
   - 刷新页面
   - 找到API请求，查看响应中的 `universeId`

---

## ⚙️ 第二步：更新配置文件

### 修改 script.js 中的配置

找到 `script.js` 文件中的 `ROBLOX_CONFIG` 部分：

```javascript
const ROBLOX_CONFIG = {
    // 示例：Grow a Garden 游戏ID（需要替换为真实ID）
    GAME_ID: 1234567890, // 请替换为真实的游戏ID
    UNIVERSE_ID: 1234567890, // 请替换为真实的universe ID
    GAME_NAME: 'Grow a Garden'
};
```

**替换为你的真实数据：**

```javascript
const ROBLOX_CONFIG = {
    GAME_ID: 你的游戏ID,           // 例如：1234567890
    UNIVERSE_ID: 你的UniverseID,   // 例如：9876543210
    GAME_NAME: '你的游戏名称'       // 例如：'Grow a Garden'
};
```

### 示例配置

假设你获取到的信息是：
- 游戏ID：`1234567890`
- Universe ID：`9876543210`
- 游戏名称：`Grow a Garden`

那么配置应该是：

```javascript
const ROBLOX_CONFIG = {
    GAME_ID: 1234567890,
    UNIVERSE_ID: 9876543210,
    GAME_NAME: 'Grow a Garden'
};
```

---

## 🧪 第三步：测试API连接

### 本地测试

1. **启动本地服务器**
   ```bash
   python -m http.server 8000
   ```

2. **打开浏览器开发者工具**
   - 按F12打开开发者工具
   - 切换到Console标签页

3. **检查API调用**
   - 刷新页面
   - 查看Console中的日志信息
   - 应该看到类似以下信息：
     ```
     获取到真实Roblox数据: {count: 12345, name: "Grow a Garden", ...}
     ```

### 常见问题排查

#### 问题1：API调用失败
```
Roblox API调用失败: TypeError: Failed to fetch
```

**解决方案：**
- 检查网络连接
- 确认游戏ID和Universe ID正确
- 检查Roblox API是否可访问

#### 问题2：返回数据为空
```
使用模拟数据
```

**解决方案：**
- 确认游戏ID存在且有效
- 检查游戏是否仍在运行
- 尝试使用不同的游戏ID

#### 问题3：CORS错误
```
Access to fetch at 'https://games.roblox.com/...' from origin '...' has been blocked by CORS policy
```

**解决方案：**
- 使用Netlify Functions代理（见下文）
- 或使用服务器端代理

---

## 🚀 第四步：部署上线

### 使用Netlify Functions代理（推荐）

为了避免CORS问题，建议使用Netlify Functions：

1. **创建functions目录**
   ```bash
   mkdir functions
   ```

2. **创建代理函数**
   创建文件 `functions/roblox-api.js`：

   ```javascript
   exports.handler = async function(event, context) {
     const { universeId } = JSON.parse(event.body || '{}');
     
     try {
       const response = await fetch(`https://games.roblox.com/v1/games?universeIds=${universeId}`);
       const data = await response.json();
       
       return {
         statusCode: 200,
         headers: {
           'Content-Type': 'application/json',
           'Access-Control-Allow-Origin': '*'
         },
         body: JSON.stringify(data)
       };
     } catch (error) {
       return {
         statusCode: 500,
         body: JSON.stringify({ error: 'API调用失败' })
       };
     }
   };
   ```

3. **更新前端代码**
   修改 `script.js` 中的API调用：

   ```javascript
   async function fetchRealRobloxPlayerCount() {
     try {
       const response = await fetch('/.netlify/functions/roblox-api', {
         method: 'POST',
         headers: {
           'Content-Type': 'application/json'
         },
         body: JSON.stringify({
           universeId: ROBLOX_CONFIG.UNIVERSE_ID
         })
       });
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
   ```

### 直接部署（简单方式）

如果不想使用代理，可以直接部署：

1. **上传到Netlify**
   - 访问 [Netlify Drop](https://app.netlify.com/drop)
   - 拖拽项目文件夹

2. **测试部署结果**
   - 访问生成的URL
   - 检查Console中的API调用情况

---

## 📊 第五步：监控和维护

### 监控API状态

1. **定期检查API可用性**
   - 每天检查一次API调用是否正常
   - 监控错误日志

2. **备用方案**
   - 当API不可用时，自动切换到模拟数据
   - 显示友好的错误提示

### 性能优化

1. **缓存策略**
   - 缓存API响应数据
   - 减少API调用频率

2. **错误处理**
   - 优雅处理API错误
   - 提供备用数据源

---

## 🔍 常见游戏ID示例

| 游戏名称 | 游戏ID | Universe ID | 备注 |
|---------|--------|-------------|------|
| Adopt Me | 920587237 | 2534724876 | 热门宠物游戏 |
| Blox Fruits | 2753915549 | 3956818381 | 海贼王主题 |
| Brookhaven RP | 4924922222 | 5599458645 | 角色扮演 |
| Grow a Garden | 待确认 | 待确认 | 需要查找 |

---

## 🆘 故障排除

### 获取不到游戏信息？

1. **检查游戏是否存在**
   - 确认游戏名称拼写正确
   - 检查游戏是否已被删除或改名

2. **使用替代方法**
   - 尝试搜索游戏的其他名称
   - 使用游戏分类页面查找

### API返回错误？

1. **检查配置**
   - 确认游戏ID和Universe ID正确
   - 检查网络连接

2. **使用备用方案**
   - 暂时使用模拟数据
   - 联系技术支持

---

## 📞 技术支持

如果遇到问题，可以：

1. **查看Console错误信息**
2. **检查网络连接**
3. **验证游戏ID有效性**
4. **使用备用数据源**

---

**🎯 完成配置后，你的网站就能显示真实的Roblox游戏数据了！** 