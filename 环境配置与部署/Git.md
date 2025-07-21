# 当Git 本地仓库发生冲突时，需要手动解决。
1. 确认冲突:
当执行 git pull 或 git merge 等操作时，如果Git 检测到冲突，它会提示你哪些文件发生了冲突。
2. 打开冲突文件:
使用文本编辑器打开有冲突的文件。你会看到类似以下的标记：
Code

   <<<<<<< HEAD
   这是当前分支（HEAD）的代码
   =======
   这是另一个分支（例如，master）的代码
   >>>>>>> master
1. 解决冲突:
你需要仔细阅读冲突的部分，决定保留哪个版本，或者修改成新的版本。你可以删除不需要的部分，并修改冲突区域，最终形成一个正确版本。
2. 标记为已解决:
在解决冲突后，使用 git add <冲突文件> 命令将已解决的文件标记为已解决状态。
3. 提交更改:
使用 git commit 提交已解决的冲突。
4. 推送更改:
最后，使用 git push 将解决冲突后的代码推送到远程仓库。
总结: 解决Git 冲突需要手动干预，需要仔细分析代码，选择正确的版本，并标记为已解决状态，然后提交并推送。


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

要把 dev 分支的 10 个 commit 合并成一个提交到 main 上，可以用 git rebase 交互式变基 先整理提交历史，再合并到 main，步骤如下：

1. 确保 dev 分支是最新的

先拉取远程 main 的最新代码，避免冲突：
# 切到 main 分支，拉取最新更新
git checkout main
git pull origin main

# 切回 dev 分支，把 main 的最新代码合并到 dev（确保 dev 基于最新 main）
git checkout dev
git merge main
# 如果有冲突，解决后提交：git add . && git commit -m "解决合并冲突"
2. 交互式变基，把 10 个 commit 合并成 1 个

用 git rebase -i 操作最近的 10 个提交（HEAD~10 表示从当前 HEAD 往前数 10 个）：
git rebase -i HEAD~10
执行后会弹出编辑器，里面列出了这 10 个 commit（从上到下是旧到新）：
pick a1b2c3d 第一个提交信息
pick e4f5g6h 第二个提交信息
...
pick x7y8z9w 第十个提交信息
修改方式：

• 把第 2 到第 10 行的 pick 改成 squash（或缩写 s），表示“把这些提交合并到上一个提交”；

• 只保留第 1 行的 pick（作为合并后的根提交）。

修改后类似：
pick a1b2c3d 第一个提交信息
squash e4f5g6h 第二个提交信息
squash ... ...
...
squash x7y8z9w 第十个提交信息
保存退出编辑器，会进入第二个编辑界面，让你填写合并后的新提交信息（可以总结这 10 个提交的内容），填写后保存退出，变基完成。

3. 推送到 dev 分支（注意需要强制推送，因为修改了历史）

变基后提交历史改变，需要强制推送到远程 dev（如果之前推过）：
git push origin dev --force-with-lease  # 比 --force 更安全，避免覆盖别人的修改
4. 合并到 main 分支

最后把整理好的 dev 合并到 main，此时只会产生一个提交：
git checkout main
git merge dev  # 因为 dev 基于最新 main，这里通常是快进合并
git push origin main
这样操作后，main 分支上就只会有一个来自 dev 的合并提交，历史更整洁～ 如果中间遇到变基冲突，解决后用 git add . 标记 resolved，再 git rebase --continue 继续即可。

---

