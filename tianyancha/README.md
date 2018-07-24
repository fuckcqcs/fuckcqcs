# 各个省份采购长春长生疫苗流向

### 特性

1. 新增`天眼查`对于各个省份对长春长生疫苗采购信息，[https://www.tianyancha.com/pagination/bid.xhtml?ps=30&pn=%s&id=2322751222](https://www.tianyancha.com/pagination/bid.xhtml?ps=30&pn=%s&id=2322751222)

2. 由于`天眼查`的数据是从`中国政府采购网`抓取，使用爬虫获取原始政府连接。

3. 对元数据进行结构化处理,针对 Echarts 结构处理。实现可视化。

### 文件说明

`static`： Echarts 所需js。

`bid1,bid2,bid3,bid4,bid5`： 天眼查原始页面，因为天眼查爬取对爬取速度，ip，Cookie 有限制，故缓存html页面结构化提取。

`f_cccs_scrapy.py`：原始爬取代码，时间紧写得比较丑陋。

`f_cccs_structure_gen.py`：生成 echarts 适配数据。

`Pipfile`：pipenv 文件，请忽略。

`structure_data.json`：结构化json文件。

`tianyancha_visual_data.htm`：最后可打开可视化页面，数据已经填充进去。

### 运行

1. 直接在浏览器打开 `tianyancha_visual_data.htm`。

### 参考

1. 中国政府采购网：[www.ccgp.gov.cn](www.ccgp.gov.cn)

2. 天眼查：[https://www.tianyancha.com](https://www.tianyancha.com)