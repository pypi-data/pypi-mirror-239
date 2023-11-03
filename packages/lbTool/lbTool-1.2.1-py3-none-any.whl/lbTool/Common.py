import hashlib
import xml.etree.ElementTree as et


def str_to_md5(text):
    """
    字符串MD5加密
    :param text: 明文
    :return:
    """
    # 创建一个 MD5 对象
    md5 = hashlib.md5()
    # 将文本转换为二进制，并进行加密
    md5.update(text.encode('utf-8'))
    # 获取加密后的结果，以十六进制表示
    encrypted_text = md5.hexdigest()

    return encrypted_text


def byte_to_md5(binary):
    """
    字节MD5加密
    :param binary: 字节数组
    :return:
    """
    # 创建一个 MD5 对象
    md5 = hashlib.md5()
    # 填充文本二进制
    md5.update(binary)
    # 获取加密后的结果，以十六进制表示
    encrypted_text = md5.hexdigest()

    return encrypted_text


def parse_xml_config(xml_file_path, element_name):
    """
    解析XML
    :param xml_file_path: xml文件路径
    :param element_name: 节点名称
    :return:
    """
    # 解析 XML 文件
    tree = et.parse(xml_file_path)
    root = tree.getroot()

    # 获取数据库连接串参数
    params_obj = {}
    for elem in root.findall(f".//{element_name}/*"):
        params_obj[elem.tag] = elem.text

    return params_obj
