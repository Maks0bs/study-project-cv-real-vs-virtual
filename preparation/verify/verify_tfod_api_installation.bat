@echo off

if [%1]==[] goto usage

python "%1\object_detection\builders\model_builder_tf2_test.py"
goto :eof

:usage
@echo Usage: %0 ^<PathToTFODAPi^>
exit /B 1
