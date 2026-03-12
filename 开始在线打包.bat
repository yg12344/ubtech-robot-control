@echo off
chcp 65001 >nul
echo ========================================
echo    优必选小微机器人控制软件
echo    在线打包APK - 自动化脚本
echo ========================================
echo.

REM 检查是否已配置Git
git config user.name >nul 2>&1
if %errorlevel% neq 0 (
    echo [1/4] 首次使用，需要配置Git信息
    echo.
    set /p username=请输入你的GitHub用户名:
    set /p email=请输入你的邮箱地址:

    git config --global user.name "%username%"
    git config --global user.email "%email%"
    echo.
    echo ✓ Git配置完成
) else (
    echo [1/4] Git已配置
    echo.
)

echo [2/4] 初始化Git仓库...
if not exist .git (
    git init
    echo ✓ 仓库初始化完成
) else (
    echo ✓ 仓库已存在
)
echo.

echo [3/4] 添加并提交代码...
git add .
git commit -m "Initial commit - 优必选小微机器人控制软件" >nul 2>&1
if %errorlevel% neq 0 (
    echo ✓ 代码已提交
) else (
    echo ✓ 代码已提交
)
echo.

echo [4/4] 推送到GitHub...
echo.
echo ════════════════════════════════════════
echo  重要提示：
echo ════════════════════════════════════════
echo.
echo  在继续之前，请确保你已经：
echo  1. 在GitHub上创建了一个新仓库
echo  2. 仓库名称建议：ubtech-robot-control
echo.
echo ════════════════════════════════════════
echo.

set /p repo_url=请输入GitHub仓库URL (例如: https://github.com/用户名/ubtech-robot-control.git):

if "%repo_url%"=="" (
    echo.
    echo ❌ 未输入仓库URL，操作取消
    echo.
    echo 请手动执行以下命令：
    echo git remote add origin https://github.com/你的用户名/ubtech-robot-control.git
    echo git branch -M main
    echo git push -u origin main
    pause
    exit /b
)

echo.
echo 正在添加远程仓库...
git remote add origin %repo_url% 2>nul
if %errorlevel% neq 0 (
    git remote remove origin
    git remote add origin %repo_url%
)

echo 正在推送代码...
git branch -M main
git push -u origin main

if %errorlevel% neq 0 (
    echo.
    echo ❌ 推送失败！
    echo.
    echo 可能的原因：
    echo 1. 仓库URL输入错误
    echo 2. 需要身份验证（GitHub Personal Access Token）
    echo.
    echo 解决方法：
    echo 1. 检查仓库URL是否正确
    echo 2. 在GitHub Settings → Developer settings → Personal access tokens 创建Token
    echo 3. 推送时使用Token作为密码
    echo.
    echo 按任意键重试或手动执行推送命令...
    pause >nul
    git push -u origin main
)

if %errorlevel% equ 0 (
    echo.
    echo ========================================
    echo    ✓ 代码推送成功！
    echo ========================================
    echo.
    echo 🎉 GitHub Actions将自动开始打包APK
    echo.
    echo 下一步：
    echo 1. 访问你的GitHub仓库
    echo 2. 点击 Actions 标签
    echo 3. 查看打包进度（约30-60分钟）
    echo 4. 打包完成后下载APK
    echo.
    echo 详细说明请查看：在线打包步骤.md
    echo.
)

echo.
pause
