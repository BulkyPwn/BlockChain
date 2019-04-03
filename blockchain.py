import hashlib

class Block:
    # 区块结构体
    #     prev_hash
    #     data
    #     timestamp
    #     hash
    def __init__(self,data,prev_hash,root_hash):
        self.previous_hash = prev_hash
        self.data = data
        self.root_hash = root_hash
        self.h = ""
        self.nonce = ""

    #计算区块的哈希值
    @property
    def hash(self):
        message = hashlib.sha256()
        message.update(str(self.previous_hash).encode("utf-8"))
        message.update(str(self.data).encode("utf-8"))
        message.update(str(self.root_hash).encode("utf-8"))
        message.update(str(self.nonce).encode("utf-8"))
        digest = message.hexdigest()
        return digest



def create_genesis_block():
    return Block(data="Genesis Block",prev_hash="",root_hash="")

class BlockChain:
    #区块链结构体
    #   blocks： 包含的区块列表
    def __init__(self):
        self.blocks = [create_genesis_block()]#初始化创建 创世区块

    def add_block(self,data,node_datas):
        #添加区块
        #param block
        #return:

        import sys
        sys.path.append("D:\Python Projects/venv/")
        import Merkle_Tree
        Merkle_Tree.update_packing_mt(node_datas,1)

        if len(self.blocks)>0:
            prev_block = self.blocks[len(self.blocks)-1]
        import pymongo
        conn = pymongo.MongoClient()
        db = conn.test
        handler = db.packing_mt
        root_hash = handler.find({"_id":0})[0]["Hash"]
        if len(self.blocks) > 0:
            new_block = Block(data,prev_block.hash,root_hash)
        else:
            new_block = Block(data,tail_hash, root_hash)
        pow = ProofOfWork(new_block)
        nonce,digest = pow.mine()
        new_block.nonce = nonce
        new_block.h = digest
        self.blocks.append(new_block)
        return new_block

class ProofOfWork():
    #工作量证明
    def __init__(self,block):
        self.block = block

    def mine(self):# 出块时间：约为0.001001second
        #挖矿函数
        i = 0
        prefix = "0000"
        # import datetime
        # start_time = datetime.datetime.now()

        while True:
            nonce = str(i)
            message = hashlib.sha256()
            message.update(str(self.block.previous_hash).encode("utf-8"))
            message.update(str(self.block.data).encode("utf-8"))
            message.update(str(self.block.root_hash).encode("utf-8"))
            message.update(nonce.encode("utf-8"))
            digest = message.hexdigest()
            if digest.startswith(prefix):
                # end_time = datetime.datetime.now()
                # print(end_time - start_time)
                return nonce,digest
            i += 1
            # print(i)

def drop_blockchain():
    import pymongo
    conn = pymongo.MongoClient()
    db = conn.test
    handler = db.blockchain
    handler.drop()

def test_product_one_block_time():
    import datetime #计算出块时间：出块时间约为 5.595643s
    start_time = datetime.datetime.now()

    node_datas = ["Jack send 0.3 BTC to Alice", "Jack send 0.5 BTC to Bob", "Bob send 0.5 BTC to Bob",
                  "Tom send 0.2 BTC to Bob", "Bob send 0.3 BTC to Alice", "3303:Analysis Succeeded",
                  "1024:Analysis Failed"]  # 块内 默克尔树 存储数据
    bc.add_block("Alice gives her key to Bob", node_datas)  # 块头 存储数据

    end_time = datetime.datetime.now()
    print(end_time - start_time)

def main():
    #drop_blockchain()

    bc = BlockChain()

    ##判断该链是否为空：若为空，新建bc；若不空，则获取链尾哈希
    import pymongo
    conn = pymongo.MongoClient()
    db = conn.test
    handler = db.blockchain.find()
    try:
        if(handler[0]["_id"] != ""):
            bc.blocks = []
            global tail_hash
            tail_hash = db.blockchain.find().sort("_id",pymongo.DESCENDING)[0]["Hash"]
    except:
        print("区块链为空")

    data = "ALOHA"
    node_datas = ["Data1", "Data2", "Data3",
                  "Data4", "Data5", "Data6",
                  "Data7"]

    bc.add_block(data,node_datas)


    # ##需手动设置 node_datas 、 bc.add_block(data,node_datas)##
    # node_datas = ["Jack send 0.3 BTC to Alice", "Jack send 0.5 BTC to Bob", "Bob send 0.5 BTC to Bob",
    #               "Tom send 0.2 BTC to Bob", "Bob send 0.3 BTC to Alice", "3303:Analysis Succeeded",
    #               "1024:Analysis Failed"]#块内 默克尔树 存储数据
    # b1 = bc.add_block("Alice gives her key to Bob",node_datas)#块头 存储数据
    #
    # node_datas = ["Data1", "Data2", "Data3",
    #               "Data4", "Data5", "Data6",
    #               "Data7"]
    # b2 = bc.add_block("Winter is coming.",node_datas)

    # node_datas = ["Jack send 0.3 BTC to Alice", "Jack send 0.5 BTC to Bob", "Bob send 0.5 BTC to Bob",
    #               "Tom send 0.2 BTC to Bob", "Bob send 0.3 BTC to Alice", "3303:Analysis Succeeded",
    #               "1024:Analysis Failed"]
    # b3 = bc.add_block("Valar Morghulis",node_datas)
    #
    # node_datas = ["Jack send 0.3 BTC to Alice", "Jack send 0.5 BTC to Bob", "Bob send 0.5 BTC to Bob",
    #               "Tom send 0.2 BTC to Bob", "Bob send 0.3 BTC to Alice", "3303:Analysis Succeeded",
    #               "1024:Analysis Failed"]
    # b4 = bc.add_block("Valar Dohaeris",node_datas)

    import pymongo

    conn = pymongo.MongoClient()
    db = conn.test

    for b in bc.blocks:
        handler = db.blockchain
        handler.insert_one({"Prev_Hash": b.previous_hash,"Data":b.data,"Hash":b.hash,"Root_Hash":b.root_hash,"Nonce":b.nonce})
        print("Prev Hash:{}".format(b.previous_hash))
        print("Data:{}".format(b.data))
        print("Hash:{}".format(b.hash))
        print("Root_Hash:{}".format(b.root_hash))
        print("Nonce:{}".format(b.nonce))
        print("\n")

    print("新区块插入成功！")

    # b1.data = "Jack send 1.3 BTC to Alice"#篡改b1区块的data
    #
    # for i,b in enumerate(bc.blocks):#本地篡改_本地验证
    #     print("Prev Hash:{}".format(b.previous_hash))
    #     print("Data:{}".format(b.data))
    #     print("Hash:{}".format(b.hash))
    #     if b.previous_hash and b.previous_hash != bc.blocks[i-1].hash:
    #         print("Invalid Block")
    #     else:
    #         print("Valid Block")
    #     print("\n")

main()