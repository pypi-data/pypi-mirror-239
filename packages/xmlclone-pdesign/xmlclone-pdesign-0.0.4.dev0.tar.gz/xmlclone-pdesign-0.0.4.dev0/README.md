[![PyPI](https://img.shields.io/pypi/v/xmlclone-pdesign.svg)](https://pypi.org/project/xmlclone-pdesign/)
[![PyPI](https://img.shields.io/pypi/pyversions/linlei04-pdesign.svg)](https://pypi.org/project/xmlclone-pdesign/)
[![PyPI - Implementation](https://img.shields.io/pypi/implementation/xmlclone-pdesign)](https://pypi.org/project/xmlclone-pdesign/)
[![license](https://img.shields.io/github/license/xmlclone/pdesign.svg)](https://github.com/xmlclone/pdesign/blob/main/LICENSE)
[![GitHub contributors](https://img.shields.io/github/contributors/xmlclone/pdesign.svg)](hhttps://github.com/xmlclone/pdesign/graphs/contributors)

# 说明

设计模式&常用算法的Python实现，本文环境如下:

```shell
$ cat /proc/version
Linux version 5.15.90.1-microsoft-standard-WSL2 (oe-user@oe-host) (x86_64-msft-linux-gcc (GCC) 9.3.0, GNU ld (GNU Binutils) 2.34.0.20200220) #1 SMP Fri Jan 27 02:56:13 UTC 2023

$ conda --version
conda 23.7.4

$ conda create -n vpdesign python=3.12 -y
$ conda activate vpdesign

$ python --version
Python 3.12.0

$ make --version
GNU Make 4.3
Built for x86_64-pc-linux-gnu
Copyright (C) 1988-2020 Free Software Foundation, Inc.
License GPLv3+: GNU GPL version 3 or later <http://gnu.org/licenses/gpl.html>
This is free software: you are free to change and redistribute it.
There is NO WARRANTY, to the extent permitted by law.
```

# Demo使用

```shell
# 安装
pip install xmlclone-pdesign
```

# 项目环境

```shell
# 创建并激活虚拟环境
conda create -n vpdesign python=3.12 -y
conda activate vpdesign

# 安装依赖
pip install -r requirements.txt

# 测试
make test

# 打包发布
make release
```

# 其它配置

## readthedocs

1. 登录[readthedocs](https://about.readthedocs.com/)
2. 导入本项目进行编译即可

## pypi

1. 当需要发布版本时，通过`git tag -a [version]`的方式创建版本并`git push --tags`推送到`git`
2. 通过`make release`即可发布到[pypi](https://pypi.org/)