class ASTNode:
    def __init__(self, node_type, text):
        self.node_type = node_type
        self.text = text
        self.parent = None
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self
