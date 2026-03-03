# Food Delivery - 后端系统架构说明

> **技术约束**: The back end of your application must be built using **Python** and **Django**.

本文档描述外卖应用的后端系统架构，包括项目结构、请求流程、应用模块与配置要点。

---

## 1. 技术栈

| 层级 | 技术 |
|------|------|
| 语言 | Python 3.x |
| Web 框架 | Django |
| 数据库 | SQLite（开发）/ 可切换 PostgreSQL 等（生产） |
| 应用服务器 | WSGI（如 Gunicorn、uWSGI） |
| 模板 | Django Template Engine |

---

## 2. 项目结构（Django 标准布局）

```
food_delivery/
├── manage.py                    # Django 管理入口
├── requirements.txt             # Python 依赖
├── food_delivery_project/       # 项目配置包（Project）
│   ├── __init__.py
│   ├── settings.py              # 全局配置
│   ├── urls.py                  # 根 URL 路由
│   └── wsgi.py                  # WSGI 应用入口
├── accounts/                    # 应用：用户认证 (M1)
├── restaurants/                 # 应用：餐厅与菜单浏览 (M2)
├── carts/                       # 应用：购物车 (M3)
├── orders/                      # 应用：订单 (M4, M5)
├── merchants/                   # 应用：商家管理 (C2)
├── reviews/                     # 应用：评价与收藏 (S1, S2, C1)
├── templates/                   # 项目级模板
├── static/                      # 静态文件 (CSS/JS/图片)
└── media/                       # 用户上传文件（运行时生成）
```

- **Project**（`food_delivery_project`）：负责全局配置与根路由。
- **Apps**（accounts、restaurants、carts、orders、merchants、reviews）：按业务域划分的可复用模块，每个 app 可包含 `models`、`views`、`urls`、`forms`、`admin` 等。

---

## 3. 请求流程（MVT）

```
HTTP 请求
    → food_delivery_project/urls.py (ROOT_URLCONF)
    → 各 app 的 urls.py（include）
    → 对应 app 的 views.py（视图函数/类）
    → 使用 models 读写数据库 或 直接渲染模板
    → 返回 HttpResponse / TemplateResponse
```

- **Model**：数据模型，定义在各自 app 的 `models.py`，由 Django ORM 映射到数据库。
- **View**：业务逻辑，在 `views.py` 中处理请求、调用 Model、选择模板并返回响应。
- **Template**：HTML 模板，位于 `templates/` 或各 app 的 `templates/<app_name>/`。

---

## 4. 应用模块职责

| App | 职责 | 对应设计文档 |
|-----|------|----------------|
| **accounts** | 用户注册、登录、登出、资料 | M1 |
| **restaurants** | 餐厅列表、菜单浏览、搜索/筛选 | M2 |
| **carts** | 购物车增删改查、数量更新 | M3 |
| **orders** | 下单、结账、订单历史、订单状态 | M4, M5 |
| **merchants** | 商家后台、菜单管理、订单查看 | C2 |
| **reviews** | 评价、收藏列表 | S1, S2, C1 |

各 app 通过 `food_delivery_project/settings.py` 的 `INSTALLED_APPS` 注册，通过 `food_delivery_project/urls.py` 的 `include()` 挂载子路由。

---

## 5. URL 路由设计

根 URL 配置在 `food_delivery_project/urls.py`，将路径前缀委托给各 app：

- `/admin/` → Django Admin
- `/accounts/` → `accounts.urls`
- `/restaurants/` → `restaurants.urls`
- `/cart/` 或 `/carts/` → `carts.urls`
- `/orders/` → `orders.urls`
- `/merchants/` → `merchants.urls`
- `/reviews/` → `reviews.urls`

静态与媒体由 Django 在开发环境提供；生产环境通常由 Nginx 等反向代理处理 `/static/` 与 `/media/`。

---

## 6. 数据库与存储

- **数据库**：默认使用 SQLite（`settings.py` 中 `DATABASES`）。生产可改为 PostgreSQL/MySQL 等，仅改配置即可。
- **静态文件**：`STATIC_URL`、`STATICFILES_DIRS` 指向 `static/`，用于 CSS、JS、图片。
- **媒体文件**：`MEDIA_URL`、`MEDIA_ROOT` 指向 `media/`，用于用户上传（如头像、菜品图）。

---

## 7. 安全与运行

- **SECRET_KEY**：生产环境必须从环境变量读取，不要提交到版本库。
- **DEBUG**：生产环境设为 `False`。
- **ALLOWED_HOSTS**：生产环境需配置实际域名/IP。
- **运行开发服务器**：`python manage.py runserver`。
- **生产部署**：使用 `food_delivery_project.wsgi.application` 配合 Gunicorn/uWSGI 等 WSGI 服务器。

---

## 8. 与设计文档的对应关系

- **M1**：用户认证 → accounts  
- **M2**：餐厅与菜单浏览 → restaurants  
- **M3**：购物车 → carts  
- **M4 / M5**：订单与结账、订单状态 → orders  
- **C1 / C2**：评价与收藏、商家管理 → reviews, merchants  
- **S1 / S2**：评价与收藏相关 → reviews  

本架构满足「**后端必须使用 Python 与 Django 构建**」的约束，并保持模块清晰、便于扩展与协作开发。
