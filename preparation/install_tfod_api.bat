@echo off
setlocal EnableDelayedExpansion

IF "%1"=="" (
    echo No install path supplied
    exit 1
)
SET install_path=%1

IF "%2"=="" (
    SET protoc_download_link=https://github.com/protocolbuffers/protobuf/releases/download/v3.19.3/protoc-3.19.3-win64.zip
) ELSE (
    SET protoc_download_link=%2%
)

IF exist %install_path%\ (
    echo object_detection folder exists, no need to clone again
) ELSE (
    git clone "https://github.com/tensorflow/models" "%install_path%"
)

IF not exist %install_path%\research\ IF exist %install_path%\help\ goto tfod_installed
goto restructure_files

:tfod_installed
echo Most likely Tensorflow Object detection folders are already structured.
echo If not, please check the folder where TFOD API should be installed for errors
goto install_packages

:restructure_files
FOR /d %%a IN ("%install_path%\*") DO (
    IF /i not "%%~nxa"=="research" (
        RD /S /Q "%%a"
    )
)
RD /S /Q "%install_path%\.git\"

FOR %%a IN ("%install_path%\*") DO (
    DEL "%%a"
)
move "%install_path%\research\object_detection" "%install_path%\"
move "%install_path%\research\slim" "%install_path%\"
RD /S /Q  "%install_path%\research\"
mkdir "%install_path%\help"

:install_packages
cd %install_path%
:: obtain absolute path
set install_path=%cd%

cd %install_path%\help
powershell.exe -Command "Invoke-WebRequest -OutFile protoc.zip %protoc_download_link%"
tar -xf protoc.zip
cd %install_path%
.\help\bin\protoc.exe .\object_detection\protos\*.proto --python_out=.
@REM for %%a in ("%install_path%\object_detection\protos\*.proto") do %install_path%\help\bin\protoc.exe %install_path%\object_detection\protos\%%a --python_out=%install_path%

copy %install_path%\object_detection\packages\tf2\setup.py %install_path%\
cd %install_path%
python setup.py build
python setup.py install
cd %install_path%\slim
@REM python -m pip install .
pip install -e .

:: fix possible errors
pip install numpy
pip install wrapt
pip install opt_einsum
pip install gast
pip install astunparse
pip install termcolor
pip install tensorflow --upgrade
pip uninstall -y google
pip install google-cloud
pip uninstall -y protobuf
pip uninstall -y google
pip install google
pip install protobuf
pip install tensorflow-gpu --upgrade
pip install matplotlib
pip install pyyaml