# Finance-Education 的 Windows 兼容副本

处理日期：2026-10-06。

原始仓库：[engineerinvestor/Finance-Education](https://github.com/engineerinvestor/Finance-Education)。

原始 Git 提交：63a6ea4597f7967ad70821748a3af6bb76a15062。

原始文件名：Portfolio_Switch_When_Does_it_Pay_Off?_A_Break_Even_Analysis.ipynb。

该文件名包含 Windows 不支持的问号。在 Windows 普通检出会失败。初始化脚本完整克隆原仓库，并仅将这一文件排除在 Windows 工作区之外；其他 6 个文件正常检出，Git 历史与原始文件对象均保留。

## 可打开的副本

兼容副本由 scripts/bootstrap.py 在本机生成，文件名为 Portfolio_Switch_When_Does_it_Pay_Off_A_Break_Even_Analysis.ipynb。公共仓库保留 [原始上游 Notebook](https://github.com/engineerinvestor/Finance-Education/blob/63a6ea4597f7967ad70821748a3af6bb76a15062/Portfolio_Switch_When_Does_it_Pay_Off%3F_A_Break_Even_Analysis.ipynb) 的引用，不重新发布副本。

副本来自上述提交的原始 Git blob，只去掉文件名中的问号，未修改 Notebook 内容。

- 文件大小：91,892 字节。
- SHA-256：87c10289c46908fc5aa1d6cf7f24e16528166b5b098192c1b55a23e706e118ef。
- Notebook 格式：nbformat 4，共 6 个单元格。
- 内容验证：副本与原 Git blob 逐字节相等；已验证 JSON 可解析，尚未执行 Notebook。

## 原仓库的检出方式

本地稀疏检出采用以下模式：

    /*
    !/Portfolio_Switch_When_Does_it_Pay_Off?_A_Break_Even_Analysis.ipynb

初始化后保留原仓库 origin 与完整历史，检出清单中的固定提交，工作区干净。已有同版本仓库会被保留。没有提交重命名改动，也没有修改全局 Git 设置。

脚本仅在新创建且已核对固定版本的仓库上，为具体检出命令临时使用 core.protectNTFS=false；该设置不会持久保存。后续不要直接关闭稀疏检出，否则 Windows 会再次尝试创建非法路径。若更新后的上游新增其他非法文件名，应先检查路径，再调整排除和副本映射。

副本在原仓库之外，因此在此练习不会改变上游工作区状态。原始 Notebook 保留了作者的内容与来源，学习计划中把它作为组合切换专题使用。
