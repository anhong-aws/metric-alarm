import numpy as np

def is_anomaly(data_point, data, threshold=3.5):
    median = np.median(data)
    mad = np.median(np.abs(data - median))
    
    # 避免除以零
    if mad == 0:
        mad = 1e-9
    
    modified_z_score = 0.6745 * (data_point - median) / mad
    
    if np.abs(modified_z_score) > threshold:
        return True, modified_z_score
    else:
        return False, modified_z_score

# 示例数据
data = np.array([110, 102, 200, 121, 130])

# 从命令终端获取数据点
data_point = float(input("请输入一个数值来判断是否异常: "))

# 测试方法
is_outlier, modified_z_score = is_anomaly(data_point, data)

print(f"数据点: {data_point}, 修改后的Z分数: {modified_z_score:.2f}, 是否异常: {'是' if is_outlier else '否'}")
