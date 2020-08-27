'''
opencv_机器学习-图片合成视频
实现步骤:
1.加载视频
2.读取视频的Info信息
3.通过parse方法完成数据的解析拿到单帧视频
4.imshow，imwrite展示和保存
'''
import cv2
#读取一张图片

def img_to_video():
    img = cv2.imread('imag/tb_200827-150021.jpg')
    #获取当前图片的信息
    imgInfo = img.shape
    size = (imgInfo[1],imgInfo[0])
    print(size)
    #完成写入对象的创建，第一个参数是合成之后的视频的名称，第二个参数是可以使用的编码器，第三个参数是帧率即每秒钟展示多少张图片，第四个参数是图片大小信息
    videowrite = cv2.VideoWriter('test.mp4',-1,1,size)
    for i in range(1,10):
        fileName = 'imag/tb_200827-15002' + str(i) + '.jpg'
        img = cv2.imread(fileName)
        #写入参数，参数是图片编码之前的数据
        videowrite.write(img)
    print('end!')















def resize_image(target_image_path, target_size):
    """
    调整图片大小，缺失的部分用黑色填充
    :param target_image_path: 图片路径
    :param target_size: 分辨率大小
    :return:
    """
    image = Image.open(target_image_path)

    iw, ih = image.size  # 原始图像的尺寸
    w, h = target_size  # 目标图像的尺寸
    scale = min(w / iw, h / ih)  # 转换的最小比例

    # 保证长或宽，至少一个符合目标图像的尺寸
    nw = int(iw * scale)
    nh = int(ih * scale)

    image = image.resize((nw, nh), Image.BICUBIC)  # 缩小图像
    # image.show()

    new_image = Image.new('RGB', target_size, (0, 0, 0, 0))  # 生成黑色图像

    # 将图像填充为中间图像，两侧为灰色的样式    
    new_image.paste(image, ((w - nw) // 2, (h - nh) // 2))  

    # 覆盖原图片
    new_image.save(target_image_path)