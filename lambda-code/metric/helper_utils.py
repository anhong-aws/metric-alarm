import json

class HelperUtils:
    @staticmethod
    def format_json(obj, indent=0, prefix='- '):
        lines = []
        if isinstance(obj, dict):
            for k, v in obj.items():
                key_line = ' ' * indent + prefix + str(k) + ':'
                if isinstance(v, (dict, list)):
                    lines.append(key_line)
                    lines.extend(HelperUtils.format_json(v, indent + 4, prefix))
                else:
                    lines.append(key_line + ' ' + str(v))
        elif isinstance(obj, list):
            for i, item in enumerate(obj):
                if isinstance(item, (dict, list)):
                    lines.extend(HelperUtils.format_json(item, indent, prefix))
                else:
                    item_line = ' ' * indent + prefix + str(item)
                    lines.append(item_line)
        return lines


    @staticmethod
    def convert_json_text(obj):
        formatted_lines = HelperUtils.format_json(obj)
        formatted_text = '\n'.join(formatted_lines)
        # print("带有短划线和多层级的格式化文本:")
        # print(formatted_text)
        return formatted_text
    
    @staticmethod
    def parse_formatted_text(text):
        obj = {}
        lines = text.split('\n')
        current_obj = obj
        path = []
        for line in lines:
            if line.strip():  # 忽略空行
                indent = len(line) - len(line.lstrip(' '))
                level = indent // 4
                key_value_pair = line.strip('- ').split(': ', 1)
                if len(key_value_pair) == 2:
                    key, value = key_value_pair
                    # 确保路径与当前缩进级别匹配
                    path = path[:level]
                    current_obj = obj
                    for k in path:
                        current_obj = current_obj[k]
                    # 尝试将值转换为其原始类型
                    try:
                        value = json.loads(value)
                    except ValueError:
                        pass
                    current_obj[key] = value
                else:
                    # 处理嵌套对象
                    key = key_value_pair[0]
                    path = path[:level]
                    path.append(key)
                    current_obj = obj
                    for k in path[:-1]:
                        current_obj = current_obj[k]
                    current_obj[key] = {}
        return obj


# # 示例使用
# json_obj = {
#     "name": "John",
#     "age": 30,
#     "address": {
#         "street": "123 Main St",
#         "city": "New York"
#     }
# }

# formatted_text = HelperUtils.convert_json_text(json_obj)
# new_json_obj = HelperUtils.parse_formatted_text(formatted_text)
# print("\n转换回的JSON对象:")
# print(new_json_obj)
