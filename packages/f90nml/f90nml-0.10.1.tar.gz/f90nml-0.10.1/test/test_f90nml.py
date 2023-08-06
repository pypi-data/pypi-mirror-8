import os
import sys
import unittest

sys.path.insert(1, '../')
import f90nml

class Test(unittest.TestCase):

    def setUp(self):
        self.empty_nml = {'empty_nml': {}}

        self.null_nml = {'null_nml':
                            {'null_value': None},
                         'null_comma_nml':
                            {'null_comma': None}
                        }

        self.types_nml = {'types_nml':
                            {'v_integer': 1,
                             'v_float': 1.0,
                             'v_complex': 1+2j,
                             'v_logical': True,
                             'v_string': 'Hello',
                            }
                         }

        self.vector_nml = {'vector_nml':
                            {'v': [1, 2, 3, 4, 5],
                             'v_idx': [1, 2, 3, 4],
                             'v_idx_ooo': [1, 2, 3, 4],
                             'v_range': [1, 2, 3, 4],
                             'v_implicit_start': [1, 2, 3, 4],
                             'v_implicit_end': [1, 2, 3, 4],
                             'v_implicit_all': [1, 2, 3, 4],
                             'v_null_start': [None, 2, 3, 4],
                             'v_null_interior': [1, 2, None, 4],
                             'v_null_end': [1, 2, 3, None],
                             'v_zero': [1, 0, 3],
                            }
                          }

        self.float_nml = {'float_nml':
                            {'v_float': 1.,
                             'v_decimal_end': 1.,
                             'v_negative': -1.,
                             'v_single': 1.,
                             'v_double': 1.,
                             'v_single_upper': 1.,
                             'v_double_upper': 1.,
                             'v_positive_index': 10.,
                             'v_negative_index': 0.1,
                            }
                         }

        self.string_nml = {'string_nml':
                            {'str_basic': 'hello',
                             'single_esc_delim': "a 'single' delimiter",
                             'double_esc_delim': 'a "double" delimiter',
                             'double_nested': "''x'' \"y\"",
                             'str_list': ['a', 'b', 'c'],
                             'slist_no_space': ['a', 'b', 'c'],
                             'slist_no_quote': ['a', 'b', 'c'],
                            }
                        }

        self.dtype_nml = {'dtype_nml':
                            {'dt_scalar': {'val': 1},
                             'dt_stack': {'outer': {'inner': 2} },
                             'dt_vector': {'vec': [1, 2, 3]}
                            },
                          'dtype_multi_nml':
                            {'dt': {'x': 1,
                                    'y': 2,
                                    'z': 3,
                                   }
                            },
                          'dtype_nested_nml':
                            {'f': {'g': {'x': 1,
                                         'y': 2,
                                         'z': 3,
                                         }
                                  }
                            },
                          'dtype_field_idx_nml':
                            {'f': {'x': [1, 2, 3]}
                            },
                          'dtype_vec_nml':
                            {'a': {'b': [{'c': 1, 'd': 2},
                                         {'c': 3, 'd': 4},
                                         {'c': 5, 'd': 6}
                                        ]
                                  }
                            }
                         }

        self.bcast_nml = {'bcast_nml':
                            {'x': [2.0, 2.0],
                             'y': [None, None, None],
                             'z': [True, True, True, True],
                            },
                          'bcast_endnull_nml':
                            {'x': [2.0, 2.0],
                             'y': [None, None, None],
                            }
                         }

        self.comment_nml = {'comment_nml':
                            {'v_cmt_inline': 123,
                             'v_cmt_in_str': 'This token ! is not a comment',
                             'v_cmt_after_str': 'This ! is not a comment',
                            }
                           }

        self.grp_repeat_nml = {'grp_repeat_nml':
                                [{'x': 1}, {'x': 2}],
                               'case_check_nml':
                                [{'y': 1}, {'y': 2}],
                              }

        self.f77_nml = {'f77_nml':
                            {'x': 123},
                        'next_f77_nml':
                            {'y': 'abc'},
                       }

        self.dollar_nml = {'dollar_nml':
                            {'v': 1.},
                          }


    def test_empty(self):
        test_nml = f90nml.read('empty.nml')
        self.assertEqual(self.empty_nml, test_nml)
        self.assert_write(test_nml, 'empty.nml')

    def test_null(self):
        test_nml = f90nml.read('null.nml')
        self.assertEqual(self.null_nml, test_nml)
        self.assert_write(test_nml, 'null_target.nml')

    def test_types(self):
        test_nml = f90nml.read('types.nml')
        self.assertEqual(self.types_nml, test_nml)
        self.assert_write(test_nml, 'types.nml')

    def test_vector(self):
        test_nml = f90nml.read('vector.nml')
        self.assertEqual(self.vector_nml, test_nml)
        self.assert_write(test_nml, 'vector_target.nml')

    def test_float(self):
        test_nml = f90nml.read('float.nml')
        self.assertEqual(self.float_nml, test_nml)
        self.assert_write(test_nml, 'float_target.nml')

    def test_string(self):
        test_nml = f90nml.read('string.nml')
        self.assertEqual(self.string_nml, test_nml)
        self.assert_write(test_nml, 'string_target.nml')

    def test_dtype(self):
        test_nml = f90nml.read('dtype.nml')
        self.assertEqual(self.dtype_nml, test_nml)
        self.assert_write(test_nml, 'dtype_target.nml')

    def test_bcast(self):
        test_nml = f90nml.read('bcast.nml')
        self.assertEqual(self.bcast_nml, test_nml)
        self.assert_write(test_nml, 'bcast_target.nml')

    def test_comment(self):
        test_nml = f90nml.read('comment.nml')
        self.assertEqual(self.comment_nml, test_nml)
        self.assert_write(test_nml, 'comment_target.nml')

    def test_grp_repeat(self):
        test_nml = f90nml.read('grp_repeat.nml')
        self.assertEqual(self.grp_repeat_nml, test_nml)
        self.assert_write(test_nml, 'grp_repeat_target.nml')

    def test_f77(self):
        test_nml = f90nml.read('f77.nml')
        self.assertEqual(self.f77_nml, test_nml)
        self.assert_write(test_nml, 'f77_target.nml')

    def test_dollar(self):
        test_nml = f90nml.read('dollar.nml')
        self.assertEqual(self.dollar_nml, test_nml)
        self.assert_write(test_nml, 'dollar_target.nml')

    def assert_write(self, nml, target_fname):

        tmp_fname = 'tmp.nml'
        f90nml.write(nml, tmp_fname)
        try:
            with open(tmp_fname) as tmp:
                with open(target_fname) as target:
                    tmp_str = tmp.read()
                    target_str = target.read()
                    self.assertEqual(tmp_str, target_str)
        finally:
            os.remove(tmp_fname)


if __name__ == '__main__':
    if os.path.isfile('tmp.nml'):
        os.remove('tmp.nml')
    unittest.main()
