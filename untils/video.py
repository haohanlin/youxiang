'''
opencv_机器学习-图片合成视频
实现步骤:
1.加载视频
2.读取视频的Info信息
3.通过parse方法完成数据的解析拿到单帧视频
4.imshow，imwrite展示和保存
'''
from untils.common import save_pic, del_pic
import cv2,glob,os
from PIL import Image
#读取一张图片


def get_file(root_path,all_files=[],sub_dirpaths = []):
    filenames = os.listdir(root_path)
    #print(filename)
    for filename in filenames:
        filepath = os.path.join(root_path,filename)
        if not os.path.isdir(filepath):# not a dir
            all_files.append(filepath)
        else:  # is a dir
            sub_dirpaths.append(filepath)
            get_file(filepath,all_files)
    return all_files,sub_dirpaths





def img_to_video(num = 7):
    
    path = r'F:\vs_code\youxiang\imag'
    filepaths,dirpathlist = get_file(path)
    #print(filepath)
    print(dirpathlist)
    for dirpath in dirpathlist[:]:
        print(dirpath)
        fps = 1
        fourcc = cv2.VideoWriter_fourcc(*'MJPG')
        filenames = os.listdir(dirpath)
        filepath = os.path.join(dirpath, filenames[0])
        if os.path.isfile(filepath):
            img = Image.open(filepath)
            size = img.size  # 大小/尺寸,获取第一张图片的尺寸
            print(size)
            videpath = path + '\\' + '_'.join(dirpath.split('\\')[-2:]) + '.avi'
            videoWriter = cv2.VideoWriter(videpath, fourcc, fps, size)#视频按照图片尺寸合成
            imgpaths = dirpath + '/*.jpg'
            imgs = glob.glob(imgpaths)
            for imgname in imgs:
                for i in range(3):  # 一张图循环7次，fps = 1，一张图停留7s
                    frame = cv2.imread(imgname)
                    videoWriter.write(frame)
            videoWriter.release()
            #del_pic(imgname)
    print('whx---------------')
    cv2.destroyAllWindows()
    for fileimg in filepaths:
        if('avi' not in fileimg):
            print(fileimg)
            del_pic(fileimg)















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