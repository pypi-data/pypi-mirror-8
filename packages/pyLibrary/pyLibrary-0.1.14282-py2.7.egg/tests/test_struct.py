import unittest
from util.cnv import CNV
from util.collections import MAX
from util.env.logs import Log
from util.struct import Null, Struct
from util.structs.wraps import wrap


class TestStruct(unittest.TestCase):
    def test_none(self):
        a = 0
        b = 0
        c = None
        d = None

        if a == b:
            pass
        else:
            Log.error("error")

        if c == d:
            pass
        else:
            Log.error("error")

        if a == c:
            Log.error("error")

        if d == b:
            Log.error("error")

        if not c:
            pass
        else:
            Log.error("error")


    def test_null(self):
        a = 0
        b = 0
        c = Null
        d = Null
        e = Struct()
        f = Struct()

        if a == b:
            pass
        else:
            Log.error("error")

        if c == d:
            pass
        else:
            Log.error("error")

        if a == c:
            Log.error("error")

        if d == b:
            Log.error("error")

        if c == None:
            pass
        else:
            Log.error("error")

        if not c:
            pass
        else:
            Log.error("error")

        if Null != Null:
            Log.error("error")

        if Null != None:
            Log.error("error")

        if None != Null:
            Log.error("error")

        if e.test != f.test:
            Log.error("error")

    def test_get_value(self):
        a = wrap({"a": 1, "b": {}})

        if a.a != 1:
            Log.error("error")
        if not isinstance(a.b, dict):
            Log.error("error")

    def test_get_class(self):
        a = wrap({})
        _type = a.__class__

        if _type is not Struct:
            Log.error("error")

    def test_int_null(self):
        a = Struct()
        value = a.b*1000
        assert value == Null


    def test_list(self):
        if not []:
            pass
        else:
            Log.error("error")

        if []:
            Log.error("error")

        if not [0]:
            Log.error("error")


    def test_assign1(self):
        a = {}

        b = wrap(a)
        b.c = "test1"
        b.d.e = "test2"
        b.f.g.h = "test3"
        b.f.i = "test4"
        b.k["l.m.n"] = "test5"

        expected = {
            "c": "test1",
            "d": {
                "e": "test2"
            },
            "f": {
                "g": {
                    "h": "test3"
                },
                "i": "test4"
            },
            "k": {
                "l": {"m": {"n": "test5"}}
            }
        }
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")


    def test_assign2(self):
        a = {}

        b = wrap(a)
        b_c = b.c
        b.c.d = "test1"

        b_c.e = "test2"

        expected = {
            "c": {
                "d": "test1",
                "e": "test2"
            }
        }
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

    def test_assign3(self):
        # IMPOTENT ASSIGNMENTS DO NOTHING
        a = {}
        b = wrap(a)

        b.c = None
        expected = {}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

        b.c.d = None
        expected = {}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

        b["c.d"] = None
        expected = {}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

        b.c.d.e = None
        expected = {}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

        b.c["d.e"] = None
        expected = {}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

    def test_assign4(self):
        # IMPOTENT ASSIGNMENTS DO NOTHING
        a = {"c": {"d": {}}}
        b = wrap(a)
        b.c.d = None
        expected = {"c": {}}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")

        a = {"c": {"d": {}}}
        b = wrap(a)
        b.c = None
        expected = {}
        if CNV.object2JSON(expected) != CNV.object2JSON(a):
            Log.error("error")


    def test_slicing(self):

        def diff(record, index, records):
            """
            WINDOW FUNCTIONS TAKE THE CURRENT record, THE index THAT RECORD HAS
            IN THE WINDOW, AND THE (SORTED) LIST OF ALL records
            """
            # COMPARE CURRENT VALUE TO MAX OF PAST 5, BUT NOT THE VERY LAST ONE
            try:
                return record - MAX(records[index - 6:index - 1:])
            except Exception, e:
                return None


        data1_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        result1 = [diff(r, i, data1_list) for i, r in enumerate(data1_list)]
        assert result1 == [-7, None, None, None, None, None, 2, 2, 2]  # WHAT IS EXPECTED, BUT NOT WHAT WE WANT

        data2_list = wrap(data1_list)
        result2 = [diff(r, i, data2_list) for i, r in enumerate(data2_list)]
        assert result2 == [None, None, 2, 2, 2, 2, 2, 2, 2]

