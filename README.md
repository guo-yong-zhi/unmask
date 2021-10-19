# unmask
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/guo-yong-zhi/unmask/main?urlpath=%2Fvoila%2Frender%2FUnmaskApp.ipynb)
* 可以设置`top_k`, `split_stences`, `single_mask`
* 挖空的词可以用数字或下划线`_`开头，如：`It's a _great tool` 或 `It's 1pretty 2useful`
* 挖空的词也可以用中括号指定词性，`|`表示逻辑或，如：`it is a [RB] useful __.` 或 `[NN|PRP] is [adj]`
* 默认自动补全末尾句号，如不希望补全，在末尾加反斜杠\，如：`I am _`和`I am _\`的区别
* 当输入是完整句子而非短语时效果会更好，整段话或者整篇文章亦可。`split_stences`控制自动拆分成单句或段落多次输入

点击[这里](https://mybinder.org/v2/gh/guo-yong-zhi/unmask/main?urlpath=%2Fvoila%2Frender%2FUnmaskApp.ipynb)在线使用，或者  
如果是windows平台，可以下载打包好的环境[unmask-environment.tar.gz](https://github.com/guo-yong-zhi/unmask/releases/tag/win-pack)到项目根目录，不必解压（或者依次执行`packenv.cmd`中的命令自行打包），然后点击`StartUp.exe`启动
