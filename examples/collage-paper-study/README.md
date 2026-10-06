# 留下这一句：五秒印刷剪贴样段

1920×1080、30fps、5秒。人物与书本来自一张本轮生成的透明 atlas；独立CSS视窗取出主体，不重画每一帧。纸条沿弧线移动并以四个离散姿态展开，最后保持标题。10fps量化视觉姿态，音轨不量化。

从仓库根目录运行 `npm ci`、`npm run setup`、`npm run preview`、`npm run check:demo`、`npm run render:demo`、`npm run mix:demo`。原成片是 `renders/collage-paper-study.mp4`，复现成片写入 `renders/reproduced.mp4`，避免覆盖原始审片版本。

用本机静态服务器从该目录打开 `review.html` 可看原带声成片。Studio预览是画面源工程，声音在最终FFmpeg混入。无需原工作区、私人音频、API密钥或付费图片生成；素材已准备好。字体重新生成与声音重新剪裁属于原制作过程，公开样例复现使用已冻结素材，避免依赖本机缓存路径。

技术检查通过；结构存在两个已记录lint提示。审片记录校验只证明记录与原成片哈希相符，不证明审美质量，主观声音与连续运动审美未声称验证。
