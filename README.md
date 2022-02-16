# Pink

[![build](https://img.shields.io/github/workflow/status/stephane-caron/pink/CI)](https://github.com/stephane-caron/pink/actions)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen?logo=read-the-docs&style=flat)](https://scaron.info/doc/pink/)
[![PyPI package](https://img.shields.io/pypi/v/pin-pink)](https://pypi.org/project/pin-pink/)
![Status](https://img.shields.io/pypi/status/pin-pink)

**P**ython **in**verse **k**inematics for your robot model based on [Pinocchio](https://github.com/stack-of-tasks/pinocchio).

## Upcoming changes

Pink's API is **not stable**. Expect the following upcoming changes:

- Import task template from pymanoid
- Reformulate task gains as time constants

## Installation

First, install [Pinocchio](https://github.com/stack-of-tasks/pinocchio), for instance by ``pip install pin``.

Then install Pink by:

```sh
pip install pin-pink
```

## Usage

*Under construction...*

## Example

*Under construction...*

## History

Pink implements the same task-based inverse kinematics as [pymanoid](https://github.com/stephane-caron/pymanoid), but it is much simpler to install and runs faster thanks to Pinocchio. Its internal math is summarized in [this note](https://scaron.info/robot-locomotion/inverse-kinematics.html). If you find yourself needing to read that to use the library, it means the API has abstraction leakage, please open an issue :-)