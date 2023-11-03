## 模块介绍
### 通用模块：lbTool.Common  
内含：MD5加密、解析XML配置文件
### 数据库操作模块 lbTool.Db
依赖于pony包实现，以oracle连接串演示
```python
from lbTool.Db import *
# 创建连接
db_con = Database("oracle", user="user", password="pwd", dsn='host:port/sid')
# 定义实体（不指定_table_则默认类名为表名）
class Test(db_con.Entity):
    _table_ = ("模式名", "表名")
    id = PrimaryKey(int)
    name = Optional(str)
    age = Optional(int)
# 获取操作实例
db = Db(db_con, is_create_table=False, show_sql=True)
# 查询
data = db.query(Test, id=1)
```
### AES/SM4加密模块 lbTool.EnCipher  
- AES  
```python
from lbTool.EnCipher import AesUtil

aes_key = "aes_key"
aes_iv = "aes_iv"
plaintext = "123"
aes_ciphertext = AesUtil.encrypt_cbc(aes_key, aes_iv, plaintext)
print("AES加密后===", aes_ciphertext)
aes_plaintext = AesUtil.decrypt_cbc(aes_key, aes_iv, aes_ciphertext)
print("AES解密后===", aes_plaintext)
```
- SM4
```python
from lbTool.EnCipher import Sm4Util

sm4_key = "sm4_key"
plaintext = "123"
sm4_ciphertext = Sm4Util.encrypt_ecb(sm4_key, plaintext)
print("SM4加密后===", sm4_ciphertext)
sm4_plaintext = Sm4Util.decrypt_ecb(sm4_key, sm4_ciphertext)
print("SM4解密后===", sm4_plaintext)
```
### 文件操作模块 lbTool.FileUtil
内含：数据流写文件，合并PDF，Word转PDF
### 日志操作模块 lbTool.Logging
默认在程序所在目录新建 Log/app_yyyymmdd.log 日志文件
```python
from lbTool.Logging import Logger
# 获取日志处理器 默认空控制台输出,可选fileLogger文件输出 
logger = Logger("fileLogger")
logger.info("xxx")
```