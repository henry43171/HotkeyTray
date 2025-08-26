@echo off
echo Starting HotkeyTray build process...

REM 清除舊的建置檔案
echo Cleaning old build files...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist *.spec del /q *.spec

echo Old files cleaned.

REM 使用PyInstaller打包
echo Building executable...
pyinstaller ^
    --onefile ^
    --windowed ^
    --icon=src/assets/icon.ico ^
    --add-data "src/assets/icon.ico;assets" ^
    --add-data "config/config.json;config" ^
    --name HotkeyTray ^
    --distpath dist ^
    --workpath build ^
    src/__main__.py

REM 檢查建置結果
if exist dist/HotkeyTray.exe (
    echo.
    echo ✅ Build successful!
    echo Executable: dist/HotkeyTray.exe
    echo.
    echo Cleaning build artifacts...
    rmdir /s /q build
    del /q *.spec
    echo Build artifacts cleaned.
    echo.
    echo 🎉 HotkeyTray.exe is ready in the dist folder!
) else (
    echo.
    echo ❌ Build failed!
    echo Please check the error messages above.
)

pause
