import hashlib

class Block:
    # 区块结构体
    #     prev_hash
    #     data
    #     timestamp
    #     hash
    def __init__(self,data,prev_hash):
        self.previous_hash = prev_hash
        self.data = data
        self.nonce = ""

    #计算区块的哈希值
    @property
    def hash(self):
        message = hashlib.sha256()
        message.update(str(self.data).encode("utf-8"))
        message.update(str(self.nonce).encode("utf-8"))
        digest = message.hexdigest()
        return message.hexdigest()



def create_genesis_block():
    return Block(data="Genesis Block",prev_hash="")

class BlockChain:
    #区块链结构体
    #   blocks： 包含的区块列表
    def __init__(self):
        self.blocks = [create_genesis_block()]#初始化创建 创世区块

    def add_block(self,data):
        #添加区块
        #param block
        #return:
        prev_block = self.blocks[len(self.blocks)-1]
        new_block = Block(data,prev_block.hash)
        pow = ProofOfWork(new_block)
        nonce,digest = pow.mine()
        new_block.nonce = nonce
        self.blocks.append(new_block)
        return new_block

class ProofOfWork():
    #工作量证明
    def __init__(self,block):
        self.block = block

    def mine(self):# 出块时间：约为0.001001second
        #挖矿函数
        i = 0
        prefix = "3"
        # import datetime
        # start_time = datetime.datetime.now()

        while True:
            nonce = str(i)
            message = hashlib.sha256()
            message.update(str(self.block.data).encode("utf-8"))
            message.update(nonce.encode("utf-8"))
            digest = message.hexdigest()
            if digest.startswith(prefix):
                # end_time = datetime.datetime.now()
                # print(end_time - start_time)
                return nonce,digest
            i += 1
            print(i)



def main():
    bc = BlockChain()

    b1 = bc.add_block("Jack send 0.3 BTC to Alice")
    # b2 = bc.add_block("Alice send 0.1 BTC to Tom")

    for b in bc.blocks:
        print("Prev Hash:{}".format(b.previous_hash))
        print("Data:{}".format(b.data))
        print("Hash:{}".format(b.hash))
        print("\n")

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

