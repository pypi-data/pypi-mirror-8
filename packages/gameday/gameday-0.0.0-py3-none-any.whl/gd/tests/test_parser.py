from datetime import datetime, date, time
import unittest

from pretend import stub

from gd import parser


class Test_get_game(unittest.TestCase):
    """Test the gd.parser.get_game function."""

    def test_get_game(self):
        expected = {"local_game_time": "12:00"}
        tree = stub(attrib=expected)
        actual = parser.get_game(tree)
        self.assertEqual(actual, expected)


class Test_get_date(unittest.TestCase):
    """Test the gd.parser.get_date function."""

    def test_get_date(self):
        game = {"date": "July 2, 1984"}
        tree = stub(attrib=game)
        actual = parser.get_date(tree)
        self.assertEqual(actual, date(1984, 7, 2))


class Test_get_players(unittest.TestCase):
    """Test the gd.parser.get_players function."""

    def test_get_players(self):
        expected = {"first": "Ryne", "last": "Sandberg"}
        s1 = stub(attrib=expected)
        s2 = stub(attrib=expected)
        s3 = stub(attrib=expected)
        tree = stub(findall=lambda arg: [s1, s2, s3])
        actual = parser.get_players(tree)
        self.assertEqual(list(actual), [expected]*3)


class Test_get_plate_umpire(unittest.TestCase):
    """Test the gd.parser.get_plate_umpire function."""

    def test_get_plate_umpire(self):
        attrib = {"position": "home", "name": "Gerry Davis"}
        expected = {"name": "Gerry Davis"}
        element = stub(attrib=attrib)
        tree = stub(findall=lambda arg: [element])
        actual = parser.get_plate_umpire(tree)
        self.assertEqual(actual, expected)

    def test_get_plate_umpire_no_pu(self):
        attrib = {"position": "first", "name": "Ted Barrett"}
        element = stub(attrib=attrib)
        tree = stub(findall=lambda arg: [element])
        self.assertRaisesRegex(Exception, "No plate umpire found.",
                               parser.get_plate_umpire, tree)

    def test_get_plate_umpire_no_umpires(self):
        tree = stub(findall=lambda arg: [])
        self.assertRaisesRegex(Exception, "No plate umpire found.",
                               parser.get_plate_umpire, tree)


class Test_get_teams(unittest.TestCase):
    """Test the gd.parser.get_teams function."""

    def test_get_teams(self):
        value = {"name": "Chicago Cubs"}
        team = stub(attrib=value)
        tree = stub(findall=lambda arg: [team, team])
        actual = parser.get_teams(tree)
        self.assertEqual(list(actual), [value, value])


class Test_get_stadium(unittest.TestCase):
    """Test the gd.parser.get_stadium function."""

    def test_get_stadium(self):
        expected = {"name": "Wrigley Field"}
        stadium = stub(attrib=expected)
        tree = stub(find=lambda arg: stadium)
        actual = parser.get_stadium(tree)
        self.assertEqual(actual, expected)

    def test_get_stadium_missing(self):
        tree = stub(find=lambda arg: None)
        self.assertRaisesRegex(Exception, "Did not find a stadium.",
                               parser.get_stadium, tree)


class Test_get_actions(unittest.TestCase):
    """Test the gd.parser.get_actions function."""

    def test_get_actions(self):
        input_value = {"tfs": "123456",
                       "tfs_zulu": "2014-07-19T23:12:35Z",
                       "id": "987654"}
        value = stub(attrib=input_value)
        tree = stub(findall=lambda arg: [value])
        actual = parser.get_actions(tree)

        expected = {"tfs": time(12, 34),
                    "tfs_zulu": datetime(2014, 7, 19, 23, 12, 35),
                    "id": "987654"}
        self.assertEqual(list(actual), [expected])


class Test_get_atbats(unittest.TestCase):
    """Test the gd.parser.get_atbats function."""

    def test_get_atbats_no_atbats(self):
        tree = stub(findall=lambda arg: [])
        actual = parser.get_atbats(tree)
        self.assertEqual(list(actual), [])

    def test_get_atbats(self):
        input_value = {"start_tfs": "123456",
                       "start_tfs_zulu": "2014-07-19T23:12:35Z",
                       "score": "T"}
        value = stub(attrib=input_value)
        atbat = stub(findall=lambda arg: [value],
                     attrib=input_value)
        tree = stub(findall=lambda arg: [atbat])

        actual = parser.get_atbats(tree)
        expected = {"start_tfs": time(12, 34),
                    "start_tfs_zulu": datetime(2014, 7, 19, 23, 12, 35),
                    "score": True}
        self.assertEqual(list(actual), [expected])


class Test_get_pitches(unittest.TestCase):
    """Test the gd.parser.get_pitches function."""

    def test_get_pitches(self):
        atbat_attribs = {"start_tfs_zulu": "2014-07-19T23:12:35Z"}
        pitch_attribs = {"tfs": "123456",
                         "tfs_zulu": "2014-07-19T23:15:35Z"}
        pitch_value = stub(attrib=pitch_attribs)

        atbat = stub(findall=lambda arg: [pitch_value],
                     attrib=atbat_attribs)
        tree = stub(findall=lambda arg: [atbat])

        actual = parser.get_pitches(tree)
        expected = {"tfs": time(12, 34),
                    "tfs_zulu": datetime(2014, 7, 19, 23, 15, 35),
                    "start_tfs_zulu": datetime(2014, 7, 19, 23, 12, 35)}
        self.assertEqual(list(actual), [expected])
