@echo off
echo Input Folder with test files
set /p input= 
echo Input checkpoint path
set /p inputckpt= 
"python3" "C:\Users\tycho\Documents\premaster\python\evaluate.py" "--folder" "%input%" "--checkpoint" "%inputckpt%" "--checkhamspam" "True"
pause