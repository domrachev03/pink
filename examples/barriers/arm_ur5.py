#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-License-Identifier: Apache-2.0
# Copyright 2022 Stéphane Caron

"""Universal Robots UR5 arm tracking a moving target."""

import meshcat_shapes
import numpy as np
import qpsolvers
from loop_rate_limiters import RateLimiter

import pink
from pink import solve_ik
from pink.barriers import PositionBarrier, ConfigurationBarrier
from pink.tasks import FrameTask, PostureTask
from pink.visualization import start_meshcat_visualizer

try:
    from robot_descriptions.loaders.pinocchio import load_robot_description
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "Examples need robot_descriptions, " "try ``pip install robot_descriptions``"
    ) from exc  # noqa: E501


if __name__ == "__main__":
    robot = load_robot_description("ur5_description", root_joint=None)
    viz = start_meshcat_visualizer(robot)

    end_effector_task = FrameTask(
        "ee_link",
        position_cost=50.0,  # [cost] / [m]
        orientation_cost=1.0,  # [cost] / [rad]
        lm_damping=100,  # tuned for this setup
    )

    posture_task = PostureTask(
        cost=1e-3,  # [cost] / [rad]
    )

    pos_cbf = PositionBarrier(
        "ee_link",
        indices=[1],
        max=np.array([0.6]),
        gain=np.array([100.0]),
        r=1.0,
    )
    configuration_cbf = ConfigurationBarrier(robot.model, gain=1, r=100.0)
    cbf_list = [pos_cbf, configuration_cbf]

    tasks = [end_effector_task, posture_task]

    q_ref = np.array(
        [
            1.27153374,
            -0.87988708,
            1.89104795,
            1.73996951,
            -0.24610945,
            -0.74979019,
        ]
    )
    configuration = pink.Configuration(robot.model, robot.data, q_ref)
    for task in tasks:
        task.set_target_from_configuration(configuration)
    viz.display(configuration.q)

    viewer = viz.viewer
    meshcat_shapes.frame(viewer["end_effector_target"], opacity=1.0)
    # meshcat_shapes.frame(viewer["end_effector"], opacity=1.0)

    # Select QP solver
    solver = qpsolvers.available_solvers[0]
    if "osqp" in qpsolvers.available_solvers:
        solver = "osqp"

    rate = RateLimiter(frequency=200.0)
    dt = rate.period
    t = 0.0  # [s]
    while True:
        # Update task targets
        end_effector_target = end_effector_task.transform_target_to_world
        end_effector_target.translation[1] = 0.0 + 0.7 * np.sin(t / 2)
        end_effector_target.translation[2] = 0.2

        # Update visualization frames
        viewer["end_effector_target"].set_transform(end_effector_target.np)
        viewer["end_effector"].set_transform(configuration.get_transform_frame_to_world(end_effector_task.frame).np)

        # Compute velocity and integrate it into next configuration
        # Note that default position limit handle given trajectory
        # much worse than CBF. Hence, we disable it here.
        velocity = solve_ik(
            configuration,
            tasks,
            dt,
            solver=solver,
            cbfs=cbf_list,
            use_position_limit=False,
        )
        configuration.integrate_inplace(velocity, dt)

        G, h = pos_cbf.compute_qp_inequality(configuration, dt=dt)
        print(f"Task error: {end_effector_task.compute_error(configuration)}")
        print(f"Position CBF value: {pos_cbf.compute_barrier(configuration)[0]:0.3f} >= 0")
        print(f"Configuration CBF value: {configuration_cbf.compute_barrier(configuration)} >= 0")
        print(f"Distance to manipulator: {configuration.get_transform_frame_to_world('ee_link').translation[1]} <= 0.6")
        print("-" * 60)
        # Visualize result at fixed FPS
        viz.display(configuration.q)
        rate.sleep()
        t += dt