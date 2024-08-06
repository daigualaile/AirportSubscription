# 机场签到脚本（多账号版）

这是一个用于自动签到机场网站的 Python 脚本，支持多个账号，并能够合并多个订阅链接。

## 功能特性

- 支持多账号签到
- 自动获取并合并订阅链接
- 使用 Server 酱进行消息推送
- 支持 GitHub Actions 自动运行

## 使用方法

### 1. 配置文件

在项目根目录创建 `config.json` 文件，格式如下：

```json
{
  "SCKEY": "YOUR_SCKEY_HERE",
  "accounts": [
    {
      "url": "https://example1.com",
      "email": "user1@example.com",
      "passwd": "password1"
    },
    {
      "url": "https://example2.com",
      "email": "user2@example.com",
      "passwd": "password2"
    }
  ]
}
```

- `SCKEY`：Server 酱的 SCKEY（可选）
- `accounts`：包含多个账号信息的数组
  - `url`：机场网站的 URL
  - `email`：登录邮箱
  - `passwd`：登录密码

### 2. 安装依赖

```bash
pip install requests beautifulsoup4
```

### 3. 运行脚本

```bash
python main.py
```

## GitHub Actions 自动运行

1. Fork 本仓库
2. 在 Fork 后的仓库中添加以下 Secrets：
   - `CONFIG`：将 `config.json` 的内容作为字符串添加
3. 启用 GitHub Actions

## 注意事项

- 请确保您的配置文件格式正确，且包含所有必要信息。
- 使用 GitHub Actions 时，请遵守相关服务条款和使用规范。
- 本脚本仅用于学习和研究目的，请勿用于非法用途。

## 致谢

本项目基于 [bighammer-link/jichang_checkin](https://github.com/bighammer-link/jichang_checkin) 修改而来，增加了多账号支持和订阅合并功能。