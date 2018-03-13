
"""
Name:
Time To Completion:
Comments:

Sources:
"""
import string
from operator import itemgetter

_ALL_DATABASES = {}


class Connection(object):
    def __init__(self, filename):
        """
        Takes a filename, but doesn't do anything with it.
        (The filename will be used in a future project).
        """
        if filename in _ALL_DATABASES:
            self.database = _ALL_DATABASES[filename]
        else:
            self.database = Database(filename)
            _ALL_DATABASES[filename] = self.database

    def execute(self, statement):
        """
         采取SQL语句。
         返回元组列表（除非选择语句，否则为空）
         用行来返回）.
        """
        def create_table(tokens):
            """
           确定令牌添加的名称和列信息
             数据库自己创建一个新表。
            """
            pop_and_check(tokens, "CREATE")
            pop_and_check(tokens, "TABLE")
            table_name = tokens.pop(0)
            pop_and_check(tokens, "(")
            column_name_type_pairs = []
            while True:
                column_name = tokens.pop(0)
                column_type = tokens.pop(0)
                assert column_type in {"TEXT", "INTEGER", "REAL"}
                column_name_type_pairs.append((column_name, column_type))
                comma_or_close = tokens.pop(0)
                if comma_or_close == ")":
                    break
                assert comma_or_close == ','
            self.database.create_new_table(table_name, column_name_type_pairs)

        def insert(tokens):
            """
            Determines the table name and row values to add.
            """
            pop_and_check(tokens, "INSERT")
            pop_and_check(tokens, "INTO")
            table_name = tokens.pop(0)
            pop_and_check(tokens, "VALUES")
            pop_and_check(tokens, "(")
            # pop_and_check(tokens, "'")
            row_contents = []

            while True:
                item = tokens.pop(0)

                print(item)
                row_contents.append(item)
                comma_or_close = tokens.pop(0)
                if comma_or_close == ")":
                    break
                # print(comma_or_close)
                try:
                    assert comma_or_close == ','
                except:
                    print(comma_or_close)
                    import time
                    # time.sleep(100)
            self.database.insert_into(table_name, row_contents)

        def select(tokens):
            """
            Determines the table name, output_columns, and order_by_columns.
            """
            pop_and_check(tokens, "SELECT")
            output_columns = []
            while True:
                col = tokens.pop(0)
                output_columns.append(col)
                comma_or_from = tokens.pop(0)
                if comma_or_from == "FROM":
                    break
                assert comma_or_from == ','
            table_name = tokens.pop(0)
            pop_and_check(tokens, "ORDER")
            pop_and_check(tokens, "BY")
            order_by_columns = []
            while True:
                col = tokens.pop(0)
                order_by_columns.append(col)
                if not tokens:
                    break
                pop_and_check(tokens, ",")
            return self.database.select(
                output_columns, table_name, order_by_columns)

        tokens = tokenize(statement)
        assert tokens[0] in {"CREATE", "INSERT", "SELECT"}
        last_semicolon = tokens.pop()
        assert last_semicolon == ";"

        if tokens[0] == "CREATE":
            create_table(tokens)
            return []
        elif tokens[0] == "INSERT":
            insert(tokens)
            return []
        else:  # tokens[0] == "SELECT"
            return select(tokens)
        assert not tokens

    def close(self):
        """
        Empty method that will be used in future projects
        """
        pass


def connect(filename):
    """
    Creates a Connection object with the given filename
    """
    return Connection(filename)


class Database:
    def __init__(self, filename):
        self.filename = filename
        self.tables = {}

    def create_new_table(self, table_name, column_name_type_pairs):
        assert table_name not in self.tables
        self.tables[table_name] = Table(table_name, column_name_type_pairs)
        return []

    def insert_into(self, table_name, row_contents):
        assert table_name in self.tables
        table = self.tables[table_name]
        table.insert_new_row(row_contents)
        return []

    def select(self, output_columns, table_name, order_by_columns):
        assert table_name in self.tables
        table = self.tables[table_name]
        return table.select_rows(output_columns, order_by_columns)


class Table:
    def __init__(self, name, column_name_type_pairs):
        self.name = name
        self.column_names, self.column_types = zip(*column_name_type_pairs)
        self.rows = []

    def insert_new_row(self, row_contents):
        assert len(self.column_names) == len(row_contents)
        row = dict(zip(self.column_names, row_contents))
        self.rows.append(row)

    def select_rows(self, output_columns, order_by_columns):
        def expand_star_column(output_columns):
            new_output_columns = []
            for col in output_columns:
                if col == "*":
                    new_output_columns.extend(self.column_names)
                else:
                    new_output_columns.append(col)
            return new_output_columns

        def check_columns_exist(columns):
            assert all(col in self.column_names for col in columns)

        def sort_rows(order_by_columns):
            return sorted(self.rows, key=itemgetter(*order_by_columns))

        def generate_tuples(rows, output_columns):
            for row in rows:
                yield tuple(row[col] for col in output_columns)

        expanded_output_columns = expand_star_column(output_columns)
        check_columns_exist(expanded_output_columns)
        check_columns_exist(order_by_columns)
        sorted_rows = sort_rows(order_by_columns)
        return generate_tuples(sorted_rows, expanded_output_columns)


def pop_and_check(tokens, same_as):
    item = tokens.pop(0)
    assert item == same_as, "{} != {}".format(item, same_as)


def collect_characters(query, allowed_characters):
    letters = []
    for letter in query:
        if letter not in allowed_characters:
            break
        letters.append(letter)
    return "".join(letters)


def remove_leading_whitespace(query, tokens):
    whitespace = collect_characters(query, string.whitespace)
    return query[len(whitespace):]


def remove_word(query, tokens):
    word = collect_characters(query,
                              string.ascii_letters + "_" + string.digits)
    if word == "NULL":
        tokens.append(None)
    else:
        tokens.append(word)
    return query[len(word):]


def remove_text(query, tokens):
    assert query[0] == "'"
    query = query[1:]
    end_quote_index = query.find("'")
    text = query[:end_quote_index]
    tokens.append(text)
    query = query[end_quote_index + 1:]
    return query


def remove_integer(query, tokens):
    int_str = collect_characters(query, string.digits)
    tokens.append(int_str)
    return query[len(int_str):]


def remove_number(query, tokens):
    query = remove_integer(query, tokens)
    if query[0] == ".":
        whole_str = tokens.pop()
        query = query[1:]
        query = remove_integer(query, tokens)
        frac_str = tokens.pop()
        float_str = whole_str + "." + frac_str
        tokens.append(float(float_str))
    else:
        int_str = tokens.pop()
        tokens.append(int(int_str))
    return query


def tokenize(query):
    tokens = []
    tokens_dict = {}
    while query:
        id = 1
        # print("Query:{}".format(query))
        # print("Tokens: ", tokens)
        old_query = query

        if query[0] in string.whitespace:
            query = remove_leading_whitespace(query, tokens)
            continue

        if query[0] in (string.ascii_letters + "_"):
            query = remove_word(query, tokens)
            continue

        if query[0] in "(),;*\'":
            tokens.append(query[0])
            query = query[1:]
            id +=1
            tokens_dict[id] = query

        if query[0] in "\'":
            a = tokens_dict[id-1]
            b = tokens_dict[id]
            c = tokens_dict[id+1]
            d = a+b+c
            tokens.append(d)
            continue

        if query[0] == "'":
            query = remove_text(query, tokens)
            continue

        if query[0] in string.digits:
            query = remove_number(query, tokens)
            continue

        if len(query) == len(old_query):
            raise AssertionError("Query didn't get shorter.")

    return tokens

 #-----------------------------
      #Start Here





# #---------------------------------------------------
# #---------------------------------------------------
# # Test 1 -- Regression Check
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table_1 (col_1 INTEGER, _col2 TEXT, col_3_ REAL);")
# conn.execute("INSERT INTO table_1 VALUES (33, 'hi', 4.5);")
# conn.execute("CREATE TABLE table2 (col_1 INTEGER, other INTEGER);")
# conn.execute("INSERT INTO table2 VALUES (15, 782);")
# conn.execute("INSERT INTO table2 VALUES (615, 7582);")
# check(
#   "SELECT * FROM table_1 ORDER BY _col2, col_1;",
#   [(33, 'hi', 4.5)]
#   )
# check("SELECT * FROM table2 ORDER BY other, col_1;",
#   [(15, 782), (615, 7582)]
#   )
# conn.execute("INSERT INTO table_1 VALUES (3, 'hi', 4.5);")
# conn.execute("INSERT INTO table2 VALUES (165, 7282);")
# conn.execute("INSERT INTO table_1 VALUES (54, 'string with spaces', 3.0);")
# conn.execute("INSERT INTO table_1 VALUES (75842, 'string with spaces', 3.0);")
# conn.execute("INSERT INTO table_1 VALUES (623, 'string with spaces', 3.0);")

# check("SELECT * FROM table_1 ORDER BY _col2, col_1;",
#   [(3, 'hi', 4.5), (33, 'hi', 4.5), (54, 'string with spaces', 3.0), (623, 'string with spaces', 3.0), (75842, 'string with spaces', 3.0)])
# check("SELECT * FROM table2 ORDER BY other, col_1;",
#   [(15, 782), (165, 7282), (615, 7582)])



# #---------------------------------------------------
# #---------------------------------------------------
# # Test 2 -- Escaping Strings
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table_1 (col_1 INTEGER, _col2 TEXT, col_3_ REAL);")
# conn.execute("INSERT INTO table_1 VALUES (33, 'hi', 4.5);")
# conn.execute("INSERT INTO table_1 VALUES (36, 'don''t', 7);")
# conn.execute("INSERT INTO table_1 VALUES (36, 'hi ''josh''', 7);")

# check(
#   "SELECT * FROM table_1 ORDER BY _col2, col_1;",
#   [(36, "don't", 7), (33, 'hi', 4.5), (36, "hi 'josh'", 7)]
#   )



# #---------------------------------------------------
# #---------------------------------------------------
# # Test 3 --Qualified Names
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table_1 (col_1 INTEGER, _col2 TEXT, col_3_ REAL);")
# conn.execute("INSERT INTO table_1 VALUES (33, 'hi', 4.5);")
# conn.execute("INSERT INTO table_1 VALUES (36, 'don''t', 7);")
# conn.execute("INSERT INTO table_1 VALUES (36, 'hi ''josh''', 7);")

# check(
#   "SELECT col_1, col_3_, table_1._col2 FROM table_1 ORDER BY table_1._col2, _col2, col_1;",
#   [(36, 7, "don't"), (33, 4.5, 'hi'), (36, 7, "hi 'josh'")]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 4 ----Select Star
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table_1 (col_1 INTEGER, _col2 TEXT, col_3_ REAL);")
# conn.execute("INSERT INTO table_1 VALUES (33, 'hi', 4.5);")
# conn.execute("INSERT INTO table_1 VALUES (36, 'don''t', 7);")
# conn.execute("INSERT INTO table_1 VALUES (36, 'hi ''josh''', 7);")

# check(
#   "SELECT col_1, *, col_3_, table_1._col2, * FROM table_1 ORDER BY table_1._col2, _col2, col_1;",
#   [(36, 36, "don't", 7, 7, "don't", 36, "don't", 7),
#  (33, 33, 'hi', 4.5, 4.5, 'hi', 33, 'hi', 4.5),
#  (36, 36, "hi 'josh'", 7, 7, "hi 'josh'", 36, "hi 'josh'", 7)]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 5 ----Insert Into Normal Order
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness');")
# conn.execute("INSERT INTO table (one, two, three) VALUES (11.4, 437, 'sadness');")

# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
#   [(3.4, 43, 'happiness'), (11.4, 437, 'sadness')]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 6 ----Insert Into Different Order
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness');")
# conn.execute("INSERT INTO table (one, three, two) VALUES (11.4, 'sadness', 84);")

# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
#   [(3.4, 43, 'happiness'), (11.4, 84, 'sadness')]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 7 ----Insert Into Not All Columns
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness');")
# conn.execute("INSERT INTO table (one, three) VALUES (11.4, 'sadness');")

# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
#   [(3.4, 43, 'happiness'), (11.4, None, 'sadness')]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 8 ----Insert Into Multiple Columns
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness');")
# conn.execute("INSERT INTO table (one, three) VALUES (11.4, 'sadness'), (84.7, 'fear'), (94.7, 'weird');")
# conn.execute("INSERT INTO table (two, three) VALUES (13, 'warmth'), (34, 'coldness');")


# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
#   [(None, 34, 'coldness'),
#  (84.7, None, 'fear'),
#  (3.4, 43, 'happiness'),
#  (11.4, None, 'sadness'),
#  (None, 13, 'warmth'),
#  (94.7, None, 'weird')]
#   )


#---------------------------------------------------
#---------------------------------------------------
# Test 9 ----Where Clause
# import project
# from pprint import pprint
#
# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)
#
#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list
#
#
#
# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness'), (5345.6, 42, 'sadness'), (43.24, 25, 'life');")
# conn.execute("INSERT INTO table VALUES (323.4, 433, 'warmth'), (5.6, 42, 'thirst'), (4.4, 235, 'Skyrim');")
#
#
# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (43.24, 25, 'life'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (323.4, 433, 'warmth')]
#   )
#
# check(
#   "SELECT * FROM table WHERE two > 50 ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'), (323.4, 433, 'warmth')]
# )
#
# check(
#   "SELECT * FROM table WHERE two = 42 ORDER BY three, two, one;",
# [(5345.6, 42, 'sadness'), (5.6, 42, 'thirst')])
#
# check(
#   "SELECT * FROM table WHERE three IS NOT NULL ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (43.24, 25, 'life'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (323.4, 433, 'warmth')]
# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 10 ----Where Clause With NULL
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness'), (5345.6, 42, 'sadness'), (43.24, 25, 'life');")
# conn.execute("INSERT INTO table VALUES (323.4, 433, 'warmth'), (5.6, 42, 'thirst'), (4.4, 235, 'Skyrim');")
# conn.execute("INSERT INTO table VALUES (NULL, NULL, 'other'), (5.6, NULL, 'hunger'), (NULL, 235, 'want');")


# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (5.6, None, 'hunger'),
#  (43.24, 25, 'life'),
#  (None, None, 'other'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (None, 235, 'want'),
#  (323.4, 433, 'warmth')]
#   )

# check(
#   "SELECT * FROM table WHERE two > 50 ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'), (None, 235, 'want'), (323.4, 433, 'warmth')]
# )

# check(
#   "SELECT * FROM table WHERE two = 42 ORDER BY three, two, one;",
# [(5345.6, 42, 'sadness'), (5.6, 42, 'thirst')])

# check(
#   "SELECT * FROM table WHERE two IS NOT NULL ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (43.24, 25, 'life'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (None, 235, 'want'),
#  (323.4, 433, 'warmth')]
# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 11 ----Where Clause Qualified
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness'), (5345.6, 42, 'sadness'), (43.24, 25, 'life');")
# conn.execute("INSERT INTO table VALUES (323.4, 433, 'warmth'), (5.6, 42, 'thirst'), (4.4, 235, 'Skyrim');")
# conn.execute("INSERT INTO table VALUES (NULL, NULL, 'other'), (5.6, NULL, 'hunger'), (NULL, 235, 'want');")


# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (5.6, None, 'hunger'),
#  (43.24, 25, 'life'),
#  (None, None, 'other'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (None, 235, 'want'),
#  (323.4, 433, 'warmth')]
#   )

# check(
#   "SELECT * FROM table WHERE table.two > 50 ORDER BY three;",
# [(4.4, 235, 'Skyrim'), (None, 235, 'want'), (323.4, 433, 'warmth')]
# )

# check(
#   "SELECT table.* FROM table WHERE two = 42 ORDER BY three, two, one;",
# [(5345.6, 42, 'sadness'), (5.6, 42, 'thirst')])

# check(
#   "SELECT * FROM table WHERE two IS NOT NULL ORDER BY table.three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (43.24, 25, 'life'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (None, 235, 'want'),
#  (323.4, 433, 'warmth')]
# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 12 ----Delete
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness'), (5345.6, 42, 'sadness'), (43.24, 25, 'life');")
# conn.execute("INSERT INTO table VALUES (323.4, 433, 'warmth'), (5.6, 42, 'thirst'), (4.4, 235, 'Skyrim');")
# conn.execute("INSERT INTO table VALUES (NULL, NULL, 'other'), (5.6, NULL, 'hunger'), (NULL, 235, 'want');")


# check(
#   "SELECT * FROM table ORDER BY three, two, one;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (5.6, None, 'hunger'),
#  (43.24, 25, 'life'),
#  (None, None, 'other'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (None, 235, 'want'),
#  (323.4, 433, 'warmth')]
#   )

# conn.execute("DELETE FROM table;")


# check(
#   "SELECT * FROM table ORDER BY three;",
#   []
# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 13 ----Delete Where
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE table (one REAL, two INTEGER, three TEXT);")
# conn.execute("INSERT INTO table VALUES (3.4, 43, 'happiness'), (5345.6, 42, 'sadness'), (43.24, 25, 'life');")
# conn.execute("INSERT INTO table VALUES (323.4, 433, 'warmth'), (5.6, 42, 'thirst'), (4.4, 235, 'Skyrim');")
# conn.execute("INSERT INTO table VALUES (NULL, NULL, 'other'), (5.6, NULL, 'hunger'), (NULL, 235, 'want');")


# check(
#   "SELECT * FROM table ORDER BY three;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (5.6, None, 'hunger'),
#  (43.24, 25, 'life'),
#  (None, None, 'other'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (None, 235, 'want'),
#  (323.4, 433, 'warmth')]
#   )

# conn.execute("DELETE FROM table WHERE one IS NULL;")

# check(
#   "SELECT * FROM table ORDER BY three;",
# [(4.4, 235, 'Skyrim'),
#  (3.4, 43, 'happiness'),
#  (5.6, None, 'hunger'),
#  (43.24, 25, 'life'),
#  (5345.6, 42, 'sadness'),
#  (5.6, 42, 'thirst'),
#  (323.4, 433, 'warmth')]
#   )

# conn.execute("DELETE FROM table WHERE two < 50;")


# check(
#   "SELECT * FROM table ORDER BY three;",
#   [(4.4, 235, 'Skyrim'), (5.6, None, 'hunger'), (323.4, 433, 'warmth')]

# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 14 ----Update
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE students (name TEXT, grade INTEGER, notes TEXT);")
# conn.execute("INSERT INTO students VALUES ('Josh', 562, 'Likes Python'), ('Dennis', 45, 'Likes Networks'), ('Jie', 455, 'Likes Driving');")
# conn.execute("INSERT INTO students VALUES ('Cam', 524, 'Likes Anime'), ('Zizhen', 4532, 'Likes Reading'), ('Emily', 245, 'Likes Environmentalism');")


# check(
#   "SELECT * FROM students ORDER BY name;",
# [('Cam', 524, 'Likes Anime'),
#  ('Dennis', 45, 'Likes Networks'),
#  ('Emily', 245, 'Likes Environmentalism'),
#  ('Jie', 455, 'Likes Driving'),
#  ('Josh', 562, 'Likes Python'),
#  ('Zizhen', 4532, 'Likes Reading')]
#   )

# conn.execute("UPDATE students SET grade = 100, notes = 'Likes Databases';")


# check(
#   "SELECT * FROM students ORDER BY name;",
#   [('Cam', 100, 'Likes Databases'),
#  ('Dennis', 100, 'Likes Databases'),
#  ('Emily', 100, 'Likes Databases'),
#  ('Jie', 100, 'Likes Databases'),
#  ('Josh', 100, 'Likes Databases'),
#  ('Zizhen', 100, 'Likes Databases')]
# )



# #---------------------------------------------------
# #---------------------------------------------------
# # Test 15 ----Update Where
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE students (name TEXT, grade INTEGER, notes TEXT);")
# conn.execute("INSERT INTO students VALUES ('Josh', 562, 'Likes Python'), ('Dennis', 45, 'Likes Networks'), ('Jie', 455, 'Likes Driving');")
# conn.execute("INSERT INTO students VALUES ('Cam', 524, 'Likes Anime'), ('Zizhen', 4532, 'Likes Reading'), ('Emily', 245, 'Likes Environmentalism');")


# check(
#   "SELECT * FROM students ORDER BY name;",
# [('Cam', 524, 'Likes Anime'),
#  ('Dennis', 45, 'Likes Networks'),
#  ('Emily', 245, 'Likes Environmentalism'),
#  ('Jie', 455, 'Likes Driving'),
#  ('Josh', 562, 'Likes Python'),
#  ('Zizhen', 4532, 'Likes Reading')]
#   )

# conn.execute("UPDATE students SET notes = 'High Grade' WHERE grade > 100;")


# check(
#   "SELECT * FROM students ORDER BY name;",
#   [('Cam', 524, 'High Grade'),
#  ('Dennis', 45, 'Likes Networks'),
#  ('Emily', 245, 'High Grade'),
#  ('Jie', 455, 'High Grade'),
#  ('Josh', 562, 'High Grade'),
#  ('Zizhen', 4532, 'High Grade')]
# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 16 ----Distinct
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE students (name TEXT, grade INTEGER, notes TEXT);")
# conn.execute("INSERT INTO students VALUES ('Josh', 99, 'Likes Python'), ('Dennis', 99, 'Likes Networks'), ('Jie', 52, 'Likes Driving');")
# conn.execute("INSERT INTO students VALUES ('Cam', 56, 'Likes Anime'), ('Zizhen', 56, 'Likes Reading'), ('Emily', 74, 'Likes Environmentalism');")


# check(
#   "SELECT * FROM students ORDER BY name;",
# [('Cam', 56, 'Likes Anime'),
#  ('Dennis', 99, 'Likes Networks'),
#  ('Emily', 74, 'Likes Environmentalism'),
#  ('Jie', 52, 'Likes Driving'),
#  ('Josh', 99, 'Likes Python'),
#  ('Zizhen', 56, 'Likes Reading')]
#   )

# check(
#   "SELECT DISTINCT grade FROM students ORDER BY grade;",
#   [(52,), (56,), (74,), (99,)]
# )

# check(
#   "SELECT DISTINCT grade FROM students WHERE name < 'Emily' ORDER BY grade;",
#   [(56,), (99,)]
# )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 17 ----Join
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE students (name TEXT, grade INTEGER, class TEXT);")
# conn.execute("CREATE TABLE classes (course TEXT, instructor TEXT);")

# conn.execute("INSERT INTO students VALUES ('Josh', 99, 'CSE480'), ('Dennis', 99, 'CSE480'), ('Jie', 52, 'CSE491');")
# conn.execute("INSERT INTO students VALUES ('Cam', 56, 'CSE480'), ('Zizhen', 56, 'CSE491'), ('Emily', 74, 'CSE431');")

# conn.execute("INSERT INTO classes VALUES ('CSE480', 'Dr. Nahum'), ('CSE491', 'Dr. Josh'), ('CSE431', 'Dr. Ofria');")


# check(
#   "SELECT students.name, students.grade, classes.course, classes.instructor FROM students LEFT OUTER JOIN classes ON students.class = classes.course ORDER BY classes.instructor, students.name, students.grade;",
# [('Jie', 52, 'CSE491', 'Dr. Josh'),
#  ('Zizhen', 56, 'CSE491', 'Dr. Josh'),
#  ('Cam', 56, 'CSE480', 'Dr. Nahum'),
#  ('Dennis', 99, 'CSE480', 'Dr. Nahum'),
#  ('Josh', 99, 'CSE480', 'Dr. Nahum'),
#  ('Emily', 74, 'CSE431', 'Dr. Ofria')]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 18 ----Join With Where
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE students (name TEXT, grade INTEGER, class TEXT);")
# conn.execute("CREATE TABLE classes (course TEXT, instructor TEXT);")

# conn.execute("INSERT INTO students VALUES ('Josh', 99, 'CSE480'), ('Dennis', 99, 'CSE480'), ('Jie', 52, 'CSE491');")
# conn.execute("INSERT INTO students VALUES ('Cam', 56, 'CSE480'), ('Zizhen', 56, 'CSE491'), ('Emily', 74, 'CSE431');")

# conn.execute("INSERT INTO classes VALUES ('CSE480', 'Dr. Nahum'), ('CSE491', 'Dr. Josh'), ('CSE431', 'Dr. Ofria');")


# check(
#   "SELECT students.name, students.grade, classes.course, classes.instructor FROM students LEFT OUTER JOIN classes ON students.class = classes.course WHERE students.grade > 60 ORDER BY classes.instructor, students.name, students.grade;",
# [('Dennis', 99, 'CSE480', 'Dr. Nahum'),
#  ('Josh', 99, 'CSE480', 'Dr. Nahum'),
#  ('Emily', 74, 'CSE431', 'Dr. Ofria')]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 19 ----Join With NULL
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE students (name TEXT, grade INTEGER, class TEXT);")
# conn.execute("CREATE TABLE classes (course TEXT, instructor TEXT);")

# conn.execute("INSERT INTO students VALUES ('Josh', 99, 'CSE480'), ('Dennis', 99, 'CSE480'), ('Jie', 52, 'CSE491');")
# conn.execute("INSERT INTO students VALUES ('Cam', 56, 'CSE480'), ('Zizhen', 56, 'CSE491'), ('Emily', 74, 'CSE431');")
# conn.execute("INSERT INTO students VALUES ('James', 96, 'CSE335'), ('Carol', 87, NULL), ('Jackie', 45, 'CSE323');")


# conn.execute("INSERT INTO classes VALUES ('CSE480', 'Dr. Nahum'), ('CSE491', 'Dr. Josh'), ('CSE431', 'Dr. Ofria');")
# conn.execute("INSERT INTO classes VALUES ('CSE331', 'Dr. Owens'), (NULL, 'Chair');")


# check(
#   "SELECT students.name, students.grade, classes.course, classes.instructor FROM students LEFT OUTER JOIN classes ON students.class = classes.course ORDER BY students.name;",
# [('Cam', 56, 'CSE480', 'Dr. Nahum'),
#  ('Carol', 87, None, None),
#  ('Dennis', 99, 'CSE480', 'Dr. Nahum'),
#  ('Emily', 74, 'CSE431', 'Dr. Ofria'),
#  ('Jackie', 45, None, None),
#  ('James', 96, None, None),
#  ('Jie', 52, 'CSE491', 'Dr. Josh'),
#  ('Josh', 99, 'CSE480', 'Dr. Nahum'),
#  ('Zizhen', 56, 'CSE491', 'Dr. Josh')]
#   )


# #---------------------------------------------------
# #---------------------------------------------------
# # Test 20 ----Integration
# import project
# from pprint import pprint

# def check(sql_statement, expected):
#   print("SQL: " + sql_statement)
#   result = conn.execute(sql_statement)
#   result_list = list(result)

#   print("expected:")
#   pprint(expected)
#   print("student: ")
#   pprint(result_list)
#   assert expected == result_list



# conn = project.connect("test.db")
# conn.execute("CREATE TABLE pets (name TEXT, species TEXT, age INTEGER);")
# conn.execute("CREATE TABLE owners (name TEXT, age INTEGER, id INTEGER);")
# conn.execute("INSERT INTO pets VALUES ('RaceTrack', 'Ferret', 3), ('Ghost', 'Ferret', 2), ('Zoe', 'Dog', 7), ('Ebony', 'Dog', 17);")
# conn.execute("INSERT INTO pets (species, name) VALUES ('Rat', 'Ginny'), ('Dog', 'Balto'), ('Dog', 'Clifford');")

# conn.execute("UPDATE pets SET age = 15 WHERE name = 'RaceTrack';")


# check(
#   "SELECT species, *, pets.name FROM pets WHERE age > 3 ORDER BY pets.name;",
# [('Dog', 'Ebony', 'Dog', 17, 'Ebony'),
#  ('Ferret', 'RaceTrack', 'Ferret', 15, 'RaceTrack'),
#  ('Dog', 'Zoe', 'Dog', 7, 'Zoe')]
#  )

# conn.execute("INSERT INTO owners VALUES ('Josh', 29, 10), ('Emily', 27, 2), ('Zach', 25, 4), ('Doug', 34, 5);")
# conn.execute("DELETE FROM owners WHERE name = 'Doug';")
# check(
#   "SELECT owners.* FROM owners ORDER BY id;",
# [('Emily', 27, 2), ('Zach', 25, 4), ('Josh', 29, 10)]
#  )

# conn.execute("CREATE TABLE ownership (name TEXT, id INTEGER);")
# conn.execute("INSERT INTO ownership VALUES ('RaceTrack', 10), ('Ginny', 2), ('Ghost', 2), ('Zoe', 4);")

# check("SELECT pets.name, pets.age, ownership.id FROM pets LEFT OUTER JOIN ownership ON pets.name = ownership.name WHERE pets.age IS NULL ORDER BY pets.name;",
#   [('Balto', None, None), ('Clifford', None, None), ('Ginny', None, 2)]

#   )
