<div align="center">

# 🌟 Spider Weibo Information

[![GitHub stars](https://img.shields.io/github/stars/Ethan-yian/spider_weibo_imformation?style=social)](https://github.com/Ethan-yian/spider_weibo_imformation/stargazers)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/)
[![Scrapy](https://img.shields.io/badge/scrapy-2.5+-green.svg)](https://scrapy.org/)
[![License](https://img.shields.io/badge/license-MIT-yellow.svg)](LICENSE)

🚀 一个强大的微博信息爬虫工具，让数据采集变得简单高效 

[English](README_EN.md) | 简体中文

</div>

## ✨ 特色功能

<table>
  <tr>
    <td>
      <h3>📊 数据采集</h3>
      <ul>
        <li>关键词搜索结果批量获取</li>
        <li>支持多种搜索条件组合</li>
        <li>智能数据去重处理</li>
        <li>断点续传功能</li>
      </ul>
    </td>
    <td>
      <h3>💾 存储方式</h3>
      <ul>
        <li>CSV 文件存储</li>
        <li>MySQL 数据库存储</li>
        <li>MongoDB 数据库存储</li>
        <li>自动文件管理</li>
      </ul>
    </td>
    <td>
      <h3>📁 媒体下载</h3>
      <ul>
        <li>原图下载功能</li>
        <li>视频内容下载</li>
        <li>自动分类存储</li>
        <li>失败重试机制</li>
      </ul>
    </td>
  </tr>
</table>

## 🎯 数据字段

### 基础信息
- 🆔 微博ID与BID
- 📝 微博文本内容
- ⏰ 发布时间信息
- 📍 地理位置数据
- 📱 发布平台来源

### 统计指标
- ❤️ 点赞数据统计
- 🔄 转发互动数据
- 💬 评论数量统计

### 多媒体内容
- 🖼️ 图片资源链接
- 🎥 视频内容地址
- 📰 头条文章链接

### 社交数据
- #️⃣ 话题标签收集
- @ 用户提及统计
- ✅ 用户认证信息

## 🚀 快速开始

### 1️⃣ 安装部署
```bash
# 克隆项目
git clone https://github.com/Ethan-yian/spider_weibo_imformation.git
cd spider_weibo_imformation

# 安装依赖
pip install -r requirements.txt
```

### 2️⃣ 配置文件
```python
# settings.py 核心配置

# 必需配置
WEIBO_COOKIE = 'your_cookie_here'  # 微博Cookie
KEYWORD_LIST = ['关键词1', '关键词2']  # 搜索关键词

# 可选配置
START_DATE = '2025-01-01'  # 起始日期
END_DATE = '2025-12-31'    # 结束日期
DOWNLOAD_DELAY = 2         # 请求间隔(秒)
```

### 3️⃣ 运行爬虫
```bash
# 开始采集数据
scrapy crawl weibo_search

# 启用断点续传
scrapy crawl weibo_search -s JOBDIR=crawls/weibo_search
```

## 📋 高级配置

### 数据过滤
```python
# 微博类型过滤
WEIBO_TYPE = {
    0: '全部微博',
    1: '原创微博',
    2: '热门微博',
    3: '关注人微博',
    4: '认证用户微博',
    5: '媒体微博'
}

# 内容类型过滤
CONTAIN_TYPE = {
    0: '全部',
    1: '图片',
    2: '视频',
    3: '音乐',
    4: '文章'
}
```

### 存储配置
```python
ITEM_PIPELINES = {
    'weibo.pipelines.DuplicatesPipeline': 300,    # 去重
    'weibo.pipelines.CsvPipeline': 301,           # CSV存储
    'weibo.pipelines.MysqlPipeline': 302,         # MySQL存储
    'weibo.pipelines.MongoDBPipeline': 303,       # MongoDB存储
    'weibo.pipelines.MediaPipeline': 304          # 媒体下载
}
```

## 🔍 Cookie获取指南

<details>
<summary>展开查看详细步骤</summary>

1. 打开Chrome浏览器，访问 https://weibo.com/
2. 完成微博账号登录
3. 按F12打开开发者工具
4. 选择 Network → Headers → Request Headers
5. 找到并复制完整的Cookie值

![Cookie获取示意图](https://user-images.githubusercontent.com/41314224/144813569-cfb5ad32-22f0-4841-afa9-83184b2ccf6f.png)

</details>

## ⚠️ 注意事项

- 请遵守微博平台的使用条款和政策
- 建议合理设置请求间隔，避免频繁访问
- 定期更新Cookie以确保正常运行
- 注意数据的安全存储和保护

## 📈 项目计划

- [ ] 支持代理IP池
- [ ] 添加用户信息采集
- [ ] 评论数据获取
- [ ] 数据可视化界面
- [ ] 分布式采集支持

## 🙏 致谢

特别感谢 [@dataabc](https://github.com/dataabc) 的 [weibo-search](https://github.com/dataabc/weibo-search) 项目，为本项目提供了重要的参考。

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

<div align="center">

### 如果这个项目对你有帮助，请考虑给它一个星星 ⭐️

</div>