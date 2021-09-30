# unmask
[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/guo-yong-zhi/unmask/HEAD?urlpath=lab%2Ftree%2Funmask.ipynb)
* 打开unmask.ipynb
* 修改`text`字符串中的内容或者直接编辑`article.txt`
* 可以修改`top_k`, `split_stences`, `single_mask`的值
* 结果输出在`output.txt`
* 挖空的词可以用数字或下划线`_`开头，如：`It's a _great tool` 或 `It's 1pretty 2useful`
* 挖空的词也可以用中括号指定词性，`|`表示逻辑或，如：`it is a [RB] useful __.` 或 `[NN|PRP] is [jj]`