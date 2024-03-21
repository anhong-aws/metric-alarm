import numpy as np

def is_anomaly(data_point, data, threshold=10):
    mean = np.mean(data)
    std_dev = np.std(data)
    z_score = (data_point - mean) / std_dev
    
    if np.abs(z_score) > threshold:
        return True, z_score
    else:
        return False, z_score

# 示例数据
data = np.array([10, 12, 12, 13, 12, 11, 14, 13, 15, 10, 10, 100, 12, 14, 14])

# 从命令终端获取数据点
data_point = float(input("请输入一个数值来判断是否异常: "))

# 测试方法
is_outlier, z_score = is_anomaly(data_point, data)

print(f"数据点: {data_point}, Z分数: {z_score:.2f}, 是否异常: {'是' if is_outlier else '否'}")

