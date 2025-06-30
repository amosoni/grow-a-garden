@echo off
echo 🌱 Grow a Garden Tracker 部署脚本
echo ================================

echo.
echo 正在检查文件...
if not exist "index.html" (
    echo ❌ 错误: 找不到 index.html 文件
    pause
    exit /b 1
)

if not exist "styles.css" (
    echo ❌ 错误: 找不到 styles.css 文件
    pause
    exit /b 1
)

if not exist "script.js" (
    echo ❌ 错误: 找不到 script.js 文件
    pause
    exit /b 1
)

echo ✅ 所有必需文件检查完成

echo.
echo 🚀 准备部署到 Netlify...
echo.
echo 请按照以下步骤操作：
echo 1. 访问 https://app.netlify.com/drop
echo 2. 将当前文件夹拖拽到页面中
echo 3. 等待部署完成
echo 4. 复制生成的URL
echo.

echo 📁 当前项目文件：
dir /b *.html *.css *.js *.md *.toml

echo.
echo 💡 提示：
echo - 确保所有文件都在当前文件夹中
echo - 部署完成后可以自定义域名
echo - 支持自动HTTPS和CDN加速
echo.

pause 