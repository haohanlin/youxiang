import time
import json
import itchat
import random
from untils.common import save_pic, del_pic
from untils.tb_top_api import TbApiClient

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
                # 发送图片
                #itchat.send('@img@%s' % (f'''{filename}'''), group_name)
                print('START_###################################')
                print(title)
                print('【在售价】¥')
                print(zk_final_price)
                print('【券后价】¥' )
                print(round(float(zk_final_price) - float(coupon_amount)))
                print('淘宝下单链接')
                print(tb_client.taobao_tbk_tpwd_create(title, coupon_share_url))
                print('END_################START###################')
                #itchat.send(f''' {title} \n【在售价】¥{zk_final_price}\n【券后价】¥{round(float(zk_final_price) - float(coupon_amount),
                #                                                            2)}\n-----------------\n復製評论({tb_client.taobao_tbk_tpwd_create(
                #    title, coupon_share_url)})，去【tao寶】下单\n''', group_name)

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
                print('END_################START###################')
                #itchat.send(
                #    f'''{title} \n【在售价】¥{zk_final_price}\n-----------------\n復製評论({tb_client.taobao_tbk_tpwd_create(
                #        title, click_url)})，去【tao寶】下单\n''', group_name)
                time.sleep(2)
                del_pic(filename)
    except Exception as e:
        print(e)
        tb_share_text(group_name, material_id, app_key, app_secret, adzone_id)


if __name__ == '__main__':
    print(f'''tb function''')