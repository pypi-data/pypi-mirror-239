import requests
import json
from jsonpath import jsonpath
import time
import random
import hmac
from hashlib import sha1

def create_general_post(data):
    """创建普通贴文销售，返回响应和贴文销售ID
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    title 不是必填
    """
    env = data["env"]
    platform = data["platform"]
    patternModel = data["patternModel"]
    headers = data["headers"]
    title = "接口自动化创建的普通贴文%d"%int(time.time())
    if "title" in data:
        title = data["title"]
    url = "%s/api/posts/post/sales/create"%env
    body = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel
         }
    response = requests.post(url,headers=headers,json=body).json()
    # print(response)
    sales_id = response["data"]["id"]
    return response,sales_id

def create_commerce_post(data):
    """创建留言串销售贴文，返回响应和贴文销售ID
    platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    patternModel:
    INCLUDE_MATCH：模式1-留言包含 关键字 或 关键字+数量
    WITH_QTY_MATCH：模式2-留言包含 关键字+数量
    EXACT_MATCH：模式3-留言只有 关键字 或 关键字+数量
    WITH_SPU_MATCH:模式4-留言包含 商品编号+规
    title 不是必填
    """
    env = data["env"]
    headers = data["headers"]
    platform = data["platform"]
    patternModel = data["patternModel"]
    title = "接口自动化创建的留言串销售贴文%d" % int(time.time())
    if "title" in data:
        title = data["title"]
    url = "%s/api/posts/post/sales/create"%env
    body = {
      "platform": platform,
      "type": 1,
      "platforms": [
          platform
      ],
      "title": title,
      "patternModel": patternModel,
      "postSubType": "COMMERCE_STACK"
         }
    response = requests.post(url,headers=headers,json=body).json()
    # print(response)
    sales_id = response["data"]["id"]
    return response,sales_id

def get_channel_info(data):
    """
    获取串接的渠道信息
    :param data:   platform："FACEBOOK"、"INSTAGRAM"、"FB_GROUP"
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    platform = data["platform"]
    url = "%s/api/posts/post/sales/channels?platform=%s"%(env,platform)
    res = requests.get(url, headers=headers).json()
    page_id = res["data"][0]["platformChannelId"]
    page_name = res["data"][0]["platformChannelName"]
    group_id = res["data"][0]["groupId"]
    return page_id,page_name,group_id


def create_fb_text_post(data):
    """
    创建fb、fb group纯文本贴文
    :param data: fb group 创建贴文时，pageId为group_id
    :return:post_pid 为贴文在post数据库的ID，取消和编辑贴文时会使用到
    """
    page_id, page_name, group_id = get_channel_info(data)
    env = data["env"]
    headers = data["headers"]
    platform = data["platform"]
    sales_id = data["sales_id"]
    postDescription = "一天天工作这么忙，烦死了%d"%int(time.time())
    if postDescription in data:
        postDescription = data["postDescription"]
    if platform == "FB_GROUP":
        page_id = group_id
    url = "%s/api/posts/post/%s/post"%(env,sales_id)
    body = {"postDescription":postDescription,"platform":platform,
            "url":[],"mediaFbid":[],"pageId":page_id}
    response = requests.post(url,headers=headers,json=body).json()
    post_id = response["data"]["post_id"]
    post_pid = response["data"]["id"]
    return post_id,post_pid,response

def search_post_product(data):
    """
    查询可添加的商品，只查询前10个，和查询openApi/proxy/v1/products不一样，这个接口经过post组装关键字返回
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/api/posts/common/product/key/spu/list?page=1&searchType=ALL&pageSize=10"%env
    response = requests.get(url, headers=headers).json()
    productSpuKeyVos = response["data"]["productSpuKeyVos"][0]
    skuKeys = productSpuKeyVos["skuKeys"]
    spuId = productSpuKeyVos["spuId"]
    return skuKeys,spuId,response

def search_oa_product(data):
    """
    查询OA的商品，并返回响应
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/products?page=1&per_page=4"%env
    response = requests.get(url, headers=headers).json()
    return response




def model_one_add_product(data):
    """
    贴文销售模式1-模式3添加商品，只添加第一个商品到贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/products"%(env,sales_id)
    skuKeys, spuId, response = search_post_product(data)
    skuList = []
    body = {}
    if skuKeys != None:
        for index, sku in enumerate(skuKeys):
            skuId = sku["skuId"]
            spuId = sku["spuId"]
            sku_data = {}
            sku_data["skuId"] = skuId
            sku_data["missCommonKey"] = False
            sku_data["keyList"] = ["模式1关键字%d" % index]
            skuList.append(sku_data)
    # print(skuList)
    if skuList == []:
        body = {
            "spuList": [{"spuId": spuId, "missCommonKey": "false", "customNumbers": [], "keyList": ["无规格商品关键字"]}]}
    else:
        body = {
            "spuList": [{"spuId": spuId, "missCommonKey": "false", "customNumbers": [], "skuList": skuList}]}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def model_four_add_product(data):
    """
    贴文销售模式4添加商品，只添加第一个商品到贴文
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s/products"%(env,sales_id)
    skuKeys, spuId, response = search_post_product(data)
    skuList = []
    if skuKeys != None:
        for index, sku in enumerate(skuKeys):
            skuId = sku["skuId"]
            spuId = sku["spuId"]
            sku_data = {}
            sku_data["skuId"] = skuId
            sku_data["missCommonKey"] = False
            skuList.append(sku_data)
    # print(skuList)
    customNumbers = "模式4接口关键字下单"
    body = {}
    if skuList == []:
        body = {"spuList": [
            {"spuId": spuId, "missCommonKey": "true", "customNumbers": [customNumbers], "customNumber": customNumbers}]}
    else:
        body = {"spuList": [
            {"spuId": spuId, "missCommonKey": "false", "customNumbers": [customNumbers], "customNumber": customNumbers,
             "skuList": skuList}]}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def modify_post_schedule(data):
    """
    修改贴文排程时间
    :param data: start_time若没有传则默认给当前时间，end_time若没有传则默认是永远有效
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    start_time = int(time.time() * 1000)
    end_time = 32503611599000
    if "start_time" in data:
        start_time = data["start_time"]
    if "end_time" in data:
        end_time = data["end_time"]
    url = "%s/api/posts/post/sales/schedule/%s"%(env,sales_id)
    body = {"start_time": start_time, "end_time": end_time}
    response = requests.put(url,headers=headers,json=body).json()
    return response

def publish_post(data):
    """启用贴文"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    #启用前先修改排程时间，若没有传时间，则按默认值设置
    modify_post_schedule(data)
    url = "%s/api/posts/post/sales/publish/%s"%(env,sales_id)
    response = requests.put(url, headers=headers).json()
    return response

def get_post_info(data):
    """
    获取贴文信息
    :param data:
    :return: 贴文全部信息，若需要调用后再过滤
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s?fieldScopes=DETAILS,PRODUCT_NUM," \
          "SALES_CONFIG,LOCK_INVENTORY,PRODUCT_LIST"%(env,sales_id)
    response = requests.get(url, headers=headers).json()
    return response

def get_post_product_keyword(data):
    """获取贴文返回第一个商品的关键字"""
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/sales/%s?fieldScopes=PRODUCT_LIST" % (env, sales_id)
    response = requests.get(url, headers=headers).json()
    keyword = jsonpath(response,"$..custom_keys_label_str")[0]
    return keyword,response



def send_post_comment(data):
    """
    在贴文下普通留言
    :param data:
    :return:
    """
    #获取关联的贴文信息-第一则贴文
    response = get_post_info(data)
    related_post_list = response["data"]["related_post_list"][0]
    page_id = related_post_list["page_id"]
    post_id = related_post_list["post_id"]
    stamp = int(time.time())
    num = random.randint(100000, 999999)
    user_id = "488864%d" % int(time.time())
    name = "test留言查息%d" % int(time.time())
    env = data["env"]
    # headers = data["headers"]
    # sales_id = data["sales_id"]
    keyword = "接口测试普通留言"
    if "keyword" in data:
        keyword = data['keyword']
    key = data["key"]
    body = {"object": "page", "entry": [{"id": page_id, "time": stamp, "changes": [{"field": "feed", "value": {
        "from": {"id": user_id, "name": name},
        "post": {"status_type": "added_video", "is_published": True, "updated_time": "2022-11-18T09:57:26+0000",
                 "permalink_url": "https://www.facebook.com/permalink.php?story_fbid=pfbid02jLK3e6YdFSXp2DmD7j7vtStLXoBzTi8rxKrp6jFhVMUTTEgz6qvZA8soR9Uwydd8l&id=107977035056574",
                 "promotion_status": "inactive", "id": post_id}, "message": keyword, "item": "comment",
        "verb": "add", "post_id": post_id, "comment_id": "%s_%d%d" % (page_id, stamp, num),
        "created_time": stamp, "parent_id": post_id}}]}]}
    url = "%s/facebook/webhook"%env
    sign_text = hmac.new(key.encode("utf-8"), json.dumps(body).encode("utf-8"), sha1)
    signData = sign_text.hexdigest()
    print(signData)
    header = {"Content-Type": "application/json", "x-hub-signature": "sha1=%s" % signData}
    response = requests.post(url, headers=header, data=json.dumps(body))
    return response

def get_payment(data):
    """
    获取店铺的付款方式，默认查询10条
    :param data:
    :return:默认返回第一个支付方式
    """
    env = data["env"]
    headers = data["headers"]
    url ="%s/openApi/proxy/v1/payments?page=1&per_page=10&include_fields[]=config_data.tappay"%env
    response = requests.get(url, headers=headers).json()
    payment_id = response["data"]["items"][0]["id"]
    return payment_id,response

def get_delivery(data):
    """
    获取店铺的物流方式，默认查询10条
    :param data:
    :return:默认返回第一个物流方式
    """
    # print("物流data",data)
    env = data["env"]
    headers = data["headers"]
    url = "%s/openApi/proxy/v1/delivery_options?page=1&per_page=10"%env
    response = requests.get(url, headers=headers).json()
    delivery_id = response["data"]["items"][0]["id"]
    return delivery_id,response

def get_comment_user(data):
    """
    查询留言面板的留言用户，查全部，并返回第一个留言用户
    :return:post_user_id,编辑购物车，发送购物车链接需要用到这个值
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    url = "%s/api/posts/post/comments"%env
    params = {"pageNo":1,"pageSize":10,"salesId":sales_id}
    response = requests.get(url, headers=headers,params=params).json()
    post_user_id = jsonpath(response, "$..id")[0]
    return post_user_id,response

def post_edit_cart(data):
    """
    编辑购物车，给用户加入查询到的第一个商品：没有排除无库存的情况
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    sales_id = data["sales_id"]
    post_user_id, __ = get_comment_user(data)
    url = "%s/api/posts/post/sales/%s/user/" \
          "%s/cart/item?skip_reapply_promotion=false"%(env,sales_id,post_user_id)
    response = search_oa_product(data)
    variations = response["data"]["items"][0]["variations"]
    spu_id = response["data"]["items"][0]["id"]
    quantity = 1
    if "quantity" in data:
        quantity = data["quantity"]
    body = {"spu_id": spu_id, "owner_type": "Guest", "quantity": quantity, "type": "product"}
    if variations != []:
        sku_id = variations[0]["id"]
        body = {"spu_id": spu_id, "owner_type": "Guest", "sku_id": sku_id, "quantity": quantity,
                "type": "product"}
    response = requests.post(url, headers=headers, json=body).json()
    return response

def manual_order(data):
    """
    创建会员，若存在则合并会员
    创建订单
    :param data:
    :return:
    """
    env = data["env"]
    headers = data["headers"]
    phone = "18776343453"
    if "query" in data:
        phone = data["query"]
    __,response = get_comment_user(data)
    # print("留言面板查询返回",response)
    name = jsonpath(response,"$..name")[0]
    user_id = jsonpath(response,"$..psid")[0]
    page_id = jsonpath(response, "$..page_id")[0]
    # 先查询号码或邮箱是否被占有
    url = "%s/openApi/proxy/v1/customers/search?query=%s&per_page=50&search_fields[]=mobile_phone" \
          "&search_fields[]=phones" %(env,phone)
    response = requests.get(url, headers=headers).json()
    items = response["data"]["items"]
    #创建会员
    url = "%s/uc/customers/merge" % env
    body = {"email": "", "mobile_phone": phone, "mobile_phone_country_calling_code": "86",
            "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
            "id": None, "party_channel_id": page_id, "platform": "FACEBOOK", "is_member": True}
    if items != []:
        id = jsonpath(response, "$..id")[0]
        body = {"email": "", "mobile_phone": phone, "mobile_phone_country_calling_code": "86",
                "name": name, "page_scoped_id": user_id, "locale_code": None, "country_code": "cn",
                "id": id, "party_channel_id": page_id, "platform": "FACEBOOK", "is_member": True}

    res = requests.put(url, headers=headers, json=body).json()
    customer_id = res["data"]["id"]
    #给会员新增物流地址
    rl = "%s/uc/customers/%s" % (env,customer_id)
    postcode = "76653"
    delivery_data = {"delivery_addresses": [
        {"city": "bb", "country": "CN", "postcode": postcode, "recipient_name": name,
         "recipient_phone": phone, "recipient_phone_country_code": "86", "logistic_codes": [],
         "address_1": "aa"}]}
    res = requests.put(url, json=delivery_data, headers=headers).json()
    # print("信息会员物流地址返回",res)

    # 查询会话ID
    platform = "facebook"
    if "platform" in data:
        platform = data["platform"]
    url = "%s/mc/conversation/id?type=%s&user_id=%s&party_channel_id=%s" % (env,platform,user_id, page_id)
    # param = {"type":"facebook","user_id":vars["user_id"],"party_channel_id":vars["platform_channel_id"]}
    response = requests.get(url, headers=headers).json()
    conversation_id = jsonpath(response, "$.data.id")[0]

    # 给cart 设置物流 和设置支付方式
    url = "%s/openApi/proxy/v1/internal/mc/api/carts/%s?owner_type=User&cart_uid=%s&created_by=post&skip_reapply_promotion=false&shop_session_id=%s" % (
    env,customer_id, customer_id, user_id)
    delivery_id,__ = get_delivery(data)
    payment_id,__ = get_payment(data)
    body = {"delivery_option_id": delivery_id, "country": "CN", "countryCode": "CN",
            "payment_id": payment_id}
    res = requests.put(url, headers=headers, json = body).json()
    # print("设置cart",res)
    # 成立订单
    url = "%s/manual_order/checkout"%env
    delivery_address = delivery_data["delivery_addresses"][0]
    delivery_address["district"] = None
    delivery_address["key"] = None
    delivery_address["regioncode"] = None
    delivery_address["province"] = None
    delivery_address["address_2"] = None
    delivery_address["country_code"] = "CN"
    body = {"country": "CN", "customer_email": None, "customer_id": customer_id, "customer_name": name,
            "customer_phone": phone, "whatsapp_phone": phone, "delivery_address": delivery_address,
            "delivery_data": {"recipient_name": name, "recipient_phone": phone},
            "delivery_option_id": delivery_id, "display_payment_info": False, "invoice": {}, "lang": "zh-cn",
            "order_remarks": "", "order_tags": [], "payment_id": payment_id,
            "payment_info": "{\"text\":\"\",\"images\":[]}", "send_notification": False, "created_by": "post",
            "created_from": "admin_post", "platform": "FACEBOOK", "conversation_id": conversation_id,
            "merchant_name": "泰国店", "shop_session_id": user_id, "platform_channel_name": "kkk",
            "source_data": {"type": "fb", "source_id": page_id}, "customer_phone_country_code": "86",
            "postcode": postcode}
    res = requests.post(url,headers=headers,json=body).json()
    # print("创建订单返回",res)
    #获取订单ID
    orderNumber = jsonpath(res,"$..orderNumber")[0]

    return orderNumber,customer_id,res

def get_user_conversation_id(data):
    """
    :return: 会员ID
    """
    # 查询会话ID
    env = data["env"]
    headers = data["headers"]
    user_id = data["user_id"]
    page_id = data["page_id"]
    platform = "facebook"
    if "platform" in data:
        platform = data["platform"]
    url = "%s/mc/conversation/id?type=%s&user_id=%s&party_channel_id=%s" % (env, platform, user_id, page_id)
    # param = {"type":"facebook","user_id":vars["user_id"],"party_channel_id":vars["platform_channel_id"]}
    response = requests.get(url, headers=headers).json()
    conversation_id = jsonpath(response, "$.data.id")[0]
    return conversation_id

def get_user_message(data):
    """
    获取信息
    :param data: 
    :return: 
    """""
    env = data["env"]
    headers = data["headers"]
    # 获取发送的私讯内容
    conversation_id = get_user_conversation_id(data)
    url = "%s/mc/message/%s?create_time="%(env,conversation_id)
    response = requests.get(url,headers=headers).json()
    content = jsonpath(response,"$..content")[0]
    text = ""
    if "message" in json.loads(content):
        text = json.loads(content)["message"]["attachment"]["payload"]["text"]
    return text


def modify_order_status(data):
    """
    :param data:
    status:订单的状态
    confirmed:已确认
    pending：处理中
    completed：已完成
    cancelled ：已取消
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
    res = requests.get(url, headers=oa_headers).json()
    order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()

def modify_order_payment_status(data):
    """
    :param data:
    status:订单的状态
    pending：未付款
    completed：已付款
    refunding ：退款中
    refunded：已退款
    partially_refunded：部分退款
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
    res = requests.get(url, headers=oa_headers).json()
    order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/order_payment_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()

def modify_order_delivery_status(data):
    """
    :param data:
    status:订单的状态
    pending：备货中
    shipping：发货中
    shipped ：已发货
    arrived：已到达
    collected：已取货
    returned：已退货
    returning：退款中
    :return:
    """
    oa_env = data["oa_env"]
    oa_headers = data["oa_headers"]
    status = data["status"]
    # 查询订单id
    global customer_id
    if "customer_id" in data:
        customer_id = data["customer_id"]
    else:
        __,customer_id,__ = manual_order(data)
    url = "%s/v1/orders/search?page=1&per_page=5&customer_id=%s" % (oa_env,customer_id)
    res = requests.get(url, headers=oa_headers).json()
    order_id = jsonpath(res, "$..id")[0]
    # print("订单ID", vars["order_id"])
    # 修改订单状态为-已确认
    url = "%s/v1/orders/%s/order_delivery_status" % (oa_env,order_id)
    body = {
        "status": status,
        "mail_notify": False
    }
    res = requests.patch(url, headers=oa_headers, json=body).json()





if __name__=="__main__":
    pass


