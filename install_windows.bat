@echo off
echo Installing CTD Document Organizer for Windows...
echo ==============================================

REM Create virtual environment (if not already done)
python -m venv ctd_env
call ctd_env\Scripts\activate

REM Step 1: Install PyTorch first
echo Installing PyTorch...
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

REM Step 2: Install basic requirements
echo Installing basic dependencies...
pip install PyPDF2 pdfplumber numpy pandas colorama tqdm psutil

REM Step 3: Install transformers without problematic dependencies
echo Installing transformers...
pip install transformers==4.36.2 accelerate==0.25.0 sentence-transformers==2.2.2

REM Step 4: Install remaining packages
echo Installing additional packages...
pip install python-json-logger protobuf scikit-learn

echo.
echo ✅ Installation complete!
echo.
echo To use the organizer:
echo 1. Activate: ctd_env\Scripts\activate
echo 2. Add PDFs to: documents_to_organize folder
echo 3. Run: python organized_document.py
pause