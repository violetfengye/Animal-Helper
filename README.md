# Animal-Helper

#### 安装依赖

```bash
pip install -r requirements.txt
```
##### 创建数据库

例如，数据库名称为：`AD`

---

#### 修改配置

数据迁移前，需要修改项目下数据库的配置

位置：`项目目录/Animal_Server/settings.py`，找到👇配置进行修改

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AD',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TIME_ZONE': 'Asia/Shanghai'
    }
}
```
