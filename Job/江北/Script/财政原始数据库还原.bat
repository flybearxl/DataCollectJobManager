@echo off
echo 开始清理已存在数据.........
echo "....................."
echo "删除用户和表空间"
echo "drop user gadata cascade"
echo "drop tablespace mof including contents and datafiles"
echo "删除完成"
pause

