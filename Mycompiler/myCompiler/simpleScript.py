from enums import ASTNodeType
from simpleParser import SimpleParser

class SimpleScript:
    def __init__(self):
        self.variables = {}
        self.verbose = False
        self.parser = SimpleParser()

    def run(self):
     while True:
         try:
             code = input(">>> ")
             if code == "exit();":
                 print("good bye!")
                 break
             if code.endswith(";"):
                 tree = self.parser.parser(code)
                 if self.verbose:
                     self.parser.dumpAST(tree, "")
                 self.evaluate(tree, "")
                 # print("\n")
         except Exception as e:
                print(e)
                # print("\n")

    def evaluate(self, node, indent):
        result = None
        if self.verbose:
            print(indent, "Calculating: ", node.node_type)
        if node.node_type == ASTNodeType.Programm:
            for child in node.children:
                result = self.evaluate(child, indent)
        elif node.node_type == ASTNodeType.Additive:
            child1 = node.children[0]
            value1 = self.evaluate(child1, indent + "\t")
            child2 = node.children[1]
            value2 = self.evaluate(child2, indent + "\t")
            if node.text == "+":
                result = int(value1) + int(value2)
            else:
                result = int(value1) - int(value2)
        elif node.node_type == ASTNodeType.Multiplicative:
            child1 = node.children[0]
            value1 = self.evaluate(child1, indent + "\t")
            child2 = node.children[1]
            value2 = self.evaluate(child2, indent + "\t")
            if node.text == "*":
                result = int(value1) * int(value2)
            else:
                result = int(value1) // int(value2)
        elif node.node_type == ASTNodeType.IntLiteral:
            result = node.text
        elif node.node_type == ASTNodeType.Identifier:
            varname = node.text
            result = self.variables.get(varname, "undefined")
            if result == "undefined":
                raise Exception("unknown variable: ", varname)
            if not result:
                raise Exception("variable ", varname, " has not been set any value")
        elif node.node_type == ASTNodeType.AssignmentStmt:
            varname = node.text
            result = self.variables.get(varname, "undefined")
            if result == "undefined":
                raise Exception("unknown variable: ", varname)
        elif node.node_type == ASTNodeType.IntDeclaration:
            varname = node.text
            varvalue = None
            if node.children:
                child = node.children[0]
                result = self.evaluate(child, indent + "\t")
                varvalue = int(result)
            self.variables[varname] = varvalue
        if self.verbose:
            print(indent, "Result: ", result)
        elif indent == "":
            if node.node_type in (ASTNodeType.IntDeclaration, ASTNodeType.AssignmentStmt):
                print(node.text, ": ", result)
            elif node.node_type != ASTNodeType.Programm:
                print(result)
        return result


s = SimpleScript()
s.run()