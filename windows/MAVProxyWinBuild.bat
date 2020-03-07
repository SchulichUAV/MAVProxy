rem build the standalone MAVProxy.exe for Windows.
rem This assumes Python is installed in C:\Python36
rem   If it is not, change the PYTHON_LOCATION environment variable accordingly
rem This assumes InnoSetup is installed in C:\Program Files (x86)\Inno Setup 5
rem   If it is not, change the INNOSETUP environment variable accordingly
SETLOCAL enableextensions

if "%PYTHON_LOCATION%" == "" (set "PYTHON_LOCATION=C:\Program Files (x86)\Python37-32")
if "%INNOSETUP%" == "" (set "INNOSETUP=C:\Program Files (x86)\Inno Setup 6")

rem get the version
for /f "tokens=*" %%a in (
 '"%PYTHON_LOCATION%\python" returnVersion.py'
 ) do (
 set VERSION=%%a
 )

rem -----build the changelog-----
"%PYTHON_LOCATION%\python" createChangelog.py

 
rem -----Upgrade pymavlink if needed-----
if exist "..\..\pymavlink" (
 rem Rebuild and use pymavlink from pymavlink sources if available
 pushd ..\..\pymavlink
 "%PYTHON_LOCATION%\python.exe" setup.py build install
 popd
) else (
 if exist "..\..\mavlink\pymavlink" (
  rem Rebuild and use pymavlink from mavlink\pymavlink sources if available
  pushd ..\..\mavlink\pymavlink
  "%PYTHON_LOCATION%\python.exe" setup.py build install
  popd
 ) else (
  "%PYTHON_LOCATION%\Scripts\pip" install pymavlink -U
 )
)

rem -----Build MAVProxy-----
cd ..\
"%PYTHON_LOCATION%\python" setup.py clean build install
cd .\MAVProxy
copy ..\windows\mavproxy.spec
"%PYTHON_LOCATION%\Scripts\pyinstaller" -y --clean mavproxy.spec
del mavproxy.spec

rem -----Create version Info-----
@echo off
@echo %VERSION%> ..\windows\version.txt
@echo on

rem -----Build the Installer-----
cd  ..\windows\
rem Newer Inno Setup versions do not require a -compile flag, please add it if you have an old version
"%INNOSETUP%\ISCC.exe" /dMyAppVersion=%VERSION% mavproxy.iss

pause
