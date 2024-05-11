Here we will have the examples of using barriers, please go over [notes](NOTES.md) for more info. 

# Barrier Examples


- [Arm: UR5](#arm-ur5): with joints and end effector limits
- [Yumi Dual Arm](#dual-arm-yumi): self collisions with spheres

## Arm: UR5

A UR5 arm tracking a moving target while stopping in front of virtual wall:


<!-- TODO: Put your video here -->
https://github.com/stephane-caron/pink/assets/1189580/d0d6aae9-326b-45fe-8cd3-013f29f7343a

| Task | Cost |
|------|------|
| End-effector | 1 |
| Posture | $10^{-3}$ |

| Barrier | Gain |
|------|------|
| End-effector | $10^{3}$ |
| Configuration | $1$ |


## Dual Arm Yumi

A dual arm YuMi randomly swinging arms while avoiding self collisions:

<!-- TODO: Put your video here -->
https://github.com/stephane-caron/pink/assets/1189580/ef3f2571-6188-4b14-ae3f-b22428b11f5c

| Task | Cost |
|------|------|
| Left end-effector | (50,1) |
| Right end-effector | (50,1) |
| Posture | $10^{-3}$ |


| Barrier | Gain |
|------|------|
| Spheres Collision  | 100 |
| Configuration | $1$ |