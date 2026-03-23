# job-hunt-jp

使用 Claude Code 管理日本企业求职活动的个人数据库模板。
日本企業への求職活動を Claude Code で管理する個人データベーステンプレートです。

---

## 开始使用（零基础版）
如果使用过github的朋友们可以跳过这个步骤，用自己觉得方便的方式使用。

### Step 1：下载这个项目

1. 点击页面右上角绿色的 **Code** 按钮
2. 点 **Download ZIP**
3. 解压，得到一个叫 `job-hunt-jp` 的文件夹

### Step 2：安装 Claude Code

还没有 Claude Code 的话，打开终端运行：

```bash
npm install -g @anthropic-ai/claude-code
```

> 没有 npm？先安装 Node.js：[nodejs.org](https://nodejs.org)（下载 LTS 版本，一路点安装即可）

### Step 3：用 Claude Code 打开这个文件夹

打开终端，运行：

```bash
cd 你解压后的文件夹路径/job-hunt-jp
claude
```

### Step 4：填写你的个人信息

用任意文本编辑器打开 `profile.md`，按照里面的格式填入你的：
- 学历・毕业时间
- 语言能力
- 工作经历
- 目标职位和行业

### Step 5：开始用

在 Claude Code 里直接输入中文就行，例如：

```
帮我调查一下索尼集团，看看适不适合我
```

Claude 会自动读取你的 `profile.md`，调查公司并生成档案。

---

## 能做什么

| 说什么 | Claude 会做什么 |
|--------|---------------|
| 「帮我调查○○公司」 | 调查基本信息・招募情况・企业文化，生成档案，按难度分级 |
| 「○○投完了」 | 更新进度 → 自动调查面试经验 → 制作面试方案 |
| 「帮我更新所有公司的信息」 | 重新搜索最新动态，更新档案 |
| 「导出成 Excel」 | 生成求职进度表 |

---

## 文件结构

```
job-hunt-jp/
├── profile.md          ← 你的个人信息（必填）
├── README.md           ← 本说明文件
├── tracker.md          ← 求职进度追踪表
├── CLAUDE.md           ← Claude 的操作指令（不需要改）
├── export_excel.py     ← Excel 导出脚本
└── companies/
    └── _template.md    ← 公司档案模板
```

---

## Tier 分级说明

Claude 会根据你的背景，把每家公司分为四个级别：

| Tier | 意思 |
|------|------|
| A | 有效路线 2 条以上，现在就可以动 |
| B | 有路线，但存在一定障壁 |
| C | 有空缺才能投，需要等待 |
| D | 中长期目标，需要先积累经验 |
