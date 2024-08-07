# 机场签到脚本（多账号版）

这是一个用于自动签到机场网站的 Python 脚本，支持多个账号，并能够合并多个订阅链接。

> 本脚本适用于所有 Powered by SSPANEL 的机场网站。要确认是否是 Powered by SSPANEL，请查看机场网站首页底部。示例如下：

![SSPANEL示例](https://user-images.githubusercontent.com/21276183/214764546-4f66333a-cb9b-420e-8260-697d26fb4547.png)

## 功能特性

- 支持多账号签到
- 自动获取并合并订阅链接
- 使用 [Server 酱](https://sct.ftqq.com/r/13569) 进行消息推送
- 支持 GitHub Actions 自动运行

## 配置说明

本脚本使用 GitHub Actions 的 Secrets 和 Variables 进行配置。您需要在 GitHub 仓库中设置以下内容：

### 设置 Secrets（用于敏感信息）

1. 在您的 GitHub 仓库页面，点击 "Settings"。
2. 在左侧菜单中，点击 "Secrets and variables"，然后选择 "Actions"。
3. 在 "Secrets" 标签下，点击 "New repository secret"。
4. 添加以下 Secrets：

   a. `ACCOUNTS`：包含多个账号信息的 JSON 字符串
   - Name: ACCOUNTS
   - Value: 
     ```json
     [
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
     ```

   b. `SCKEY`：Server 酱的 SCKEY（可选）
   - Name: SCKEY
   - Value: 您的 SCKEY

5. 对于每个 Secret，填写完信息后点击 "Add secret"。

注意：请确保 JSON 格式正确，且不包含多余的空格或换行。

## 使用方法

### 1. Fork 本仓库

点击本仓库页面右上角的 "Fork" 按钮，将仓库复制到您的 GitHub 账户下。

### 2. 配置 Secrets

按照上述 "配置说明" 部分的步骤在您 Fork 的仓库中设置 Secrets。

### 3. 启用 GitHub Actions

1. 在您 Fork 的仓库中，点击 "Actions" 标签。
2. 如果 Actions 未启用，您会看到一个启用按钮，点击它以启用 Actions。
3. 在左侧的工作流列表中，找到并选择 "Checkin"（或您的工作流名称）。
4. 点击 "Enable workflow" 按钮启用工作流。

GitHub Actions 将根据预设的时间表自动运行脚本。您也可以手动触发工作流运行。

## 本地运行

如果您想在本地运行脚本，请按以下步骤操作：

1. 克隆仓库到本地：
   ```bash
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 设置环境变量：
   在运行脚本之前，请确保设置了 `ACCOUNTS` 和 `SCKEY`（可选）环境变量。

4. 运行脚本：
   ```bash
   python main.py
   ```

## 注意事项

- 请确保您的 Secrets 格式正确，且包含所有必要信息。
- 使用 GitHub Actions 时，请遵守相关服务条款和使用规范。
- 本脚本仅用于学习和研究目的，请勿用于非法用途。
- 如果您想使用 [Server 酱](https://sct.ftqq.com/r/13569) 进行消息推送，请先注册并获取 SCKEY。

## 致谢

本项目基于 [bighammer-link/jichang_checkin](https://github.com/bighammer-link/jichang_checkin) 修改而来，增加了多账号支持和订阅合并功能。