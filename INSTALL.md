# Installation Guide
1. pip install pyinstaller
2. Navigate to the src/gui folder
3. Run in terminal: \
  pyinstaller --noconfirm \
  --windowed \
  --icon=x-ray.icns \
  tkinter_app.py
4. rm -rf build __pycache__ *.spec