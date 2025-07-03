# GitHub 远程仓库连接指南
1. 安装 Git
2. 配置用户名邮箱
3. 生成并添加 SSH 密钥
4. 测试连接
5. 克隆或添加远程仓库
6. 拉取、提交、推送代码

---

## 一、安装 Git

- 从 [git-scm.com](https://git-scm.com) 下载并安装 Git。

---

## 二、配置 Git 用户信息（只需设置一次）

```bash
git config --global user.name "你的用户名"
git config --global user.email "你的邮箱"
```

> 用于让 Git 知道你是谁，提交记录会使用该信息。

## 三、在特定仓库中设置局部 Git 用户信息

在项目文件夹中运行：

```bash
git config user.name "你的用户名"
git config user.email "你的邮箱"
```

> 这只影响当前仓库的配置。

---

## 四、查看当前仓库的 Git 配置

```bash
git config --list --show-origin
```

> 显示所有配置项，包括局部和全局配置。

### 小贴士

- `--global` 是全局配置（对所有仓库生效）。
- 不加 `--global` 是本地配置（只对当前仓库生效）。

---

## 五、生成 SSH 密钥并添加到 GitHub（推荐方式）

1. **生成 SSH 密钥**：
   
   ```bash
   ssh-keygen -t ed25519 -C "邮箱@example.com"
   ```
   
   > 默认保存在 `~/.ssh/id_ed25519`或`/home/你的用户名/.ssh/id_ed25519`。
   > 可自定义路径以保存不同账号的密钥。
   > 可设置密码
2. **添加 SSH 密钥到 ssh-agent**：
   
   ```bash
   eval "$(ssh-agent -s)"
   ssh-add ~/.ssh/id_ed25519
   ```
3. **复制公钥内容**：
   
   ```bash
   cat ~/.ssh/id_ed25519.pub
   ```
4. **登录 GitHub**
   
   - 右上角头像 → Settings → SSH and GPG keys → New SSH key → 粘贴公钥。

---

## 六、测试 SSH 连接是否成功

```bash
ssh -T git@github.com
```

> 如果看到欢迎信息，说明连接成功。

---

## 七、克隆远程仓库或添加远程地址

- **克隆仓库**（首次）：
  
  ```bash
  git clone git@github.com:用户名/仓库名.git
  ```
- **已有本地项目，添加远程地址**：
  
  ```bash
  git remote add origin git@github.com:用户名/仓库名.git
  ```

---

## 八、拉取、提交、推送代码

```bash
git pull origin main       # 拉取远程主分支（可能是 main 或 master）
git add .                  # 添加所有更改
git commit -m "提交说明"   # 提交更改
git push origin main       # 推送到远程主分支
```

## 九、可选：设置默认推送分支

```bash
git push --set-upstream origin main
```

---

# 回滚代码

1. 查询要回滚的 `commit_id`：
   
   ```bash
   git log
   ```
2. 回滚操作：
   
   ```bash
   git reset --hard commit_id
   git push origin HEAD --force
   ```

---

# 作者信息设置

- 查看当前配置：
  ```bash
  git config --list
  ```
- 重置本项目用户信息：
  ```bash
  git config user.name '用户名'
  git config user.email '邮箱'
  ```

---

# 显示当前仓库关联的远程仓库地址。

```bash
git remote -v
```

---

# 手动关联本地文件夹

1. 初始化本地仓库：
   
   ```bash
   git init
   ```
2. 关联远程仓库：
   
   ```bash
   git remote add origin https://github.com/你的用户名/仓库名.git
   ```
3. 拉取远程内容并合并：
   
   ```bash
   git pull origin main --allow-unrelated-histories
   ```
4. 添加文件并提交：
   
   ```bash
   git add .
   git commit -m "初始提交"
   git push origin main
   ```

---

# 删除最近的 commit

```bash
git reset --soft HEAD~1 # 保持改动，回到暂存区
git reset --mixed HEAD~1 # 保持改动，回到工作区
git reset --hard HEAD~1 # 改动也删除
```

---

# Git 的基本步骤和命令

### 1. 初始化 Git 仓库

```bash
git init
```

### 2. 添加文件到暂存区

```bash
git add <文件名> 
# 或者添加所有文件
git add .
```

### 3. 提交更改

```bash
git commit -m "提交信息"
```

### 4. 查看仓库状态

```bash
git status
```

### 5. 查看提交历史

```bash
git log
```

### 6. 创建和切换分支

- 创建新分支：

```bash
git branch <分支名>
```

- 切换分支：

```bash
git checkout <分支名>
```

### 7. 合并分支

```bash
git merge <分支名>
```

### 8. 添加远程仓库

```bash
git remote add origin <远程仓库URL>
```

### 9. 推送到远程仓库

```bash
git push -u origin <分支名>
```

### 10. 拉取远程仓库的更改

```bash
git pull origin <分支名>
```

### 11. 克隆远程仓库

```bash
git clone <远程仓库URL>
```

---

# 使用子模块引入 Git 仓库

### 步骤

1. 进入小组的主项目仓库：
   
   ```bash
   git clone https://github.com/yourgroup/project.git
   cd project
   ```
2. 添加子模块：
   
   ```bash
   git submodule add https://github.com/yourname/your-repo.git 子模块路径
   ```
3. 提交子模块信息：
   
   ```bash
   git add .gitmodules modules/your-repo
   git commit -m "Add your-repo as submodule"
   git push
   ```

---

# 冲突处理

当本地分支落后于远程分支，需先拉取再推送：

```bash
git pull origin main --rebase
git push origin main
```

---

