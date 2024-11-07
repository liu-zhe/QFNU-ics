# QFNU-ics
曲阜师范大学课表自动生成，支持一键导入，兼容各种日历APP 

![preview.png](https://s2.loli.net/2024/11/07/9pAMsXE7HzcwQZP.png)

> 膜拜MoveToEx
# 功能

- 为你的课表生成跨平台可通用的`.ics`日历文件。可一键导入手机，平板电脑，笔记本电脑等移动设备，便于随时随地进行查看。

# 使用

## 准备工作

- 本代码需使用 **Python 3** 运行，建议 Python 版本在 3.7 以上。

## 生成ics文件

1. 在项目目录中运行`pip install -r requirements.txt`

2. 在项目目录中运行`python main.py`，输入你的账号密码，此时会弹出验证码图片，填写验证码

3. 此时目录中将会生成`output.ics`，该文件即为生成的ics文件

## 导入日历

### 微软日历

单击生成的`output.ics`，选择最上方「添加到日历」即可

### Android 手机日历

用QQ，微信等常用聊天软件将 ics 文件传至 Android 设备，之后在「打开方式」中选择「日历」，根据系统提示导入即可

### iOS 日历

iOS 日历导入方式较为繁琐，他人曾使用两种方式成功导入，供参考。

#### 方法1：使用NodeJS

1. 安装 [NodeJS](https://nodejs.org)

2. 在任一目录下运行`npm install http-server --global`

3. 在`output.ics`文件所在目录运行`http-server`

4. 使用Safari浏览器打开终端中显示的网址，通常形式为`http://*.*.*.*:*`，其中`*`为通配符

5. 在页面中找到`.ics`文件，点击打开，并根据系统提示导入日历

#### 方法2：使用文件传输网址

以[奶牛快传](https://cowtransfer.com/)为例。

1. 将 ics 文件传至奶牛快传。

2. 此时奶牛快传将会给出文件链接和提取码，点击「Copy both」进行复制，并通过QQ，微信等社交软件传至 iOS 设备。

3. 将文件链接复制到 Safari 浏览器中，输入提取码，点击「下载」。

4. 此时系统会自动弹出日程，单击右上角「添加全部」。

5. **这点十分重要！！！** 请点击右下角「添加日历」，输入日历名称并选中，之后点击「完成」。

**不要**直接点击完成，否则万一出错删除会非常麻烦。


# 其他

> 项目灵感来源于[FJNU-ics](https://github.com/payphone-x/FJNU-ics)，多谢MoveToEx的指导
