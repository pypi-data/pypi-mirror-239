"""Tests if  ``dist_plot`` is working as expected

--------------------------------------------------------------------------------
Command to run at the prompt:
    python -m unittest -v tests/ryan_joiner/test_dist_plot.py
    or
    python -m unittest -b tests/ryan_joiner/test_dist_plot.py

--------------------------------------------------------------------------------
"""
### GENERAL IMPORTS ###
import os
import unittest
import numpy as np
from matplotlib.axes import SubplotBase
import matplotlib.pyplot as plt
from pathlib import Path

### FUNCTION IMPORT ###
from tests.functions_to_test import functions
from normtest.ryan_joiner import dist_plot

os.system("cls")


class Test_dist_plot(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        fig, cls.axes = plt.subplots()
        cls.x_data = np.array(
            [148, 148, 154, 158, 158, 160, 161, 162, 166, 170, 182, 195, 210]
        )

    def test_outputs(self):
        result = dist_plot(
            self.axes,
            self.x_data,
            cte_alpha="3/8",
            min=4,
            max=50,
            weighted=False,
            safe=False,
        )
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

        result = dist_plot(
            axes=self.axes,
            x_data=self.x_data,
            cte_alpha="3/8",
            min=4,
            max=50,
            weighted=False,
            safe=False,
        )
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

    def test_safe(self):
        result = dist_plot(self.axes, self.x_data, safe=True)
        self.assertIsInstance(result, SubplotBase, msg="not a SubplotBase")
        plt.close()

    def test_basic_plot(self):
        fig1_base_path = Path("tests/ryan_joiner/figs_dist_plot/fig1.png")

        fig, ax = plt.subplots()
        result = dist_plot(ax, self.x_data)
        fig1_file = Path("tests/ryan_joiner/figs_dist_plot/fig1_test.png")
        plt.savefig(fig1_file)
        plt.close()

        self.assertTrue(
            functions.validate_file_contents(fig1_base_path, fig1_file),
            msg="figures does not match",
        )
        fig1_file.unlink()


if __name__ == "__main__":
    unittest.main()
