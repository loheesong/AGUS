@echo off
IF NOT EXIST out mkdir out
chdir beta-assembler
python .\assembler_wrapper.py -x ../uasm/code5 -o ../out/code5
