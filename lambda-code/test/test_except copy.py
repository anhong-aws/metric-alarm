import numpy as np

def moving_average(data, window_size):
    return np.convolve(data, np.ones(window_size), 'valid') / window_size

def moving_std_dev(data, window_size):
    ma = moving_average(data, window_size)
    return np.sqrt(moving_average((data[:len(ma)] - ma)**2, window_size))

def is_anomaly(data_point, data, window_size=3, threshold=3):
    if len(data) < window_size:
        raise ValueError("数据点的数量少于窗口大小，请提供更多的数据。")
    
    ma = moving_average(data, window_size)
    msd = moving_std_dev(data, window_size)
    
    mean = ma[-1]  # 使用最近的移动平均值
    std_dev = msd[-1]  # 使用最近的移动标准差
    
    z_score = (data_point - mean) / std_dev
    
    if np.abs(z_score) > threshold:
        return True, z_score
    else:
        return False, z_score

# 示例数据
data = np.array([10, 12, 12, 13, 12, 11, 14, 13, 15, 10, 10, 100, 102, 100, 101, 100])

# 从命令终端获取数据点
data_point = float(input("请输入一个数值来判断是否异常: "))

# 测试方法
is_outlier, z_score = is_anomaly(data_point, data)

print(f"数据点: {data_point}, Z分数: {z_score:.2f}, 是否异常: {'是' if is_outlier else '否'}")
