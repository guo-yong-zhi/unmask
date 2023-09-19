两个英语教辅编辑的工具。
# 完形填空
点击[这里](https://mybinder.org/v2/gh/guo-yong-zhi/holly-editor/main?urlpath=%2Fvoila%2Frender%2Fsrc%2FHolly%20Cloze.ipynb)在线使用，离线使用方法见下文。
## 功能
* 可以设置`top_k`, `split_stences`, `single_mask`
* 挖空的词可以用数字或下划线`_`开头，如：`It's a _great tool` 或 `It's 1pretty 2useful`
* 挖空的词也可以用中括号指定词性，`|`表示逻辑或，如：`it is a [RB] useful __.` 或 `[NN|PRP] is [adj]`
* 默认自动补全末尾句号，如不希望补全，在末尾加反斜杠\，如：`I am _`和`I am _\`的区别
* 当输入是完整句子而非短语时效果会更好，整段话或者整篇文章亦可。`split_stences`控制自动拆分成单句或段落多次输入

# 超纲词检测
点击[这里](https://mybinder.org/v2/gh/guo-yong-zhi/holly-editor/main?urlpath=%2Fvoila%2Frender%2Fsrc%2FWords%20Excluded.ipynb)在线使用，离线方法见下文。
## 功能
支持检测文章中各年级的超纲词汇。
# 离线使用
## windows平台
先克隆本项目，然后下载打包好的环境[holly-environment.tar.gz](https://github.com/guo-yong-zhi/holly-editor/releases/tag/win-pack)到项目根目录，不必解压。或者在项目根目录依次执行`packenv.cmd`中的命令可以自行完成环境安装和打包。最后点击`StartUp Holly Cloze.exe`或者`StartUp Word Excluded.exe`启动。
## Linux平台
`conda env create -f environment.yml`安装环境。`voila "src/Holly Cloze.ipynb"`或`voila "src/Words Excluded.ipynb"`启动应用。暂时没有打包好的环境。