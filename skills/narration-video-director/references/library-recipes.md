# 按镜头能力复用库

用于选择具体绘图库、动画资产或合成效果时；沿用作品已成立的视觉方向，不作为必须安装的套餐。以下来自2026-10-02的实际样段与官方资料，版本/API在新项目中仍需核验。

## 从表达任务选择

| 镜头需要 | 优先复用 | 设计与接入边界 |
|---|---|---|
| 发光观测素材、统一照片或纸张质感 | Remotion effects | 只处理有材质理由的主体；先试直接Canvas素材，整组DOM另查HtmlInCanvas支持 |
| 有力度的墨迹、圈选与收笔 | perfect-freehand | 输入压力与中心线点，输出笔画外轮廓；描外轮廓的dash不同于笔尖书写 |
| 从模糊感觉变为可处理对象 | flubber | 先设计起止对象与中间姿态；含洞/多个子路径不能视为通用形变；几何对应关系预先构造 |
| 图表与原因、行动、反馈关系 | D3 + 必要时ELK | 几何/布局先算好，口播逐步显露；自动布局不决定哪些信息应出现 |
| 复用角色或专业插画动作 | Remotion Lottie/Rive | 先检查资产风格和动作含义；Lottie expressions、Rive状态机分别验证帧定位，不能整体承诺任意动画可seek |
| 空间对象局部发光与部件强调 | 已有Drei + 按需postprocessing | 所有位置/uniform由视频时间声明；空间Bloom与Glitch、累计阴影、物理状态需分别适配 |
| 真实短动作声音 | 已有音效素材/SFX + FFmpeg | 根据对象材质挑声音并保存具体来源；重点到达才考虑音效，不给所有动作加whoosh |

## 已暴露的实际接入问题

### 首次导出与预览不是同一条就绪路径

在Remotion4.0.530、R3F9.8.1、Drei10.7.9、react-postprocessing3.1.3、postprocessing6.39.5的月相样段中，第一次直达目标帧时Composer尚未装好全部pass，静帧丢失上方月亮；预览拖动后能正常显示。实际修复是在贴图组件就绪后等待pass安装，用`delayRender`阻止提前截图，并调用一次`composer.render(0)`。

这是该空间Bloom样段的局部适配，不能推广为所有后期的通用方案。ThreeCanvas触发绘制不会自动把第三方clock/delta对齐视频时间；带时间/历史/随机的效果另行控制。不要用“播放一次后再截图”掩盖首次定位问题。

### 统一参与解释的几何来源

观察者的SVG标记、3D发光点、轨迹和相机角度应从同一条路径求值。本次误用上方固定相机的angle导致发光点停在初始位置；改用轨迹终点后恢复对应。新的路径和坐标关系同样要检查端点，而非只看动画能运行。

### 动画资产的背景也是设计的一部分

官方Gatin Lottie样例的橙色方形背景与场景留白不协调，采用composition中的圆形裁切统一边界，保留主体原动画。复用资产时先检查背景、画幅、姿态占地与镜头语义；不要把一个已设计资产硬塞进不相容的画面。

### FFmpeg截取与留白分开计算

在输出侧设置`-t`，再通过滤镜加入delay/pad，会把最终输出裁到该长度，从而截短原本需要保留的句尾。需要“完整语音片段+前后留白”时，明确输入截取范围与最终输出时长；用实际文件时长和句尾锚点检查。音轨存在、峰值正常不证明句子完整。

### 文字标注与尺寸测量

对文本圈选、划除与下划线，优先评估官方`@remotion/rough-notation`，保持低而稳定的粗糙度、固定seed和帧驱动progress。标注只指向当前需要观察的部分，不同时高亮整张文档。文字尺寸可用`@remotion/layout-utils`，必须等实际字体加载后测量；不要先用回退字体得到尺寸，再让中文字体挤出框。

FocusDirectionDemo以同一个工作稿承载开头改写，镜头先观察反馈，再移到改写，最后退回二者的关系。两条措辞是被修改的对象，“反馈”是必要身份标签，其余叙述交给配音。自制工作稿与曲线标为示意；不能把这种设计称为真实后台截图。

### 运动模糊的能力与阅读边界

按当前官方规范优先评估HtmlInCanvasMotionBlur，并检查预览的HTML-in-canvas能力。可使用CameraMotionBlur作为兼容实现，但它的叠层混合可能改变颜色与透明度，不能承诺两种实现逐像素一致，也不能用拖影代替曝光模糊。不要因为渲染正常就假定当前预览支持相同路径。

模糊只服务快速运动；阅读保持时关闭，子场景仍从自己的视频帧求值。检查实际编码的移镜中帧：出现分离的多重轮廓时，减少曝光长度或增加采样，同时控制渲染开销。相机需要明确观察目标、加减速与停留，模糊不能修复无目的的镜头移动。

参考：[官方文字标注](https://www.remotion.dev/docs/text-highlights)、[文字测量](https://www.remotion.dev/docs/layout-utils/measure-text)、[运动模糊](https://www.remotion.dev/docs/motion-blur)。上述场景判断来自本地FocusDirectionDemo，尚未宣称用户认可其审美。

## 验证并保存可复用经验

静帧检查首次直达、主体加载与遮挡；定位检查反向返回；导出检查细线、透明、编码和落定。若宣称Studio可编辑，选一个实际元素修改并保存，再确认源码。程序化形变与3D内部参数可以保持代码控制，清楚区分编辑边界。

月相、墨迹变形、Lottie角色是三种不同实验；不能以一个成功截图证明整个工具组合已通用。技术验证与带声审片分别记录；没有实际听取音频就不宣称听感已通过。

来源：[effects](https://www.remotion.dev/docs/effects)、[perfect-freehand](https://github.com/steveruizok/perfect-freehand)、[flubber](https://github.com/veltman/flubber)、[ELK](https://github.com/kieler/elkjs)、[ThreeCanvas](https://www.remotion.dev/docs/three-canvas)、[Lottie](https://www.remotion.dev/docs/lottie)、[Rive](https://www.remotion.dev/docs/rive)、[FFmpeg filters](https://www.ffmpeg.org/ffmpeg-filters.html)。实际例子和适配判断来自本地LibraryCraftReel，未宣称复现参考片风格或优于其他工具。
