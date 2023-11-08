import seldom


class MyTest3(seldom.TestCase):

    def test_case3(self):
        self.sleep(3)
        self.assertEqual(2 + 3, 5)
