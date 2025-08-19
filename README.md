# 🌱 Grow a Garden Calculator

一个多语言的Roblox游戏计算器网站，提供水果价值计算、变异倍数计算和游戏策略指导。

## 🚀 项目特性

- **多语言支持**: 支持12种语言（英语、中文、西班牙语、葡萄牙语、法语、德语、俄语、阿拉伯语、印地语、印尼语、越南语、日语）
- **响应式设计**: 适配各种设备尺寸
- **SEO优化**: 完整的meta标签、结构化数据和sitemap
- **性能优化**: 模块化CSS、图片懒加载、缓存控制
- **错误处理**: 专业的404和500错误页面

## 📁 项目结构

```
Grow a Garden/
├── css/                    # 模块化CSS文件
│   ├── base.css           # 基础样式
│   ├── components.css     # 组件样式
│   ├── language-switcher.css # 语言切换器样式
│   ├── error-pages.css    # 错误页面样式
│   └── main.css           # 主样式文件（引用所有模块）
├── en/                    # 英文版本
│   ├── index.html         # 英文首页
│   ├── guides.html        # 英文指南
│   ├── game.html          # 英文游戏页面
│   └── ...                # 其他英文页面
├── zh-cn/                 # 中文版本
│   ├── index.html         # 中文首页
│   ├── guides.html        # 中文指南
│   └── ...                # 其他中文页面
├── [其他语言目录]/         # 其他语言版本
├── index.html             # 根目录重定向页面
├── sitemap.xml            # XML网站地图
├── sitemap.html           # HTML网站地图
├── robots.txt             # 搜索引擎爬虫配置
├── .htaccess              # Apache服务器配置
├── flag-switcher.js       # 语言切换器JavaScript
├── script.js              # 主要JavaScript功能
└── README.md              # 项目说明文档
```

## 🛠️ 技术栈

- **前端**: HTML5, CSS3, JavaScript (ES6+)
- **样式**: 模块化CSS、CSS变量、Flexbox/Grid布局
- **服务器**: Apache (.htaccess配置)
- **SEO**: 结构化数据、hreflang标签、sitemap
- **性能**: 图片优化、缓存控制、代码压缩

## 🔧 安装和部署

### 本地开发

1. 克隆项目到本地
2. 使用本地服务器（如XAMPP、WAMP等）
3. 确保Apache mod_rewrite模块已启用

### 生产部署

1. 上传所有文件到服务器
2. 确保.htaccess文件正常工作
3. 配置域名和SSL证书
4. 提交sitemap到Google Search Console

## 🌐 多语言支持

### 支持的语言

| 语言 | 代码 | 目录 | 状态 |
|------|------|------|------|
| 英语 | en | /en/ | ✅ 完整 |
| 中文 | zh-cn | /zh-cn/ | ✅ 完整 |
| 西班牙语 | es | /es/ | 🔄 部分 |
| 葡萄牙语 | pt-br | /pt-br/ | 🔄 部分 |
| 法语 | fr | /fr/ | 🔄 部分 |
| 德语 | de | /de/ | 🔄 部分 |
| 俄语 | ru | /ru/ | 🔄 部分 |
| 阿拉伯语 | ar | /ar/ | 🔄 部分 |
| 印地语 | hi | /hi/ | 🔄 部分 |
| 印尼语 | id | /id/ | 🔄 部分 |
| 越南语 | vi | /vi/ | 🔄 部分 |
| 日语 | ja | /ja/ | 🔄 部分 |

### 语言切换机制

- 基于Accept-Language头的自动重定向
- 国旗图标语言切换器
- 正确的hreflang标签配置
- 语言特定的URL结构

## 📱 响应式设计

- **桌面端**: 1200px+ 完整功能
- **平板端**: 768px-1199px 优化布局
- **手机端**: 320px-767px 移动优先设计

## 🚀 性能优化

### CSS优化
- 模块化CSS文件结构
- CSS变量减少重复
- 响应式设计优化
- 关键CSS内联

### JavaScript优化
- 模块化代码结构
- 事件委托优化
- 懒加载实现
- 代码分割

### 服务器优化
- Gzip压缩
- 浏览器缓存
- 静态资源CDN
- 错误页面处理

## 🔍 SEO优化

### 技术SEO
- 语义化HTML结构
- 结构化数据标记
- XML和HTML网站地图
- robots.txt配置

### 内容SEO
- 多语言内容本地化
- 关键词优化
- 内部链接结构
- 页面加载速度

## 🐛 故障排除

### 常见问题

1. **语言切换不工作**
   - 检查flag-switcher.js是否正确加载
   - 验证语言目录结构

2. **样式显示异常**
   - 确认CSS文件路径正确
   - 检查浏览器兼容性

3. **重定向循环**
   - 检查.htaccess配置
   - 验证hreflang标签

### 调试工具

- 浏览器开发者工具
- Google Search Console
- PageSpeed Insights
- 移动端友好性测试

## 📈 维护和更新

### 定期任务
- 更新游戏数据
- 检查链接有效性
- 优化页面性能
- 更新多语言内容

### 版本控制
- 使用Git进行版本管理
- 定期备份重要文件
- 记录重要更改

## 🤝 贡献指南

1. Fork项目
2. 创建功能分支
3. 提交更改
4. 发起Pull Request

## 📄 许可证

本项目采用MIT许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 📞 联系方式

- 项目主页: [网站URL]
- 问题反馈: [GitHub Issues]
- 邮箱: [联系邮箱]

---

**注意**: 这是一个持续开发的项目，功能和内容会定期更新。请关注最新版本获取最佳体验。 