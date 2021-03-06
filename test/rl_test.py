#!/usr/bin/python3
#  -*- coding: utf-8 -*-

import unittest

from dotdict import dotdict

from gomoku.env import GomokuEnv
from gomoku.nnet import GomokuNNet
from gomoku.rl import GomokuRL


class TestRL(unittest.TestCase):

    def setUp(self):
        self.args = dotdict({
            'rows': 7,
            'columns': 7,
            'n_in_row': 2,
            'history_num': 2,
            'conv_filters': 16,
            'conv_kernel': (3, 3),
            'residual_block_num': 2,
            'save_weights_path': './tmp',
            'max_sample_pool_size': 10000,
            'l2': 1e-4,
        })
        self.env = GomokuEnv(self.args)
        self.nnet = GomokuNNet(self.env, self.args)
        self.rl = GomokuRL(self.nnet, self.env, self.args)

    def test_coordinate_transform(self):
        """
        . . o . o . .
        . . x . x . .
        o x . . . x o
        . . . . . . .
        o x . . . x o
        . . x . x . .
        . . o . o . .
        """
        expected = {(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)}
        self.assertEqual(expected, set(self.rl.augment_coordinate(1, 2)))

    def test_augment_board(self):
        sgf = "B[12];W[02]"
        expected = {'B[12];W[02]', 'B[14];W[04]', 'B[21];W[20]', 'B[25];W[26]', 'B[41];W[40]', 'B[45];W[46]',
                    'B[52];W[62]', 'B[54];W[64]'}
        self.assertEqual(expected, set(self.rl.augment_board(sgf)))


if __name__ == '__main__':
    unittest.main()
