include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  -- 基础配置
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "base_link",        -- 改为你的机器人基座标系
  published_frame = "odom",
  odom_frame = "odom",
  provide_odom_frame = false,
  publish_frame_projected_to_2d = false, -- 2D建图设为true
  
  -- 数据源配置 - 使用2个PointCloud2
  num_laser_scans = 0,
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 2,                -- 两个激光雷达
  
  -- 传感器开关
  use_odometry = true,                -- 你没有里程计
  use_pose_extrapolator = true,        -- 使用姿态外推器
  use_nav_sat = false,
  use_landmarks = false,
  
  -- 超时和发布周期（参考配置中的值）
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  
  -- 采样率（全部设为1表示不降采样）
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 1.,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,
  landmarks_sampling_ratio = 1.,
}

-- 使用2D SLAM
MAP_BUILDER.use_trajectory_builder_2d = true

-- 轨迹生成器配置
TRAJECTORY_BUILDER.collate_landmarks = false
TRAJECTORY_BUILDER_2D.num_accumulated_range_data = 2
TRAJECTORY_BUILDER_2D.use_imu_data = false  -- 你没有IMU
TRAJECTORY_BUILDER_2D.submaps.num_range_data = 45

-- 点云滤波参数
TRAJECTORY_BUILDER_2D.adaptive_voxel_filter.max_length = 0.2
TRAJECTORY_BUILDER_2D.adaptive_voxel_filter.min_num_points = 400

-- 激光雷达范围
TRAJECTORY_BUILDER_2D.max_range = 30.0  -- 根据你的雷达调整
TRAJECTORY_BUILDER_2D.min_range = 0.2
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 5.0

-- 扫描匹配参数
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.translation_weight = 20
TRAJECTORY_BUILDER_2D.ceres_scan_matcher.rotation_weight = 20

-- 实时相关扫描匹配
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.linear_search_window = 0.1
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.translation_delta_cost_weight = 1e-1
TRAJECTORY_BUILDER_2D.real_time_correlative_scan_matcher.rotation_delta_cost_weight = 1e-1

-- 体素滤波
TRAJECTORY_BUILDER_2D.voxel_filter_size = 0.025

-- 位姿图优化
POSE_GRAPH.optimize_every_n_nodes = 35
POSE_GRAPH.constraint_builder.max_constraint_distance = 5.0
POSE_GRAPH.constraint_builder.min_score = 0.5

return options