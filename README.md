# Site Runtime Mirror

`Site Runtime Mirror` 是一个用于复刻复杂官网的 TRAE Skill。它的重点不是“照着截图重新画一个相似页面”，而是尽量把原站前端运行时搬到本地，让原始脚本、动效、资源和状态在本地重新跑起来。

它适合处理那些靠普通静态还原很容易翻车的网站：加载动画、GSAP 时间线、WebGL Canvas、Rive、Lottie、3D 模型、自定义字体、懒加载 chunk、依赖路由的页面状态，以及滚动驱动动画。目标是让原站代码路径在本地达到同样的状态，并用浏览器证据验证，而不是凭肉眼感觉说“差不多”。

## 为什么需要它

很多“官网复刻”失败的原因都一样：只复制了某一帧的外观，却丢掉了真正让页面成立的运行时行为。这个 Skill 会把工作锚定在原站 runtime 上，包括真实 HTML、脚本、样式、资源、路由假设和浏览器状态。

当你需要保留源网站的动效系统、加载过程、交互逻辑和最终渲染状态时，就应该使用它。视觉相似只是结果，运行链路一致才是关键。

## 它会处理什么

- 捕获页面真实运行图：HTML、CSS、JavaScript、动态 chunk、preload、内联配置和运行时请求。
- 本地化视觉资源：图片、字体、视频、动画文件、模型、纹理、解码器、worker、WASM，以及路由触发的资源。
- 通过 HTTP 复跑源站行为，而不是依赖容易破坏现代前端运行时的 `file://`。
- 区分真正影响视觉的资源和埋点、客服插件、统计脚本等非关键噪音。
- 用浏览器证据对比官方页面和本地页面，包括 console/network 状态、canvas/video/image 数量、滚动状态和时间线截图。
- 在登录态、Cookie、CMS 内容、地区或 A/B 实验影响页面时，捕获用户浏览器里看到的准确版本。

## 适用场景

适合这类需求：

- “1:1 复刻这个官网”
- “动效要和原站一样，不要自己重做”
- “把这个 WebGL / Rive / Lottie 页面本地化”
- “这个复刻版和官网不一致，继续修到一致”
- “用我 Chrome 里看到的登录态页面做准”
- “把官网源码打包成可运行 H5 项目”

不适合普通落地页、视觉参考稿、重新设计页面，或者用户明确接受“按风格新做一版”的场景。

## 目录结构

```text
.trae/skills/official-site-replica/
  SKILL.md
  README.md
  references/
    runtime-acquisition.md
    verification-checklist.md
    pitfalls.md
  scripts/
    timeline_compare.py
    asset_manifest_template.json
  evals/
    evals.json
```

安装目录暂时保留历史 slug `official-site-replica`，用于兼容已有包和引用；对外名称使用 `Site Runtime Mirror`。

## 典型流程

1. 检查官方 HTML，找到运行时入口。
2. 在浏览器里捕获真实网络图，确认动态 chunk、动画文件、媒体资源和运行状态。
3. 判断目标效果到底由什么渲染：DOM、Canvas、WebGL、Rive、Lottie、视频，或多层混合。
4. 本地镜像必要资源，同时保留原站路径和路由假设。
5. 通过 HTTP 服务运行本地版本；如果源站从 `/` 初始化，本地也优先用 `/` 和 `index.html`。
6. 对比多个时间点的官方状态和本地状态，不只看一张截图。
7. 在报告完成前，修掉无法解释的缺失资源、console 错误、卡住的加载层和状态不一致。

## 登录态与变体

有些站点会根据登录态、Cookie、localStorage、地区、视口、浏览器 Profile 或实验桶返回不同页面。此时匿名 headless 抓取不一定等于用户正在评判的页面。

当目标是“用户 Chrome 里看到的页面”时，应以该浏览器会话为准。只捕获复现视觉和运行状态所需的信息，例如渲染后 DOM、已加载资源、视口、可见文本和安全的运行时配置；不要保存凭据、Cookie、私有 token 或无关个人数据。

## 验收标准

页面能打开不代表复刻完成。至少要检查：

- 没有无法解释的本地 `404`、`403` 或 `5xx` 响应；
- 没有未处理的运行时异常；
- 预期的 canvas、video、image、model、font 和 animation 资源都已加载；
- 关键 DOM 状态、路由、视口、滚动位置和可见文本与目标状态一致；
- 动效密集页面需要对比多个时间线帧；
- 登录态或个性化快照在不重新调用私有线上 API 的情况下仍能稳定展示。

## 交付物

- `dist/official-site-replica.skill`：可安装 Skill 包，文件名暂时保留旧 slug 以兼容已有引用。
- `dist/official-site-replica-skill-source.zip`：源码包，包含 evals。
- `manifest/official-site-replica-package-manifest.json`：包清单和校验信息。

## 使用边界

镜像的官网资源可能受版权或许可证限制。除非用户拥有重新分发源站脚本、字体、图片、视频、模型和动画文件的权限，否则复刻产物应保持私有。

这个仓库存放的是可复用的工作流说明、验证脚本和检查清单，不包含第三方站点资产。
