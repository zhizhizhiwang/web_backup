下面是 **Browsertrix Crawler 参数说明中文翻译**（保持技术含义准确，尽量贴近原始术语）。

---

# Browsertrix Crawler 参数说明（中文）

## 基础参数

* `--help`
  显示帮助信息

* `--version`
  显示版本号

* `--seeds, --url`
  爬取起始 URL
  类型：数组
  默认：`[]`

* `--seedFile, --urlFile`
  从文件读取起始 URL（每行一个）

---

## 并发与任务控制

* `-w, --workers`
  并行 worker 数量
  默认：1

* `--crawlId, --id`
  爬虫任务 ID（可通过环境变量 `CRAWL_ID` 设置）
  默认：Docker 容器主机名 + collection 名

---

## 页面加载控制

* `--waitUntil`
  Puppeteer `page.goto()` 等待条件，可多个
  选项：

  * `load`
  * `domcontentloaded`
  * `networkidle0`
  * `networkidle2`
    默认：`["load","networkidle2"]`

* `--depth`
  爬取深度
  默认：-1（无限）

* `--extraHops`
  超出当前作用域允许额外跳转层数
  默认：0

* `--pageLimit, --limit`
  最大爬取页面数量
  默认：0（无限）

* `--maxPageLimit`
  覆盖 pageLimit 的最大页面数

* `--pageLoadTimeout, --timeout`
  单页面加载超时时间（秒）
  默认：90

---

## 爬取范围控制

* `--scopeType`
  爬取范围类型：

  * `page`（仅当前页）
  * `page-spa`
  * `prefix`
  * `host`
  * `domain`
  * `any`
  * `custom`

* `--scopeIncludeRx, --include`
  包含 URL 的正则表达式

* `--scopeExcludeRx, --exclude`
  排除 URL 的正则表达式

* `--allowHashUrls`
  允许带 `#` 的 URL（适合 SPA）

---

## 链接提取

* `--selectLinks, --linkSelector`
  自定义链接提取规则
  格式：

  ```
  CSS选择器->属性
  ```

* `--clickSelector`
  自动点击元素选择器
  默认：`a`

---

## 内容阻止规则

* `--blockRules`
  阻止加载 URL 的规则

* `--blockMessage`
  URL 被阻止时写入的错误信息

* `--blockAds`
  屏蔽广告

* `--adBlockMessage`
  广告被阻止时写入的信息

---

## 数据输出

* `-c, --collection`
  爬取输出目录名
  默认：`crawl-@ts`

* `--generateCDX`
  生成 CDXJ 索引

* `--combineWARC`
  合并 WARC 文件

* `--rolloverSize`
  WARC 文件大小轮转阈值
  默认：1GB

* `--generateWACZ`
  生成 WACZ 包

* `--useSHA1`
  使用 SHA1（默认 SHA256）

---

## 日志系统

* `--logging`
  日志类型：

  * stats
  * js errors
  * debug

* `--logLevel`
  日志级别

* `--context`
  日志上下文过滤

* `--logExcludeContext`
  排除日志上下文

---

## 文本提取

* `--text`
  文本提取方式：

  * `to-pages`
  * `to-warc`
  * `final-to-warc`

---

## 运行环境

* `--cwd`
  工作目录
  默认：`/crawls`

* `--headless`
  是否无头模式运行

* `--mobileDevice`
  模拟移动设备

* `--userAgent`
  自定义 UA

* `--userAgentSuffix`
  UA 附加字符串

---

## Sitemap 支持

* `--useSitemap`
  自动检测 sitemap

* `--sitemapFromDate`
  过滤最早日期

* `--sitemapToDate`
  过滤最晚日期

---

## 页面行为模拟

* `--behaviors`
  页面自动行为：

  * autoplay
  * autofetch
  * autoscroll
  * siteSpecific

* `--behaviorTimeout`
  行为执行超时

* `--postLoadDelay`
  页面加载后延迟

* `--pageExtraDelay`
  页面完成后延迟

---

## 浏览器配置

* `--profile`
  加载浏览器配置

* `--saveProfile`
  保存浏览器配置

---

## 截图与录屏

* `--screenshot`
  截图类型：

  * view
  * thumbnail
  * fullPage
  * fullPageFinal

* `--screencastPort`
  开启录屏服务端口

---

## Redis 状态存储

* `--redisStoreUrl`
  Redis 地址
  默认：`redis://localhost:6379/0`

* `--saveState`
  保存爬虫状态：

  * never
  * partial
  * always

---

## 资源限制

* `--sizeLimit`
  爬取大小限制

* `--diskUtilization`
  磁盘占用限制

* `--timeLimit`
  爬取时间限制

---

## 任务控制

* `--overwrite`
  覆盖已有数据

* `--waitOnDone`
  完成后等待信号退出

* `--restartsOnError`
  允许错误后重启

---

## 网络空闲检测

* `--netIdleWait`
  网络空闲等待时间
  默认：2秒

* `--netIdleMaxRequests`
  判定空闲最大请求数

---

## 元数据

* `--title`
  WACZ 标题

* `--description`
  WACZ 描述

---

## 代理支持

* `--proxyServer`
  设置代理服务器

* `--proxyServerConfig`
  多代理配置文件

---

## 失败控制

* `--maxPageRetries`
  页面重试次数

* `--failOnFailedSeed`
  种子失败时终止

* `--failOnInvalidStatus`
  4xx/5xx 视为失败

---

## 自定义行为脚本

* `--customBehaviors`
  注入自定义行为脚本

---

## 存储扩展

* `--saveStorage`
  保存 localStorage / sessionStorage

---

## 调试模式

* `--debugAccessRedis`
  允许外部访问 Redis

* `--debugAccessBrowser`
  启用 Chrome DevTools 端口 9222

---

## Service Worker

* `--serviceWorker`
  选项：

  * disabled
  * disabled-if-profile
  * enabled

---

## 其它

* `--dryRun`
  不写入归档数据

* `--qaSource`
  QA 模式输入源

* `--extraChromeArgs`
  额外 Chrome 参数

* `--useRobots`
  遵循 robots.txt

* `--robotsAgent`
  robots 检测 UA

* `--config`
  YAML 配置文件路径

---

