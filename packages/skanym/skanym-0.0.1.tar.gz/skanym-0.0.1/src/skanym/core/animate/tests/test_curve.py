import unittest
import numpy as np

from skanym.core.math.constants import HIGH_R_TOL, HIGH_A_TOL
from skanym.core.animate.key import Key
from skanym.core.animate.curve import Curve


class TestCurveDefaultConstructor(unittest.TestCase):
    def setUp(self):
        self.kt0 = Key(0.0, [0.0, 0.0, 0.0])
        self.kt1 = Key(1, [1.0, 2.0, 3.0])
        self.kt2 = Key(20, [4.0, 5.0, 6.0])

        self.kr0 = Key(0.0, np.quaternion(1, 0.0, 0.0, 0.0))
        self.kr1 = Key(0.33, np.quaternion(2 / 3, 0.0, 2 / 3, 1 / 3))
        self.kr2 = Key(20.0, np.quaternion(4 / 3, 0.0, 4 / 3, 1 / 3))

    def test_animation_curve_default_constructor_with_default_params(self):
        curve = Curve()
        self.assertEqual(curve.keys, [])

    def test_animation_curve_default_constructor_with_valid_keys(self):
        curve = Curve(keys=[self.kt0, self.kt1, self.kt2])
        self.assertEqual(curve.keys, [self.kt0, self.kt1, self.kt2])

    def test_animation_curve_default_constructor_with_duplicate_keys(self):
        kt = Key(1, [0.0, 1.0, 0.0])
        with self.assertRaisesRegex(ValueError, "already exists in animation curve"):
            curve = Curve(keys=[self.kt0, self.kt1, self.kt2, kt])
            self.assertIsNone(curve)

    def test_animation_curve_default_constructor_with_different_key_types(self):
        with self.assertRaisesRegex(
            ValueError, "the type of the first key of the animation curve."
        ):
            curve = Curve(keys=[self.kt0, self.kr1, self.kt2])
            self.assertIsNone(curve)


class TestCurveGetKeyCount(unittest.TestCase):
    def setUp(self):
        self.kt1 = Key(0.33, [1.0, 2.0, 3.0])

    def test_animation_curve_get_key_count_with_no_keys(self):
        curve = Curve()
        self.assertEqual(curve.get_key_count(), 0)

    def test_animation_curve_get_key_count_with_key(self):
        curve = Curve(keys=[self.kt1])
        self.assertEqual(curve.get_key_count(), 1)


class TestCurveNormalizeTimes(unittest.TestCase):
    def setUp(self):
        self.kt0 = Key(0.0, [0.0, 0.0, 0.0])
        self.kt1 = Key(0.33, [1.0, 2.0, 3.0])
        self.kt2 = Key(20.0, [4.0, 5.0, 6.0])

    def test_animation_curve_normalize_times_with_no_keys(self):
        curve = Curve()
        curve.normalize_times(1.0)
        self.assertEqual(curve.keys, [])

    def test_animation_curve_normalize_times(self):
        curve = Curve(keys=[self.kt0, self.kt1, self.kt2])
        curve.normalize_times(20.0)
        self.assertTrue(
            np.allclose(
                [key.time for key in curve.keys],
                [0.0, 0.33 / 20.0, 1.0],
                rtol=HIGH_R_TOL,
                atol=HIGH_R_TOL,
            )
        )


class TestCurveGetKeyByTime(unittest.TestCase):
    def setUp(self):
        self.kt0 = Key(0.0, [0.0, 0.0, 0.0])
        self.kt1 = Key(0.33, [1.0, 2.0, 3.0])
        self.kt2 = Key(20.0, [4.0, 5.0, 6.0])

        self.curve0 = Curve(keys=[self.kt0, self.kt1, self.kt2])

    def test_animation_curve_get_key_at_with_no_keys(self):
        curve = Curve()
        self.assertIsNone(curve.get_key_at(0.0))

    def test_animation_curve_get_key_at_with_valid_time(self):
        self.assertEqual(self.curve0.get_key_at(0.0), self.kt0)
        self.assertEqual(self.curve0.get_key_at(0.33), self.kt1)
        self.assertEqual(self.curve0.get_key_at(20.0), self.kt2)

    def test_animation_curve_get_key_at_with_invalid_time(self):
        self.assertIsNone(self.curve0.get_key_at(-0.001))
        self.assertIsNone(self.curve0.get_key_at(1 / 3))
        self.assertIsNone(self.curve0.get_key_at(21))

    def test_animation_curve_get_key_at_with_close_time(self):
        self.assertEqual(self.curve0.get_key_at(20.0 + 1e-5), self.kt2)


class TestCurveGetPreviousKey(unittest.TestCase):
    def setUp(self):
        self.curve = Curve()

        for t in np.linspace(0, 1, 5):
            self.curve.add_key(Key(t, [t * 1.0, t * 2.0, t * 3.0]))

        self.single_key_curve = Curve(keys=[Key(0.0, [1.0, 2.0, 3.0])])

        self.special_curve = Curve(keys=[Key(0.25, [1.0, 2.0, 3.0]), Key(0.77, [4.0, 5.0, 6.0])])

    def test_animation_curve_get_previous_key_with_no_keyss(self):
        curve = Curve()
        self.assertIsNone(curve.get_previous_key(0))
        self.assertIsNone(curve.get_previous_key(0.25))
        self.assertIsNone(curve.get_previous_key(1))

    def test_animation_curve_get_previous_key_with_keys(self):
        self.assertEqual(self.curve.get_previous_key(0), self.curve.keys[0])
        self.assertEqual(self.curve.get_previous_key(0.25), self.curve.keys[1])
        self.assertEqual(self.curve.get_previous_key(1), self.curve.keys[-1])

    def test_animation_curve_get_previous_key_with_single_key(self):
        self.assertEqual(self.single_key_curve.get_previous_key(0), self.single_key_curve.keys[0])
        self.assertEqual(self.single_key_curve.get_previous_key(0.25), self.single_key_curve.keys[0])
        self.assertEqual(self.single_key_curve.get_previous_key(1), self.single_key_curve.keys[0])

    def test_animation_curve_get_previous_key_with_special_keys(self):        
        self.assertEqual(self.special_curve.get_previous_key(0), self.special_curve.keys[-1])
        self.assertEqual(self.special_curve.get_previous_key(0.25), self.special_curve.keys[0])
        self.assertEqual(self.special_curve.get_previous_key(1), self.special_curve.keys[-1])


class TestCurveGetNextKey(unittest.TestCase):
    def setUp(self):
        self.curve = Curve()
        for t in np.linspace(0, 1, 5):
            self.curve.add_key(Key(t, [t * 1.0, t * 2.0, t * 3.0]))
        
        self.special_curve = Curve(keys=[Key(0.25, [1.0, 2.0, 3.0]), Key(0.77, [4.0, 5.0, 6.0])])

    def test_animation_curve_get_next_key_with_no_keys(self):
        curve = Curve()
        self.assertIsNone(curve.get_next_key(0))
        self.assertIsNone(curve.get_next_key(0.25))
        self.assertIsNone(curve.get_next_key(1))

    def test_animation_curve_get_next_key_with_keys(self):
        self.assertEqual(self.curve.get_next_key(0), self.curve.keys[1])
        self.assertEqual(self.curve.get_next_key(0.25), self.curve.keys[2])
        self.assertEqual(self.curve.get_next_key(1), self.curve.keys[0])

    def test_animation_curve_get_next_key_with_special_keys(self):
        self.assertEqual(self.special_curve.get_next_key(0), self.special_curve.keys[0])
        self.assertEqual(self.special_curve.get_next_key(0.25), self.special_curve.keys[-1])
        self.assertEqual(self.special_curve.get_next_key(1), self.special_curve.keys[0])


class TestCurveGetPreviousValue(unittest.TestCase):
    def setUp(self):
        self.curve = Curve()
        for t in np.linspace(0, 1, 5):
            self.curve.add_key(Key(t, [t * 1.0, t * 2.0, t * 3.0]))

    def test_animation_curve_previous_value_with_no_keys(self):
        curve = Curve()
        self.assertIsNone(curve.get_previous_value(0))
        self.assertIsNone(curve.get_previous_value(0.25))
        self.assertIsNone(curve.get_previous_value(1))

    def test_animation_curve_previous_value_with_keys(self):
        self.assertTrue(
            np.allclose(
                self.curve.get_previous_value(0),
                [0.0, 0.0, 0.0],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.curve.get_previous_value(0.25),
                [0.25, 0.5, 0.75],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.curve.get_previous_value(0.9999999),
                [0.75, 1.5, 2.25],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.curve.get_previous_value(1),
                [0.0, 0.0, 0.0],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )


class TestCurveGetLerpValue(unittest.TestCase):
    def setUp(self):
        self.curve = Curve()
        for t in np.linspace(0, 1, 5):
            self.curve.add_key(Key(t, [t * 1.0, t * 2.0, t * 3.0]))

    def test_animation_curve_lerp_value_with_no_keys(self):
        curve = Curve()
        self.assertIsNone(curve.get_lerp_value(0))
        self.assertIsNone(curve.get_lerp_value(0.25))
        self.assertIsNone(curve.get_lerp_value(1))

    def test_animation_curve_lerp_value_with_keys(self):
        self.assertTrue(
            np.allclose(
                self.curve.get_lerp_value(0),
                [0.0, 0.0, 0.0],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.curve.get_lerp_value(0.1),
                [0.1, 0.2, 0.3],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.curve.get_lerp_value(0.9999999),
                [1.0, 2.0, 3.0],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.curve.get_lerp_value(1),
                [0.0, 0.0, 0.0],
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )

class TestCurveValidateForInterpolation(unittest.TestCase):
    def setUp(self):
        self.empty_curve = Curve()
        self.curve = Curve()
        for t in np.linspace(0, 1, 5):
            self.curve.add_key(Key(t, [t * 1.0, t * 2.0, t * 3.0]))

    def test_animation_curve_validate_for_interpolation_with_no_keys(self):
        with self.assertRaisesRegex(ValueError, "Animation curve must contain at least 1 key."):
            self.empty_curve.validate_for_interpolation()

class TestCurveShiftKeys(unittest.TestCase):
    def setUp(self):
        self.base_curve = Curve()
        for t in np.linspace(0, 1, 5):
            self.base_curve.add_key(Key(t, [t * 1.0, t * 2.0, t * 3.0]))

    def test_animation_curve_lerp_with_shifted_keys(self):
        curve = Curve(self.base_curve.keys)
        self.assertTrue(
            np.allclose(
                self.base_curve.get_lerp_value(0.0, shift=99),
                self.base_curve.get_lerp_value(0.0),
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.base_curve.get_lerp_value(0.05, shift=-1.2),
                self.base_curve.get_lerp_value(0.85),
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )
        self.assertTrue(
            np.allclose(
                self.base_curve.get_lerp_value(0.1, shift=0.42),
                self.base_curve.get_lerp_value(0.1 + 0.42),
                rtol=HIGH_R_TOL,
                atol=HIGH_A_TOL,
            )
        )        