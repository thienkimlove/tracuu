#!/bin/bash
#
# CHANGE VALUES OF DATABASE AND MYSQL TO MATCH YOUR SETUP

DATABASE="python_medicine"
MYSQL="mysql -uroot -ptieungao -N --database=$DATABASE"

# convert database with all tables to utf8mb4
echo "ALTER DATABASE $DATABASE CHARACTER SET = utf8mb4 COLLATE = utf8mb4_unicode_ci;" | $MYSQL

echo 'show tables' | eval $MYSQL | while read table
do
    echo "ALTER TABLE $table ROW_FORMAT=DYNAMIC;" |
        eval $MYSQL
    echo "ALTER TABLE $table CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;" |
        eval $MYSQL
done
