def as_list(node, stream: list):
    if not node:
        return

    stream.append(str(node.data))
    as_list(node.left, stream)
    as_list(node.right, stream)


class Tree:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data

    def insert(self, data: str, qtd: int, last: bool):
        # the left sun should never have a son and only the last right node has a value
        # Compare the new value with the parent node
        if self.data:
            self.data += qtd
            if last and self.left and not self.right:
                self.right = Tree(data)
            elif not self.left:
                self.left = Tree(data)
            elif self.right:
                self.right.insert(data, qtd + self.data, last)
            else:
                self.right = Tree(qtd)
                self.right.insert(data, qtd + self.data, last)
        else:
            self.data = qtd
            self.left = Tree(data)

    def search(self, char: str, start_bit_str='') -> str:
        if type(self.data) == int:
            if self.left.data == char:
                return start_bit_str + '0'
            else:
                if self.right:
                    return self.right.search(char, start_bit_str + '1')
                else:
                    return ''
        elif self.data == char:
            # ultimo valor a direita
            return start_bit_str
        else:
            return ''

    def find_symbol_by_bytes(self, param: str, start_bit_str='') -> str:
        if type(self.data) == int:
            # valida se com a adição do bit 0 no final da string vai ser o mesmo dos bits enviados para comparação
            # caso for retorna o valor da esquerda se não prosegue pelos filhos da direita
            if start_bit_str + '0' == param:
                return self.left.data
            else:
                if self.right:
                    return self.right.find_symbol_by_bytes(param, start_bit_str + '1')
                return ''
        else:
            # ultimo valor a direita
            if start_bit_str == param:
                return self.data
            else:
                return ''


