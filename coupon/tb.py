import time
import json
import itchat
import random
import qrcode
from untils.common import save_pic, del_pic
from untils.tb_top_api import TbApiClient
from PIL import Image, ImageDraw, ImageFont


def tb_share_text(group_name: str, material_id: str, app_key, app_secret, adzone_id):
    '''

    :param group_name:
    :param material_id:
    :return:
    '''
    print("开始获取-----")
    try:
        material_id = str(random.choices(material_id.split(','))[0])
        
        print(material_id+ "whx1")
        print(group_name + "whx2")
        #groups = itchat.search_chatrooms(name=f'''{group_name}''')
        #for room in groups:
       #group_name = room['UserName']
        time.sleep(random.randint(1, 5))
        tb_client = TbApiClient(app_key=app_key, secret_key=app_secret, adzone_id=adzone_id)
        res = tb_client.taobao_tbk_dg_optimus_material(material_id)
        print("输出tb_client数据res:----------------------- whx3")
        print(repr)
        json_data = json.loads(res)['tbk_dg_optimus_material_response']['result_list']['map_data']
        count = 0
        print("输出json数据:----------------------- whx4")
        #print(json_data)
        for item in json_data:
            count += 1
            if str(item).find("coupon_share_url") > -1:
                coupon_share_url = "https:" + item['coupon_share_url']
                coupon_amount = item['coupon_amount']
                pict_url = "https:" + str(item['pict_url'])
                title = item['title']
                item_id = item['item_id']
                filename = save_pic(pict_url, item_id)
                zk_final_price = item['zk_final_price']
                coupon_share_url_1 = item['coupon_share_url']
                # 发送图片
                #itchat.send('@img@%s' % (f'''{filename}'''), group_name)
                print('START_###################################')

                #itchat.send(f''' {title} \n【在售价】¥{zk_final_price}\n【券后价】¥{round(float(zk_final_price) - float(coupon_amount),
                #                                                            2)}\n-----------------\n復製評论({tb_client.taobao_tbk_tpwd_create(
                #    title, coupon_share_url)})，去【tao寶】下单\n''', group_name)
                qr = qrcode.QRCode(
                    error_correction=qrcode.constants.ERROR_CORRECT_L,
                    box_size=3,
                )
                qr.add_data(coupon_share_url_1)
                qr.make(fit=True)
                qr_img = qr.make_image()
                #qr_img.show()
                qr_img_copy = qr_img.copy()
                

                text_title = list(title)#title.lnsert(15,'\n')
                text_title.insert(15,'\n')
                title = "".join(text_title)
                text_he = "【在售价】￥" + str(zk_final_price) + '\n'
                text_he = text_he + "【券后价】￥" + str(round(float(zk_final_price) - float(coupon_amount))) + '\n'
                text_he = text_he + tb_client.taobao_tbk_tpwd_create(title, coupon_share_url)
                img = Image.open(filename) #打开图片
                img_copy = img.copy()   #拷贝图片
                imghead =  Image.new("RGB", (img.size[0],img.size[1]+270), "#FFFFFF")  #创建一个纯白图片
                imghead.paste(img_copy,(0,0))   #把拷贝的图片粘贴到纯白的图片
                imghead.paste(qr_img_copy,(530,img.size[1]))
                draw = ImageDraw.Draw(imghead)  #把图片放进区域
                typeface = ImageFont.truetype('simkai.ttf',size=33)  #设置字体
                draw.text((10,img.size[1]+10),title,fill=(0, 0, 1),font=typeface) #写入字

                typeface2 = ImageFont.truetype('simkai.ttf',size=50)  #设置字体
                draw.text((10,img.size[1]+100),text_he,fill=(250, 0, 1),font=typeface2) #写入字
                print(title) 
                print(text_he) 
                filenamehead = 'imag' + filename[6:]  
                #imghead.show()
                imghead.save(filenamehead)  #保存
                print('END_###################################')
                time.sleep(2)
                del_pic(filename)
            else:
                click_url = "https:" + item['click_url']
                title = item['title']
                item_id = item['item_id']
                pict_url = "https:" + str(item['pict_url'])
                zk_final_price = item['zk_final_price']
                filename = save_pic(pict_url, item_id)
                #itchat.send('@img@%s' % (f'''{filename}'''), group_name)
                print('START_###################################')
                print(title)
                print('【在售价】¥')
                print(zk_final_price)
                print('淘宝下单链接')
                print(tb_client.taobao_tbk_tpwd_create(title, click_url))
                print('END_###################################')
                #itchat.send(
                #    f'''{title} \n【在售价】¥{zk_final_price}\n-----------------\n復製評论({tb_client.taobao_tbk_tpwd_create(
                #        title, click_url)})，去【tao寶】下单\n''', group_name)
                time.sleep(2)
                #del_pic(filename)
    except Exception as e:
        print(e)
        tb_share_text(group_name, material_id, app_key, app_secret, adzone_id)


if __name__ == '__main__':
    print(f'''tb function''')