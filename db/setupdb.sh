#!/bin/bash

if [ "$1" == "small" ]; then
  # 如果传入参数为 "small"，执行以下命令
  echo "Setup small data db commands..."
  psql -d amazon -f ../drop_all_table.sql
  ./setup.sh
else
  # 如果没有传入参数，或参数不是 "small"，执行以下命令
  echo "Setup and Switch to large scale db commands..."
  psql -d amazon -f ../drop_all_table.sql
  python3 generated/gen.py
  ./setup.sh generated
fi
