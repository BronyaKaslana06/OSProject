## 文件结构

一份readme文件简单介绍如何运行项目和项目的基本信息

说明文档.docx是作业的一部分，详细介绍了项目的实现

localFile是文件系统保存在磁盘上的数据

FileSystem.exe是用pyInstaller封装好的可执行文件

static文件夹中是项目需要的静态图片资源

FileSystemClass.py和FileSystemMainUI.py是项目的代码文件

演示视频.mp4是项目的演示视频

## 运行

安装相关包

```Shell
pip install PyQt5
pip install bitarray
pip install qt-material
```

安装好依赖包后运行FileSystemMainUI.py

```bash
python FileSystemMainUI.py
```

也可以直接运行用pyInstaller打包后的文件FileSystem.exe。不过仍然建议配置好环境后在python环境中运行。
