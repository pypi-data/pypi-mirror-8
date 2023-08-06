# -*- coding: utf-8 -*-
import unittest, sys, os, sqlite3
##include smstools/ directory
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__),'..')))
import core, android, core_tests

class AndroidTest(core_tests.BaseTests):

    def setUp(self):
        self.db = self.get_empty_db_in_memory(android)


    def test_write_parse(self):
        true_texts = core.getTestTexts()
        cursor = self.db.cursor()

        android.Android().write_cursor(true_texts, cursor)
        parsed_texts = android.Android().parse_cursor(cursor)

        for i in range(len(true_texts)):
            self.assertEqual(true_texts[i], parsed_texts[i])
        cursor.close()


if __name__ == '__main__':
    unittest.main()
