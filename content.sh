#!/bin/bash

# 接受第一个命令行参数作为表名
TABLE_NAME=$1

# 使用 psql 执行查询，展示表内容
psql -d amazon -c "SELECT * FROM $TABLE_NAME;"