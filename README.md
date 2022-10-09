# Robot Arm Package for Object Manipulation
This repository is a ROS package for object manipulation with robot **Mitsubishi RV6SDL**.

## Project structure
The structure is standard ROS package structure.

    .
    ├── documentation
    ├── launch
    ├── scripts
    └── src

The main components are

- `documentation` - directory where the documentation is stored
- `launch` - directory where the ROS launch files are stored
- `scripts` - directory where the python scripts for ROS nodes are stored
- `src` - directory where the source code of the project is stored

## Usage
For running the project, please run the following command:

    roslaunch robot_arm_manipulation robot_arm_manipulation.launch


