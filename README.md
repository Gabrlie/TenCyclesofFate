# 《浮生十梦》

**《浮生十梦》** 是一款基于 Web 的沉浸式文字冒险游戏。玩家在游戏中扮演一个与命运博弈的角色，每天有十次机会进入不同的“梦境”（即生命轮回），体验由 AI 动态生成的、独一无二的人生故事。游戏的核心在于“知足”与“贪欲”之间的抉择：是见好就收，还是追求更高的回报但可能失去一切？

## ✨ 功能特性

- **动态 AI 生成内容**:每一次游戏体验都由大型语言模型（如 GPT）实时生成，确保了故事的独特性和不可预测性。
- **实时交互**: 通过 WebSocket 实现前端与后端的实时通信，提供流畅的游戏体验。
- **OAuth2 认证**: 集成 Linux.do OAuth2 服务，实现安全便捷的用户登录。
- **精美的前端界面**: 采用具有“江南园林”风格的 UI 设计，提供沉浸式的视觉体验。
- **互动式判定系统**: 游戏中的关键行动可能触发“天命判定”。AI 会根据情境请求一次 D100 投骰，其“成功”、“失败”、“大成功”或“大失败”的结果将实时影响叙事走向，增加了游戏的随机性和戏剧性。
- **智能反作弊机制**: 内置一套基于 AI 的反作弊系统。它会分析玩家的输入行为，以识别并惩罚那些试图使用“奇巧咒语”（如 Prompt 注入）来破坏游戏平衡或牟取不当利益的玩家，确保了游戏的公平性。
- **数据持久化**: 游戏状态会定期保存，并在应用重启时加载，保证玩家进度不丢失。

## 🛠️ 技术栈

- **后端**:
  - **框架**: FastAPI
  - **Web 服务器**: Uvicorn
  - **实时通信**: WebSockets
  - **认证**: Python-JOSE (JWT), Authlib (OAuth)
  - **数据库**: SQLite (用于存储兑换码)
  - **AI 集成**: OpenAI API
  - **依赖管理**: uv / pip

- **前端**:
  - **语言**: HTML, CSS, JavaScript (ESM)
  - **库**:
    - `marked.js`: 用于在前端渲染 Markdown 格式的叙事文本。
    - `pako.js`: 用于解压缩从 WebSocket 服务器接收的 Gzip 数据，提高传输效率。

## 🚀 快速开始

### 方式一：Docker 部署（推荐）

```bash
# 1. 克隆项目
git clone https://github.com/Gabrlie/TenCyclesofFate.git
cd TenCyclesofFate

# 2. 配置环境变量（复制并编辑 .env 文件）
cp .env.example .env
# 编辑 .env 文件，至少需要设置 OPENAI_API_KEY 和 SECRET_KEY

# 3. 一键启动
docker compose up -d
```

访问 `http://localhost:8000` 开始游戏！

**停止服务：**
```bash
docker compose down
```

**查看日志：**
```bash
docker compose logs -f
```

---

### 方式二：本地开发部署

适合需要修改代码或本地开发的情况。

#### 1. 环境准备

- **Python 3.8+**
- **Git**
- **pip** 或 **uv**（推荐）

#### 2. 安装依赖

```bash
# 克隆项目
git clone https://github.com/Gabrlie/TenCyclesofFate.git
cd TenCyclesofFate

# 安装依赖
pip install -r backend/requirements.txt
# 或使用 uv（更快）
uv pip install -r backend/requirements.txt
```

#### 3. 配置环境变量

```bash
# 复制配置文件
cp .env.example .env

# 编辑配置文件
# OPENAI_API_KEY=你的OpenAI密钥
# SECRET_KEY=使用 openssl rand -hex 32 生成
nano .env  # 或使用你喜欢的编辑器
```

#### 4. 运行应用

```bash
# 方式 A：使用启动脚本
chmod +x run.sh
./run.sh

# 方式 B：直接使用 uvicorn
cd backend
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

访问 `http://localhost:8000` 开始游戏！

---

## ⚙️ 配置说明

所有配置项都在 `.env` 文件中管理。以下是关键配置项：

### 必填配置

| 配置项 | 说明 | 示例 |
|--------|------|------|
| `OPENAI_API_KEY` | OpenAI API 密钥 | `sk-...` |
| `SECRET_KEY` | JWT 签名密钥（必须是随机字符串） | 使用 `openssl rand -hex 32` 生成 |

### 可选配置

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `OPENAI_BASE_URL` | OpenAI API 地址（可用于代理） | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 主模型 | `gpt-4o` |
| `OPENAI_MODEL_CHEAT_CHECK` | 作弊检查模型 | `gpt-3.5-turbo` |
| `LINUXDO_CLIENT_ID` | Linux.do OAuth ID（可选） | - |
| `LINUXDO_CLIENT_SECRET` | Linux.do OAuth 密钥（可选） | - |
| `ENABLE_LINUXDO_OAUTH` | 是否启用 Linux.do OAuth 登录 | `true` |
| `ENABLE_LOCAL_LOGIN` | 是否启用站内账号登录 | `true` |
| `DATABASE_URL` | 数据库连接地址 | `sqlite:///data/tencyclesoffate.db` |
| `ENABLE_LOCAL_REGISTRATION` | 是否允许站内账号注册（需先开启账号登录） | `true` |
| `PORT` | 服务端口 | `8000` |
| `EXTERNAL_PORT` | Docker 外部端口 | `8000` |

**注意：**
- Docker 部署会自动使用 SQLite 数据库，数据保存在 `./data` 目录
- `SECRET_KEY` 务必修改为随机字符串，否则存在安全风险

---

## 🎮 使用指南

### 首次使用

1. **访问游戏**：在浏览器打开 `http://localhost:8000`
2. **注册账号**：
   - 点击"注册"标签
   - 点击"使用 Linux.do 登录"（需先配置 OAuth）
3. **开始游戏**：点击"开始第一次试炼"

### 数据持久化

- **Docker 部署**：数据自动保存在 `./data` 目录，即使容器重启数据也不会丢失
- **本地部署**：数据保存在配置的 `DATABASE_URL` 位置

---

## 🔧 高级配置

### 更改端口

编辑 `.env` 文件：
```bash
PORT=8080              # 应用端口
EXTERNAL_PORT=8080     # Docker 映射端口
```

### 启用 Linux.do OAuth 登录

1. 在 [Linux.do](https://linux.do/) 注册 OAuth 应用
2. 设置回调 URL：`http://你的域名:端口/callback`
3. 在 `.env` 中配置：
   ```bash
   LINUXDO_CLIENT_ID=你的ClientID
   LINUXDO_CLIENT_SECRET=你的ClientSecret
   ENABLE_LINUXDO_OAUTH=true
   ```

### 关闭注册或第三方登录

- 只允许既有账号登录：
  ```bash
  ENABLE_LOCAL_REGISTRATION=false
  ```
- 完全关闭 Linux.do 登录：
  ```bash
  ENABLE_LINUXDO_OAUTH=false
  ```
  关闭后前端入口和相关后端路由都会禁用。

- 禁用全部站内账号登录与注册：
  ```bash
  ENABLE_LOCAL_LOGIN=false
  ENABLE_LOCAL_REGISTRATION=false  # 可选，登录关闭时注册会自动失效
  ```
  生效后仅保留第三方登录（若启用）。

### 使用自定义 OpenAI API

支持使用代理或第三方兼容 API：
```bash
OPENAI_BASE_URL=https://your-proxy.com/v1
```

---

## 📋 常见问题

**Q: Docker 启动失败？**
- 检查 `.env` 文件是否存在且配置正确
- 检查端口 8000 是否被占用：`lsof -i :8000`
- 查看日志：`docker compose logs`

**Q: 如何重置数据？**
- Docker 部署：删除 `./data` 目录
- 本地部署：删除 `DATABASE_URL` 指定的数据库文件

**Q: 如何更新到最新版本？**
```bash
# Docker 部署
docker compose pull
docker compose up -d

# 本地部署
git pull
pip install -r backend/requirements.txt --upgrade
```

---

## 📁 项目结构

```
TenCyclesofFate/
├── .env.example            # 环境变量模板
├── .env                    # 环境变量配置（需自行创建）
├── docker-compose.yml      # Docker Compose 配置
├── Dockerfile              # Docker 镜像构建文件
├── run.sh                  # 本地启动脚本
├── README.md               # 本文档
├── STREAMING_UPDATE.md     # 流式输出更新说明
│
├── backend/                # 后端代码
│   ├── requirements.txt    # Python 依赖
│   └── app/
│       ├── main.py         # FastAPI 主入口
│       ├── config.py       # 配置管理
│       ├── auth.py         # 认证逻辑
│       ├── db.py           # 数据库操作
│       ├── game_logic.py   # 游戏逻辑
│       ├── openai_client.py # OpenAI 客户端
│       ├── websocket_manager.py # WebSocket 管理
│       ├── state_manager.py # 状态管理
│       ├── cheat_check.py  # 反作弊系统
│       ├── redemption.py   # 兑换码系统
│       ├── security.py     # 加密工具
│       ├── live_system.py  # 观战系统
│       └── prompts/        # AI 提示词
│
├── frontend/               # 前端代码
│   ├── index.html          # 游戏主页
│   ├── index.css           # 主页样式
│   ├── index.js            # 主页逻辑
│   ├── live.html           # 观战页面
│   ├── live.css            # 观战样式
│   └── live.js             # 观战逻辑
│
├── scripts/                # 工具脚本
│   ├── generate_token.py   # 生成测试 Token
│   └── init_db.py          # 初始化数据库
│
├── data/                   # 数据目录（自动创建）
│   ├── tencyclesoffate.db  # SQLite 数据库
│   └── game_states.json    # 游戏状态
│
└── logs/                   # 日志目录（自动创建）
```

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

## 📄 许可证

本项目采用 MIT 许可证。

## 🙏 致谢

- 原项目[CassiopeiaCode/TenCyclesofFate](https://github.com/CassiopeiaCode/TenCyclesofFate)
