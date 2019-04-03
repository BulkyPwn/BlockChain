import hashlib

class MerkleTree_node:
    def __init__(self,id,data,lhash,rhash):
        self.id = id
        self.data = data
        self.lhash = lhash
        self.rhash = rhash
        self.hash = MerkleTree_node.hash(self)

    def hash(self):
        message = hashlib.sha256()
        message.update(str(self.data+self.lhash+self.rhash).encode("utf-8"))
        return message.hexdigest()

def create_root():
    return MerkleTree_node(id=0,data="Root",lhash="",rhash="")

def create_node(node_id,node_data,left,right):
    return MerkleTree_node(id=node_id,data=node_data,lhash=left,rhash=right)

def update_one_node(id,mt,flag,mask):
    import pymongo
    conn = pymongo.MongoClient()
    db = conn.test
    handler = db.packing_mt

    updating_node_id = id
    if mask == 0 :
        print("本次更新id为 "+str(id))
    if len(mt.nodes) > id * 2 + 1 :
        for record in handler.find({"_id":updating_node_id * 2 +1}):
            updating_lhash = record["Hash"]
            if mask == 0:
                print("更新结点LHash为 "+updating_lhash)
        if len(mt.nodes) > id * 2 + 2:
            for record in handler.find({"_id": updating_node_id * 2 + 2}):
                updating_rhash = record["Hash"]
                if mask == 0:
                    print("更新结点RHash为 "+updating_rhash)
        else:
            updating_rhash = ""
    else:
        updating_lhash = ""
        updating_rhash = ""

    for record in handler.find({"_id": id}):
        hashing_data = record["Data"]
        if mask == 0 :
            print("更新节点Data为 "+hashing_data)

    m = hashlib.sha256()
    m.update(str(hashing_data + updating_lhash + updating_rhash).encode("utf-8"))
    updating_hash = m.hexdigest()

    handler.update_one({"_id": id},{ "$set":{"LHash": updating_lhash, "RHash": updating_rhash, "Hash": updating_hash}})
    if(flag == 0 & mask == 0):
        print("更新成功！(共更新 1 条记录)")


def update_one_way_of_one_node(id,mt,flag,mask):
    updating_id = id
    count = 0
    halt = 0
    while updating_id >= 0:
        update_one_node(updating_id,mt,1,mask)
        count+=1
        updating_id = int((updating_id-1)/2)
        if (updating_id == 0) & (halt == 1):
            updating_id = -1
        if updating_id == 0:
            halt = 1
    if(flag == 0 & mask == 0):
        print("更新成功！(共更新 "+str(count)+" 条记录)")

def update_all_tree(mt,mask):
    i = len(mt.nodes) - 1
    count = 0
    while i>=0:
        update_one_way_of_one_node(i, mt,1,mask)
        i -= 1
        count+=1
    if mask == 0:
        print("更新成功！(共更新 "+str(count)+" 条记录)")

def insert_one_node(mt,mask):
    import pymongo
    conn = pymongo.MongoClient()
    db = conn.test
    handler = db.packing_mt

    n = mt.nodes[len(mt.nodes) - 1]
    handler.insert_one({"_id": n.id,"Data":n.data,"LHash":n.lhash,"RHash":n.rhash,"Hash":n.hash})
    if mask == 0:
        print("id:{}".format(n.id))
        print("Data:{}".format(n.data))
        print("LHash:{}".format(n.lhash))
        print("RHash:{}".format(n.rhash))
        print("Hash:{}".format(n.hash))
        print("\n")

        print("哈希值插入成功！")

class merkle_t:
    def __init__(self,mask):
        self.nodes = [create_root()]
        insert_one_node(self,mask)

    def add_node(self,node_data,left,right,mask):
        new_node = create_node(len(self.nodes),node_data,left,right)
        self.nodes.append(new_node)
        insert_one_node(self,mask)
        return new_node

def drop_packing_mt():
    import pymongo
    conn = pymongo.MongoClient()
    db = conn.test
    handler = db.packing_mt
    handler.drop()

def update_packing_mt(node_datas,mask):
    # mt = merkle_t()
    # n1 = mt.add_node(node_data="Jack send 0.3 BTC to Alice", left="", right="")  # 添加一个结点
    # n2 = mt.add_node(node_data="Jack send 0.5 BTC to Bob", left="", right="")
    # n3 = mt.add_node(node_data="Bob send 0.5 BTC to Bob", left="", right="")
    # n4 = mt.add_node(node_data="Tom send 0.2 BTC to Bob", left="", right="")
    # n5 = mt.add_node(node_data="Bob send 0.3 BTC to Alice", left="", right="")
    # n6 = mt.add_node(node_data="3303:Analysis Succeeded", left="", right="")
    # n7 = mt.add_node(node_data="1024:Analysis Failed", left="", right="")

    drop_packing_mt()

    mt = merkle_t(mask)
    n1 = mt.add_node(node_data=node_datas[0], left="", right="",mask=mask)  # 添加一个结点
    n2 = mt.add_node(node_data=node_datas[1], left="", right="",mask=mask)
    n3 = mt.add_node(node_data=node_datas[2], left="", right="",mask=mask)
    n4 = mt.add_node(node_data=node_datas[3], left="", right="",mask=mask)
    n5 = mt.add_node(node_data=node_datas[4], left="", right="",mask=mask)
    n6 = mt.add_node(node_data=node_datas[5], left="", right="",mask=mask)
    n7 = mt.add_node(node_data=node_datas[6], left="", right="",mask=mask)
    if mask == 0:
        print("最后一个结点的序号为 " + str(len(mt.nodes) - 1))
        print("\n")

    update_all_tree(mt,mask)

    if mask:
        print("当前操作区块的默克尔树已更新！")

def main():
    node_datas = ["Jack send 0.3 BTC to Alice","Jack send 0.5 BTC to Bob","Bob send 0.5 BTC to Bob","Tom send 0.2 BTC to Bob","Bob send 0.3 BTC to Alice","3303:Analysis Succeeded","1024:Analysis Failed"]

    update_packing_mt(node_datas,0)

    # import pymongo
    #
    # conn = pymongo.MongoClient()
    # db = conn.test
    #
    #
    # handler = db.mt

    # for n in mt.nodes:
    #     handler.insert_one({"_id": n.id,"Data":n.data,"LHash":n.lhash,"RHash":n.rhash,"Hash":n.hash})
    #     print("id:{}".format(n.id))
    #     print("Data:{}".format(n.data))
    #     print("LHash:{}".format(n.lhash))
    #     print("RHash:{}".format(n.rhash))
    #     print("Hash:{}".format(n.hash))
    #     print("\n")
    #
    # print("哈希值插入成功！")

main()