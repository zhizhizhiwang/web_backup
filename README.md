# web backup

## 部署
- 保证有可用的docker环境 依赖镜像 `webrecorder/browsertrix-crawler` 与 `ghcr.io/openzim/warc2zim`
- 使用`uv sync` 部署`python`环境

## 使用流程

1. 编写模板yaml (可选) :  
至少应该包含 `seeds -> url`, 其中scopeType参数会自动作用于所有后续生成的`seeds`  
```yaml
seeds:
- url: ''
  scopeType: page-spa
workers: 4
combineWARC: true
logging: stats
```
2. 使用`uv run .\discover\cli.py` 获取最近新增  
例 `uv run .\discover\cli.py wikidot --browsertrix /path/to/config.yaml --since 1770336000 `  
```
--since         指定开始时间戳(UTC)
--page          最大爬取页数, 过低可能导致无法爬取到--since设定的时间戳就提前结束
--browsertrix   指定yaml配置文件则会自动填充seeds列表, 文件不存在则会自动新建
--out           指定json报告输出文件名
```

3. 使用 `uv run .\crawl.py` 开始爬取  
例`uv run .\crawl.py --config \path\to\config`  
```
--config        指向browsertrix配置文件 (必填)
--seeds         指向browsertrix的seeds.txt 
```

4. 使用`uv run .\convert_docker.py` 使用WARC生成zim  
```
<input>         WARC文件夹或文件(自动递归识别)
<output>        输出文件夹
[args]          其他自定义参数
```


### 其他
- 使用`uv run .\tasks\clean_crawls.py` 清理爬取残留文件   
!!! 会删除`\crawl`下所有文件, 无法恢复
## todo list
- 自动环境部署