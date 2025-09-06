# Git 與 SSH 操作指南

## 1. Git 基礎操作

### 1.1 初始化本地版本庫
```bash
git init
```
此命令用於在當前目錄創建一個新的Git版本庫。

## 2. SSH 協議介紹

### 2.1 什麼是 SSH？
SSH（Secure Shell，安全外殼協議）是由IETF網路工作小組制定的協議。SSH是目前最可靠的協議，專為遠程登錄會話和其他網路服務提供安全性。使用SSH協議可以有效防止遠程管理過程中的信息洩露問題。

### 2.2 基於密鑰的安全驗證原理
使用SSH協議通信時，建議使用基於密鑰的驗證方式：

1. **創建密鑰對**：用戶需要為自己創建一對密鑰（公鑰和私鑰）
2. **部署公鑰**：將公鑰放在需要訪問的服務器上
3. **驗證流程**：
   - 客戶端向SSH服務器發出請求，請求使用密鑰進行安全驗證
   - 服務器在用戶主目錄下尋找公鑰，並與客戶端發送的公鑰進行比較
   - 如果兩個密鑰一致，服務器用公鑰加密"質詢"並發送給客戶端
   - 客戶端用私鑰解密"質詢"並發送回服務器完成驗證

## 3. Git 與 GitHub 的 SSH 配置

### 3.1 生成 SSH 密鑰對
```bash
ssh-keygen -t rsa
```

執行此命令後，會在 `~/.ssh` 目錄下生成以下文件：
- `id_rsa`：私鑰（需要保密）
- `id_rsa.pub`：公鑰（可以公開）

### 3.2 配置 GitHub SSH 密鑰
1. 複製 `id_rsa.pub` 文件的內容
2. 登錄 GitHub
3. 前往：頭像 → Settings → SSH and GPG keys
4. 添加新的 SSH 密鑰，貼上公鑰內容

### 3.3 建立本地倉庫與 GitHub 的連接
```bash
git remote add origin git@github.com:Benson0418/myFoobarRepo.git
```

### 3.4 推送代碼到 GitHub
```bash
git push -u origin master
```
- `-u` 參數用於設置上游分支
- 首次推送後，之後可以直接使用 `git push`

## 4. Git 操作方式比較

### 4.1 SSH 方式
**優點**：
- 安全性高，使用密鑰驗證
- 一次配置，後續操作無需輸入密碼

**克隆示例**：
```bash
git clone git@github.com:d36351/d36351.github.io.git
```

### 4.2 HTTPS 方式
**特點**：
- 每次推送可能需要輸入用戶名和密碼
- 適合臨時或簡單的操作

**克隆示例**：
```bash
git clone https://github.com/username/repository.git
```

## 5. 常用 Git 工作流程

1. **初始化或克隆倉庫**
2. **添加遠程倉庫**（如果是本地初始化）
3. **進行代碼修改**
4. **添加到暫存區**：`git add .`
5. **提交更改**：`git commit -m "提交信息"`
6. **推送到遠程倉庫**：`git push`

---

**注意事項**：
- 私鑰文件（`id_rsa`）必須保密，不能共享
- 建議為不同的服務使用不同的SSH密鑰
- 定期檢查和更新SSH密鑰