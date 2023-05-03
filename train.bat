@echo off
echo Input Folder to Train
set /p input= 
echo Input Class Amount
set /p inputamt= 
echo Input Vocabulary Amount
set /p inputv= 
"python3" "train.py" "--folder" "%input%" "--c" "%inputamt%" "--v" "%inputv%"
pause