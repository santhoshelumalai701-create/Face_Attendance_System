@echo off
title Face Attendance Setup

echo ==========================
echo Checking Python...
echo ==========================

python --version
if %errorlevel% neq 0 (
    echo Python NOT FOUND! Install Python first.
    pause
    exit
)

echo.
echo ==========================
echo Upgrading pip...
echo ==========================
python -m pip install --upgrade pip

echo.
echo ==========================
echo Installing packages...
echo ==========================
python -m pip install opencv-python
python -m pip install deepface
python -m pip install pandas numpy tensorflow

echo.
echo ==========================
echo Testing installs...
echo ==========================
python -c "import cv2; print('OpenCV OK')"
python -c "from deepface import DeepFace; print('DeepFace OK')"

echo.
echo ==========================
echo SETUP COMPLETE
echo ==========================
pause