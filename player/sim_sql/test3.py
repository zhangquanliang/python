
#---------------------------------------------------
#---------------------------------------------------
# Test 3 --Qualified Names
import proj as project
from pprint import pprint


def check(sql_statement, expected):
  print("SQL: " + sql_statement)
  result = conn.execute(sql_statement)
  result_list = list(result)

  print("expected:")
  pprint(expected)
  print("student: ")
  pprint(result_list)
  assert expected == result_list



conn = project.connect("test.db")
conn.execute("CREATE TABLE table_1 (col_1 INTEGER, _col2 TEXT, col_3_ REAL);")
# conn.execute("INSERT INTO table_1 VALUES (33, 'hi', 4.5);")
conn.execute('INSERT INTO table_1 VALUES (36, don\'t, 7);')
# conn.execute("INSERT INTO table_1 VALUES (36, 'hi ''josh''', 7);")

check(
  "SELECT col_1, _col2, col_3_ FROM table_1 ORDER BY col_1, _col2, col_3_;",
  [(36, 7, "don't")]
  )
