# TurtleBot3 Gazebo Spawn Package

This ROS 2 package spawns a TurtleBot3 robot in an indoor Gazebo environment without collision.

## Package Structure

```
navigation_2floor_env/
├── CMakeLists.txt
├── package.xml
├── README.md
├── launch/
│   └── spawn_turtlebot.launch.py
└── worlds/
    └── indoor_gazebo.sdf
```

## Features

- Spawns TurtleBot3 (waffle_pi model by default) in an indoor two-story building environment
- Initial position carefully selected to avoid collision with walls and furniture
- Includes Gazebo server and client launch
- Robot state publisher for TF transforms

## Initial Spawn Position

The robot is spawned at position **(0.0, -5.0, 0.1)** with yaw **0.0** radians.

This position was chosen based on analysis of `indoor_gazebo.sdf`:
- Building dimensions: 20.4m × 20.4m (walls at ±10.1m)
- Lower floor open area in the center region
- z=0.1 prevents sinking into the ground plane
- No obstacles or furniture at this location

## Prerequisites

Install required dependencies:

```bash
sudo apt install ros-${ROS_DISTRO}-turtlebot3-description
sudo apt install ros-${ROS_DISTRO}-gazebo-ros-pkgs
```

For ROS 2 Humble/Iron/Jazzy, you may also need:
```bash
sudo apt install ros-${ROS_DISTRO}-turtlebot3-gazebo
```

## Usage

### Build the Package

```bash
cd ~/navigation_ws
colcon build --packages-select navigation_2floor_env
source install/setup.bash
```

### Launch the Simulation

```bash
ros2 launch navigation_2floor_env spawn_turtlebot.launch.py
```

This will:
1. Start Gazebo server with the indoor environment
2. Launch Gazebo client (GUI)
3. Load the TurtleBot3 URDF/SDF model
4. Spawn the robot at the safe initial position

## Customization

### Change Robot Model

Edit `launch/spawn_turtlebot.launch.py` and modify the `robot_model` variable:
```python
robot_model = 'burger'  # or 'waffle' or 'waffle_pi'
```

### Change Spawn Position

Edit `launch/spawn_turtlebot.launch.py` and modify the initial pose variables:
```python
initial_x = '0.0'   # X position in meters
initial_y = '-5.0'  # Y position in meters
initial_z = '0.1'   # Z position in meters (keep > 0 to avoid ground collision)
initial_yaw = '0.0' # Orientation in radians
```

**Important:** When changing the spawn position, ensure:
- The position is within the building bounds (±10.1m)
- Avoid wall positions (check `indoor_gazebo.sdf` for wall locations)
- Keep z > 0 to prevent physics glitches
- Choose areas without furniture or obstacles

### Safe Spawn Zones in indoor_gazebo.sdf

Based on the environment layout, these are safe spawn areas on the lower floor (z ≈ 0.1):
- Center area: (0.0, -5.0) - **Recommended**
- Open corridors between walls
- Avoid: Near walls (±10.1m), furniture locations, ramp area (x ∈ [-0.75, 0.75], y ∈ [-5.6, 5.6])

## Troubleshooting

### Robot spawns inside a wall or object
- Check the spawn coordinates in the launch file
- Verify they don't overlap with any collision objects in `indoor_gazebo.sdf`
- Increase `initial_z` slightly if robot sinks into ground

### TurtleBot3 model not found
- Ensure `turtlebot3_description` or `turtlebot3_gazebo` package is installed
- Check that the robot model name matches available models (burger, waffle, waffle_pi)

### Gazebo fails to start
- Verify Gazebo ROS packages are installed
- Check that the world file path is correct
- Ensure no other Gazebo instances are running

## Environment Details

The `indoor_gazebo.sdf` contains:
- Two-story building (20.4m × 20.4m)
- Lower floor (z = 0.05m) with rooms and furniture
- Upper floor (z = 3.1m) with offices and meeting areas
- Ramp connecting floors (15° incline)
- Various furniture: beds, tables, chairs, cabinets, shelves
- Semi-transparent outer walls

## License

Apache-2.0
