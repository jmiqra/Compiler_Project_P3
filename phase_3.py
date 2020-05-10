import phase_2
import tokens
from treelib.treelib import Node, Tree

astree = phase_2.getAstree()
localSymbolTable = {}
functionSymbolTable = [] # funcId, ret type
globalSymbolTable = {}
breakFound = False

typeMap = {tokens.T_IntConstant.split("_")[1]: tokens.T_Int, tokens.T_DoubleConstant.split("_")[1]:tokens.T_Double, tokens.T_BoolConstant.split("_")[1]: tokens.T_Bool, tokens.T_StringConstant.split("_")[1]: tokens.T_String }


def printDebug(debug):
    #print(debug)
    return True

def printFunction(errStr):
    print(errStr)
    return True

def handleError(err, astreeNode):
    astreeNodeInfo = astreeNode.identifier.split("_")
    lineNo = astreeNodeInfo[1]
    colNo = astreeNodeInfo[2]

    printFunction("\n*** Error line " + str(lineNo) + ".")
    printFunction(phase_2.phase_1.lines[int(lineNo)-1])
    errStr = ""
    for i in range(int(colNo) - len(astreeNode.tag.split(":")[1].strip())):
        errStr += " "
    for j in range(len(astreeNode.tag.split(":")[1].strip())):
        errStr += "^"
    printFunction(errStr)
    printFunction(err)
    print()
    return True


def dfsStart(root): 
    dfsVisit = {} 
    dfsTreeTraverse(root, dfsVisit)


def dfsTreeTraverse(v, dfsVisit): 
    global localSymbolTable
    dfsVisit[str(v)] = True
    astreeNode = astree.get_node(v)
    printDebug("inside dfstraverse astreeNode is" +  str(astreeNode))
    if "Expr" in astreeNode.identifier:

        printDebug("Type of Expr" +  astreeNode.tag)
        childList = astree.children(astreeNode.identifier)
        leftOperand = childList[0]
        operator = childList[1]
        rightOperand = childList[2]

        if "Expr" in leftOperand.tag:
            printDebug("leftOperandType is Expr")
            leftOperandType = dfsTreeTraverse(leftOperand.identifier, dfsVisit)
            if leftOperandType == "False":
                return 
        else:
            printDebug("leftOperandType found")
            leftOperandType = findSymbolType(leftOperand)
        
        if "Expr" in rightOperand.tag:
            printDebug("rightOperandType is Expr")
            rightOperandType = dfsTreeTraverse(rightOperand.identifier, dfsVisit)
            if rightOperandType == "False":
                return
        else:
            printDebug("rightOperandType found")
            rightOperandType = findSymbolType(rightOperand)

        if leftOperandType == rightOperandType:
            printDebug("left right type matched" + leftOperandType)
            printDebug("operator " + operator.tag)
            if operator.tag.split(":")[1].strip() in tokens.boolOP:
                return "bool"            
            return leftOperandType
        elif leftOperandType == None or rightOperandType == None:
            return None
        else:
            handleError("*** Incompatible operands: " + leftOperandType + " " + operator.tag.split(":")[1].strip() + " " + rightOperandType, operator)
            return None

    elif "FnDecl" in astreeNode.tag:
        printDebug("inside fundecl handler...............")
        tempFuncInfo = {}
        paramCount = 1
        childList = astree.children(astreeNode.identifier)
        for c in childList:
            if "(return type)" in c.tag:
                tempFuncInfo["returnType"] = c.tag.split(":")[1].strip()
            elif "Identifier" in c.tag:
                funcId = c.tag.split(":")[1].strip()
                
                tempFuncInfo["identifier"] = funcId
            
            elif "(formals)" in c.tag:
                grandChildList = astree.children(c.identifier)
                type = grandChildList[0].tag.split(":")[1].strip()
                tempFuncInfo["param_" + str(paramCount)] = type
                paramCount += 1
                #putting vardecl in table
                identifier = grandChildList[1].tag.split(":")[1].strip()
                localSymbolTable[identifier] = type

            elif "(body)" in c.tag:
                dfsTreeTraverse(c.identifier, dfsVisit)
                functionSymbolTable.append(tempFuncInfo)
                #find returnStmt
                returnNode = None
                childList = astree.children(c.identifier)
                printDebug("<<<<<<<<<<<<<<<<<<<>>>>>>>>>>>>>>>>>>>")
                for c in childList:
                    printDebug(c)
                    if "ReturnStmt" in c.tag:
                        printDebug("return found")
                        returnNode = c

                printDebug("RETURN CHILD..." +  str(returnNode))
                if returnNode != None:
                    printDebug("return found")
                    returnExpr = astree.siblings(returnNode.identifier)[-1]
                    if "Constant" in returnExpr.tag:
                        type = findSymbolType(returnExpr)
                    else:
                        type = dfsTreeTraverse(astree.siblings(returnNode.identifier)[-1].identifier, dfsVisit)
                    if type != tempFuncInfo["returnType"]:
                        print("*** Incompatible return: ",type, "given, ", tempFuncInfo["returnType"], " expected")
                else:
                    printDebug("... not sure")
                printDebug("function SymbolTable ..." + str(functionSymbolTable))
                localSymbolTable.clear()
                break
                #todo return type match handle
        return

    elif "Call" in astreeNode.tag:
        printDebug("function Call found")
        childList = astree.children(astreeNode.identifier)
        numOfParam = len(childList) - 1
        funcId = childList[0].tag.split(":")[1].strip()
        func = findFuncById(funcId)
        if func == None:
            handleError("*** No declaration for Function " + "\'" + funcId + "\'" + "found", childList[0])
        else:
            numberofParamInTable = len(func) - 2
            if numberofParamInTable != numOfParam:
                handleError("*** Function " + "\'" + funcId + "\'" + " expects " + str(numberofParamInTable) + " arguments but " + str(numOfParam) + " given", childList[0])
            else:
                for i in range(1, len(childList)):
                    if "FieldAccess" in childList[i].tag or "Constant" in childList[i].tag:
                        printDebug("constant found")
                        type = findSymbolType(childList[i])
                        printDebug("type " + type)
                    else:
                        printDebug("constant not found")
                        type = dfsTreeTraverse(childList[i].identifier, dfsVisit)
                    if type != func["param_" + str(i)]:
                        handleError("*** Incompatible argument " + str(i) + ": " + type + " given, " + func["param_" + str(i)] +  " expected", childList[i])
                        break
                    else:
                        printDebug("good to go...")

        return func["returnType"]
     
# for scope search   
    for i in astree.children(v): 
        #printDebug(i)
        if dfsVisit.get(str(i.identifier)) == None:
            #printDebug(i.identifier, " ",i.tag ) 
            #printDebug("not found")
            if "AssignExpr" in i.tag:
                printDebug("assignment expr found.....")
                fieldAccess = astree.children(i.identifier)
                grandChildList = astree.children(fieldAccess[0].identifier)
                identifier = grandChildList[0].tag.split(":")[1].strip()
                printDebug(localSymbolTable)
                printDebug("identifier = " + identifier)
                leftOperandType = localSymbolTable.get(identifier)
                printDebug("type = " + leftOperandType)
                #do type check
                
                expr = astree.siblings(fieldAccess[0].identifier)
                printDebug("expr" +  str(expr))
                if "FieldAccess" in expr[1].tag or "Constant" in expr[1].tag:
                    rightOperandType = findSymbolType(expr[1])
                else:
                    printDebug(expr)
                    rightOperandType = dfsTreeTraverse(expr[1].identifier, dfsVisit)
                if leftOperandType != rightOperandType and not (leftOperandType == None or rightOperandType == None):
                    printDebug("typerightOperand " + str(rightOperandType))
                    handleError("*** Incompatible operands: " + leftOperandType + " = " + rightOperandType, expr[0])
                continue
            elif "VarDecl" in i.tag:
                parent = astree.parent(i.identifier)
                
                childList = astree.children(i.identifier)
                type = childList[0].tag.split(":")[1].strip()
                identifier = childList[1].tag.split(":")[1].strip()
                if parent.identifier == "Program":
                    globalSymbolTable[identifier] = type
                else:
                    localSymbolTable[identifier] = type
                printDebug("symboltable ********************" + str(localSymbolTable))
                printDebug("global symboltable ********************"+ str(globalSymbolTable))

                continue
            elif "LogicalExpr" in i.tag:
                printDebug("logical expr found")
                sthExpr = astree.children(i.identifier)
                if "FieldAccess" in sthExpr[1].tag or "Constant" in sthExpr[1].tag:
                    printDebug("inside if field or const")
                    type = findSymbolType(sthExpr[1])
                else:
                    printDebug("inside else field or const")
                    type = dfsTreeTraverse(i.identifier, dfsVisit)
                printDebug("type =" +  type)
                continue
            elif "ForStmt" in i.tag or "WhileStmt" in i.tag:
                printDebug("for found")
                breakFound = True
                dfsTreeTraverse(i.identifier, dfsVisit)
                breakFound = False
            elif "BreakStmt" in i.tag and breakFound != True:
                print("*** break is only allowed inside a loop")
            
            elif "Call" in i.tag:
                printDebug("function Call found")
                childList = astree.children(i.identifier)
                numOfParam = len(childList) - 1
                funcId = childList[0].tag.split(":")[1].strip()
                func = findFuncById(funcId)
                if func == None:
                    handleError("*** No declaration for Function " + "\'" + funcId + "\'" + "found", childList[0])
                else:
                    numberofParamInTable = len(func) - 2
                    if numberofParamInTable != numOfParam:
                        handleError("*** Function " + "\'" + funcId + "\'" + " expects " + str(numberofParamInTable) + " arguments but " + str(numOfParam) + " given", childList[0])
                    else:
                        for j in range(1, len(childList)):
                            if "FieldAccess" in childList[j].tag or "Constant" in childList[j].tag:
                                printDebug("constant found")
                                
                                type = findSymbolType(childList[j])
                            else:
                                printDebug("constant not found")
                                type = dfsTreeTraverse(childList[j].identifier, dfsVisit)
                            if type != func["param_" + str(j)]:
                                handleError("*** Incompatible argument " + str(j) + ": " + type + " given, " + func["param_" + str(j)] +  " expected", childList[j])
                                break
                            else:
                                printDebug("good to go...")
            else:
                dfsTreeTraverse(i.identifier, dfsVisit)
        else:
            pass


def findSymbolType(astreeNode): 
    printDebug("inside findSymbolType() ")
    if "FieldAccess" in astreeNode.tag:
        printDebug("fieldaccess found....")
        childList = astree.children(astreeNode.identifier)
        if "Identifier" in childList[0].tag:
            ident  = childList[0].tag.split(":")[1].strip()
            type = localSymbolTable.get(ident)
            printDebug("ident" + ident)
            printDebug("localSymbol" + str(localSymbolTable))
            ############# if not found... type error
            if type == None:
                print("********variable not found in local")
                type = globalSymbolTable.get(ident)
                if type == None:
                    return "False"
                else:
                    return type
            return type
    else:
        #param inside typeMap.get(param)
        #param =   5$IntConstant: 5
        key = astreeNode.tag.split(":")[0].split("$")[1]
        if ")" in key:
            key = key.split(")")[1].strip()
        type =  typeMap.get(key)      
        return type


def findFuncById(ident):
    for func in functionSymbolTable:
        printDebug(func)
        if func.get("identifier") == ident:
            return func
    return None


def main():
    #astree.show(key = False, line_type = 'ascii-sp')
    #printDebug(astree.size())
    root = astree.root
    #printDebug(root)
    #printDebug("children.....", astree.children(root)[0].identifier)
    dfsStart(root)
    printDebug(typeMap)
    print()

if __name__ == "__main__":
    main()