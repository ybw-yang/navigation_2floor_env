import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution, Command, FindExecutable
from launch_ros.actions import Node

def generate_launch_description():
    # Get package directories
    pkg_navigation_2floor_env = get_package_share_directory('navigation_2floor_env')
    
    # World file path - copy indoor_gazebo.sdf to worlds directory
    world_file = PathJoinSubstitution([pkg_navigation_2floor_env, 'worlds', 'indoor_gazebo.sdf'])

    # Robot Model (waffle_pi, waffle, or burger)
    robot_model = 'waffle_pi'
    
    # Try to get turtlebot3_description package
    try:
        pkg_turtlebot3_description = get_package_share_directory('turtlebot3_description')
        urdf_file = PathJoinSubstitution([pkg_turtlebot3_description, 'urdf', 'turtlebot3_' + robot_model + '.urdf'])
    except:
        # Fallback: try turtlebot3_gazebo package
        try:
            pkg_turtlebot3_gazebo = get_package_share_directory('turtlebot3_gazebo')
            urdf_file = PathJoinSubstitution([pkg_turtlebot3_gazebo, 'models', 'turtlebot3_' + robot_model, 'model.sdf'])
        except:
            raise Exception("Neither turtlebot3_description nor turtlebot3_gazebo package found!")

    # Initial Pose - Safe position in the indoor environment
    # Based on indoor_gazebo.sdf analysis:
    # Building size: 20.4m x 20.4m (walls at ±10.1m)
    # Lower floor center area around (0, 0) is relatively open
    # z=0.1 to avoid sinking into ground plane
    initial_x = '0.0'
    initial_y = '0.0'
    initial_z = '0.1'
    initial_yaw = '0.0'

    # Gazebo Server
    gazebo_server = ExecuteProcess(
        cmd=['gzserver', '-s', 'libgazebo_ros_init.so', '-s', 'libgazebo_ros_factory.so', world_file],
        output='screen'
    )

    # Gazebo Client (GUI)
    gazebo_client = ExecuteProcess(
        cmd=['gzclient'],
        output='screen'
    )

    # Robot State Publisher
    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        parameters=[{'robot_description': Command([FindExecutable(name='xacro'), ' ', urdf_file])}],
        output='screen'
    )

    # Spawn Entity
    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'turtlebot3',
            '-x', initial_x,
            '-y', initial_y,
            '-z', initial_z,
            '-Y', initial_yaw
        ],
        output='screen'
    )

    return LaunchDescription([
        gazebo_server,
        gazebo_client,
        robot_state_publisher_node,
        spawn_entity_node,
    ])
