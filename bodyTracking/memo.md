# 📝 2022/10/16


## 事前調査

[Capturing Body Motion in 3D | Apple Developer Documentation](https://developer.apple.com/documentation/arkit/content_anchors/capturing_body_motion_in_3d?language=objc)


[はじめに｜RealityKit入門](https://zenn.dev/noby111/books/3f370e126df73b/viewer/d6cc56)


[Xamarin.iOS での ARKit の概要 - Xamarin | Microsoft Learn](https://learn.microsoft.com/ja-jp/xamarin/ios/platform/introduction-to-ios11/arkit/)

## RealityKit

多分`ARView` 呼び出せない？SceneKit でいいからええけど

ん、framework は存在するか？


```
--- Frameworks :hit 2
/System/Library/Frameworks/RealityFoundation.framework
/System/Library/Frameworks/RealityKit.framework
--- PrivateFrameworks :hit 3
/System/Library/PrivateFrameworks/CoreRealityIO.framework
/System/Library/PrivateFrameworks/RealityFusion.framework
/System/Library/PrivateFrameworks/RealityIO.framework

```

## `debugOptions`


```
>>> int("fffffffffc000000", 16)
18446744073642442752
>>> (1 << 1) | (1 << 31)
2147483650

```
