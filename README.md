# Animal-Helper

- [后端配置](##后端配置)
- [前端配置](##前端配置)

## 后端配置

#### 安装依赖

```bash
pip install -r requirements.txt
```

---

##### 创建数据库

例如，数据库名称为：`AD`

---

#### 修改配置

数据迁移前，需要修改项目下数据库的配置

位置：`项目目录/Animal_Server/settings.py`，找到 👇 配置进行修改

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'AD', #改成你上面创建的数据库名称
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'TIME_ZONE': 'Asia/Shanghai'
    }
}
```

---

#### 数据迁移

配置修改完成后，执行 👇 的命令

```bash
python manage.py makemigrations
```

```bash
python manage.py migrate
```

数据迁移完成后，检查数据表

#### 导入预制数据

迁移完成后，导入预制数据

```bash
python manage.py loaddata init_data.json
python sample_data.py
```

⚠️ 注意：导入预制数据前需要先进行 migrate。由于预制数据会在开发过程中发生变化，如果更新预制数据，最好先清表，再重新导入。

---

#### 启动项目

预制数据创建完成后，就可以启动项目了

```bash
python manage.py runserver
```

## 前端配置

### 步骤 1：安装 Node.js 和 npm

Node.js 是 JavaScript 的运行环境，npm 是 Node.js 的包管理工具，Vue 项目依赖它们来运行和管理依赖。

#### Windows 系统

- 访问 [Node.js 官方下载页面](https://nodejs.org/en/download/)。
- 下载适合你系统的安装包（通常选择 LTS 版本）。
- 运行安装包，按照安装向导的提示完成安装。安装过程中保持默认设置即可。
- 安装完成后，打开命令提示符（CMD）或 PowerShell，输入以下命令验证安装是否成功：

```bash
node -v
npm -v
```

### 步骤 2：安装项目依赖

进入`项目目录/Animal_Front`，执行以下命令安装项目依赖：

```bash
npm install
```

### 步骤 3：启动项目

使用以下命令运行：

```bash
npm run dev
```
