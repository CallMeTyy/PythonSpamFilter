@echo off
echo Input Folder to Train
set /p input= 
echo Input Class Amount
set /p inputamt= 
echo Input Vocabulary Amount
set /p inputv= 
"python3" "C:\Users\tycho\Documents\premaster\python\train.py" "--folder" "%input%" "--c" "%inputamt%" "--v" "%inputv%"
pause