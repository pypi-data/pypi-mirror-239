import seldom


class MyTest2(seldom.TestCase):

    def test_case2(self):
        self.sleep(3)
        self.assertEqual(2 + 3, 5)
