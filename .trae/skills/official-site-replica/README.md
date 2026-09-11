# Site Runtime Mirror

`Site Runtime Mirror` 是一个用于复刻复杂官网的 TRAE Skill。它不会先照着截图重新画页面，而是优先搬运并复跑原站前端运行时。

它适合那些真正难点在行为而不是布局的页面：加载动画、GSAP 时间线、WebGL Canvas、Rive、Lottie、3D 模型、自定义字体、懒加载 chunk、依赖路由的状态，以及滚动驱动动画。

## 保留什么

- 真实 HTML、CSS、JavaScript、动态 chunk、preload、内联配置和运行时请求。
- 图片、字体、视频、动画文件、模型、纹理、解码器、worker、WASM 等运行资源。
- 会影响视觉结果的路由假设、浏览器状态、滚动位置、首次访问状态和登录态变体。
- 技术上可恢复的原始动效链路，而不是手写 CSS 或截图式仿制。

## 适用场景

用户提出以下需求时使用：

- `1:1` 复刻网站或官网首页；
- 保留源站加载、滚动、WebGL、Rive、Lottie 或 3D 行为；
- 排查本地复刻版为什么和官网不一致；
- 匹配用户自己 Chrome 里看到的准确页面版本；
- 打包一个可本地服务和验证的 H5 版本。

不适合普通落地页、重新设计稿、视觉参考板，或用户明确接受“按风格新做一版”的页面。

## 包内容

```text
official-site-replica/
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

目录保留历史 slug `official-site-replica`，用于兼容已有安装路径；对外名称使用 `Site Runtime Mirror`。

## 工作流程

1. 检查官方 HTML 和运行时入口。
2. 捕获真实浏览器网络图，包括动态 chunk 和动画资源。
3. 判断目标效果由什么渲染：DOM、Canvas、WebGL、Rive、Lottie、视频，或混合栈。
4. 本地镜像必要资源，同时保留路由和路径假设。
5. 通过 HTTP 运行本地版本，并测试与源站一致的有效路径。
6. 对比多个时间点的官方状态和本地状态。
7. 在报告完成前，修掉缺失资源、console 错误、卡住的加载层和状态不一致。

## 登录态变体

有些站点会根据登录态、Cookie、localStorage、地区、视口、浏览器 Profile 或实验桶返回不同页面。当目标是用户 Chrome 里看到的页面时，应以该浏览器会话为准，只捕获复现视觉和运行状态所需的信息。

不要在 Skill 或生成包里保存凭据、Cookie、私有 token 或无关个人数据。

## 验收标准

至少检查：

- 没有无法解释的本地 `404`、`403` 或 `5xx` 响应；
- 没有未处理的运行时异常；
- 预期的 canvas、video、image、model、font 和 animation 资源都已存在；
- 关键 DOM 状态、路由、视口、滚动位置和可见文本与目标状态一致；
- 动效密集页面已对比多个时间线帧。

## 使用边界

镜像的官网资源可能受版权或许可证限制。除非用户拥有重新分发源站脚本、字体、图片、视频、模型和动画文件的权限，否则复刻产物应保持私有。
