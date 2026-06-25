import os
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    pkg_share = FindPackageShare('navigation_2floor_env').find('navigation_2floor_env')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    cartographer_node = Node(
        package='cartographer_ros',
        executable='cartographer_node',
        name='cartographer_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-configuration_directory', os.path.join(pkg_share, 'config'),
                   '-configuration_basename', 'my_lidar.lua'],
        remappings=[
            # 核心：将 points2 话题重映射到你的雷达点云话题
            ('points2_1', '/back_lidar'),
            ('points2_2', '/front_lidar'),
        ]
    )

    # 发布栅格地图以便在 RViz 中查看
    occupancy_grid_node = Node(
        package='cartographer_ros',
        executable='cartographer_occupancy_grid_node',
        name='occupancy_grid_node',
        output='screen',
        parameters=[{'use_sim_time': use_sim_time}],
        arguments=['-resolution', '0.05'],
        remappings=[
            ('map', '/map')  # 可以重映射地图话题
        ]
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'rviz', 'demo_3d.rviz')],
        parameters=[{'use_sim_time': use_sim_time}],
    )

    return LaunchDescription([
        rviz_node,
        cartographer_node,
        occupancy_grid_node,
    ])