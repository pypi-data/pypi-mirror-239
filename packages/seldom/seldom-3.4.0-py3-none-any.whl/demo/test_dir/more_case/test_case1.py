import seldom


class MyTest1(seldom.TestCase):

    def test_case1(self):
        self.sleep(3)
        self.assertEqual(2 + 3, 5)
