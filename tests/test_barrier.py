#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Tests that should pass for all barriers."""

import unittest

import numpy as np
import pinocchio as pin
from robot_descriptions.loaders.pinocchio import load_robot_description

from pink import Configuration
from pink.barriers import PositionBarrier


class TestBarrier(unittest.TestCase):
    """Tests that should pass for all barriers."""

    def setUp(self):
        self.robot = load_robot_description(
            "upkie_description", root_joint=pin.JointModelFreeFlyer()
        )
        self.conf = Configuration(
            self.robot.model,
            self.robot.data,
            q=np.zeros(self.robot.nq),
        )
        self.dt = 1e-3  # [s]

    def test_diff_form_dimensions(self):
        """Velocity barrier dimension is the number of bounded joints."""
        for barrier in [PositionBarrier("left_hip", p_min=np.zeros(3))]:
            H, c = barrier.compute_qp_objective(self.conf)
            G, h = barrier.compute_qp_inequality(self.conf, self.dt)
            self.assertEqual(H.shape[0], self.robot.nv)
            self.assertEqual(H.shape[1], self.robot.nv)
            self.assertEqual(c.shape[0], self.robot.nv)
            self.assertEqual(G.shape[0], barrier.dim)
            self.assertEqual(G.shape[1], self.robot.nv)

    def test_barrier_value_dimension(self):
        """Test tha shape of value in all barriers is correct."""

        for barrier in [PositionBarrier("left_hip", p_min=np.zeros(3))]:
            v = barrier.compute_barrier(self.conf)
            self.assertEqual(v.shape[0], barrier.dim)

    def test_barrier_jacobians_dimension(self):
        """Test that shapes of jacobians in all barriers are correct."""

        for barrier in [PositionBarrier("left_hip", p_min=np.zeros(3))]:
            J = barrier.compute_jacobian(self.conf)
            self.assertEqual(J.shape[0], barrier.dim)
            self.assertEqual(J.shape[1], self.robot.nv)

    def test_barrier_without_save_radius(self):
        """Barrier without"""
        for limit in [PositionBarrier("left_hip", r=0.0, p_min=np.zeros(3))]:
            H, c = limit.compute_qp_objective(self.conf)
            self.assertTrue(np.allclose(H, 0))
            self.assertTrue(np.allclose(c, 0))

    def test_barrier_save_radius(self):
        """"""
        for limit in [PositionBarrier("left_hip", r=1.0, p_min=np.zeros(3))]:
            H, c = limit.compute_qp_objective(self.conf)
            self.assertFalse(np.allclose(H, 0))
            if np.any(limit.compute_safe_policy(self.conf) != 0):
                self.assertFalse(np.allclose(c, 0))

    def test_task_repr(self):
        """Test task string representation."""
        for limit in [PositionBarrier("universe", r=0.0, p_min=np.zeros(3))]:
            self.assertTrue("gain=" in repr(limit))
            self.assertTrue("safety_policy=" in repr(limit))
            self.assertTrue("r=" in repr(limit))
