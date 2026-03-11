---
name: utility-speedtest
description: 网络速度测试工具，支持延迟测试、下载速度、上传速度测试。完全本地测试，无需 API。适用于网络诊断、带宽测试。Use when: 用户需要测试网络速度。
---

# 网络速度测试

## 🌐 核心功能

- ✅ **延迟测试** - 测试到目标的延迟
- ✅ **下载速度** - 测试下载带宽
- ✅ **上传速度** - 测试上传带宽
- ✅ **完整测试** - 一键测试所有项目

## 📖 使用方法

### 延迟测试

```
测试到 Google 的延迟
```

**脚本调用：**
```bash
python scripts/speedtest.py latency
python scripts/speedtest.py latency 8.8.8.8 53 4
```

### 下载速度测试

```
测试下载速度
```

**脚本调用：**
```bash
python scripts/speedtest.py download
```

### 上传速度测试

```
测试上传速度
```

**脚本调用：**
```bash
python scripts/speedtest.py upload
```

### 完整测试

```
完整网络测试
```

**脚本调用：**
```bash
python scripts/speedtest.py full
```

## 📊 输出示例

### 延迟测试
```
🌐 延迟测试

目标：8.8.8.8:53
测试次数：4
成功：4
失败：0

平均延迟：25.34ms
最小：23.12ms
最大：28.45ms
```

### 下载速度
```
📥 下载速度测试

目标：http://speedtest.tele2.net/1MB.zip
时长：5.02s
下载：1250.5KB

速度：1.99 Mbps
```

### 完整测试
```
🌐 完整网络测试

1️⃣ 延迟测试...
平均延迟：25.34ms

2️⃣ 下载速度测试...
速度：1.99 Mbps
```

## 💡 使用技巧

- 延迟越低越好（<50ms 优秀）
- 下载速度受服务器限制
- 多次测试取平均值
- 选择近端测试服务器更准确

## 📈 速度参考

| 用途 | 最低速度 | 推荐速度 |
|------|---------|---------|
| 网页浏览 | 1 Mbps | 5 Mbps |
| 视频 720p | 3 Mbps | 5 Mbps |
| 视频 1080p | 5 Mbps | 10 Mbps |
| 视频 4K | 25 Mbps | 50 Mbps |
| 在线游戏 | 3 Mbps | 10 Mbps |

---

**作者：** 白虎 🐯  
**版本：** 1.0  
**许可证：** MIT
