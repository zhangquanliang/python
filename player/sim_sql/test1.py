
#---------------------------------------------------
#---------------------------------------------------
# Test 1 -- Regression Check
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
conn.execute("INSERT INTO table_1 VALUES (33, 'hi', 4.5);")
conn.execute("CREATE TABLE table2 (col_1 INTEGER, other INTEGER);")
conn.execute("INSERT INTO table2 VALUES (15, 782);")
conn.execute("INSERT INTO table2 VALUES (615, 7582);")
check(
  "SELECT * FROM table_1 ORDER BY _col2, col_1;",
  [(33, 'hi', 4.5)]
  )
check("SELECT * FROM table2 ORDER BY other, col_1;",
  [(15, 782), (615, 7582)]
  )
# conn.execute("INSERT INTO table_1 VALUES (3, 'hi', 4.5);")
# conn.execute("INSERT INTO table2 VALUES (165, 7282);")
# conn.execute("INSERT INTO table_1 VALUES (54, 'string with spaces', 3.0);")
# conn.execute("INSERT INTO table_1 VALUES (75842, 'string with spaces', 3.0);")
# conn.execute("INSERT INTO table_1 VALUES (623, 'string with spaces', 3.0);")
#
# check("SELECT * FROM table_1 ORDER BY _col2, col_1;",
#   [(3, 'hi', 4.5), (33, 'hi', 4.5), (54, 'string with spaces', 3.0), (623, 'string with spaces', 3.0), (75842, 'string with spaces', 3.0)])
# check("SELECT * FROM table2 ORDER BY other, col_1;",
#   [(15, 782), (165, 7282), (615, 7582)])
