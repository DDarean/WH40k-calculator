from unittest.mock import patch

from script.calculator import Shooting
from script.model_stats import Model


@patch.object(Shooting, 'roll')
def test_hit_false(roll):
    test_model_a = Model('Necron Warrior', 'Gauss reaper')
    test_model_d = Model('Intercessor', 'Bolt pistol')
    shooting = Shooting(test_model_a, test_model_d)
    roll_result = range(1, 3)
    for result in roll_result:
        roll.return_value = result
        assert shooting.hit() is False


@patch.object(Shooting, 'roll')
def test_hit_true(roll):
    test_model_a = Model('Necron Warrior', 'Gauss reaper')
    test_model_d = Model('Intercessor', 'Bolt pistol')
    shooting = Shooting(test_model_a, test_model_d)
    roll_result = range(3, 7)
    for result in roll_result:
        roll.return_value = result
        assert shooting.hit() is True


@patch.object(Shooting, 'roll')
def test_wound(roll):
    test_model_a = Model('Necron Warrior', 'Gauss reaper')
    test_model_d = Model('Intercessor', 'Bolt pistol')
    test_model_a.weapon_S = 10
    test_model_d.t = 5
    shooting = Shooting(test_model_a, test_model_d)
    roll.return_value = 2
    assert shooting.wound() is True
    roll.return_value = 1
    assert shooting.wound() is False

    test_model_a.weapon_S = 10
    test_model_d.t = 6
    shooting = Shooting(test_model_a, test_model_d)
    roll.return_value = 3
    assert shooting.wound() is True
    roll.return_value = 2
    assert shooting.wound() is False

    test_model_a.weapon_S = 5
    test_model_d.t = 5
    shooting = Shooting(test_model_a, test_model_d)
    roll.return_value = 4
    assert shooting.wound() is True
    roll.return_value = 3
    assert shooting.wound() is False

    test_model_a.weapon_S = 4
    test_model_d.t = 5
    shooting = Shooting(test_model_a, test_model_d)
    roll.return_value = 5
    assert shooting.wound() is True
    roll.return_value = 4
    assert shooting.wound() is False

    test_model_a.weapon_S = 5
    test_model_d.t = 11
    shooting = Shooting(test_model_a, test_model_d)
    roll.return_value = 6
    assert shooting.wound() is True
    roll.return_value = 5
    assert shooting.wound() is False


@patch.object(Shooting, 'roll')
def test_save(roll):
    test_model_a = Model('Necron Warrior', 'Gauss reaper')
    test_model_d = Model('Intercessor', 'Bolt pistol')
    shooting = Shooting(test_model_a, test_model_d)
    assert test_model_d.sv - test_model_a.weapon_AP == 5
    roll.return_value = 4
    assert shooting.save() is True
    roll.return_value = 5
    assert shooting.save() is False
