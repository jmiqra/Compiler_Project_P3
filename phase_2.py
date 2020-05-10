"""
@author: iqrah
"""

import sys
import tokens
import phase_1
from treelib.treelib import Node, Tree

astree = Tree()
astree.create_node("   $Program:", "Program") # abstract syntax tree root
parent = "Program"
prefix = ""

errorFound = False

def printDebug(str):
    #print(str)
    return True

def printFunction(str):
    global errorFound 
    if not errorFound:
        print(str)
    return True

t = phase_1.get_next_token()
printDebug(t)

def next_token():
    global t
    t = phase_1.get_next_token()
    printDebug(t)
    if t != None:
        return True
    else:
        return False

def find_line(t):
    return phase_1.lines[t.lineno-1]

def find_col(t):
    #str(find_column(input_str, t)) + "-" + 
    #str(find_column(input_str, t)+len(str(t.value))-1)
    return phase_1.find_column(phase_1.input_str, t) - 1

def find_node_id(t, id):
    node_id = id + "_" + str(t.lineno) + "_" + str(find_col(t))
    return node_id

def update_parent(par):
    global parent
    parent = par
    return True

def clear_prefix():
    global prefix
    prefix = ""
    return True

def set_prefix(pre_str):
    global prefix
    prefix = pre_str
    return True

def handleError(t):
    global errorFound
    if not errorFound:
        print()
        printFunction("*** Error line " + str(t.lineno) + ".")
        printFunction(find_line(t))
        #printDebug(find_col(t))
        err_str = ""
        for i in range(find_col(t)):
            err_str += " "
        for j in range(len(t.value)):
            err_str += "^"
        printFunction(err_str)
        printFunction("*** syntax error")
        print()
        print()
        errorFound = True
        return True
    else:
        return False

def program_start():
    printDebug("------program")
    if t == None:
        printFunction("Empty program is syntactically incorrect.")
        #handleError(t)
        return False
    return decl() and program()

def program():
    #next_token()
    if t == None:
        printDebug("Program ended successfully!")
        return True
    else:
        return program_start()


def decl():
    global parent
    prevPar = parent
    printDebug("------decl " + str(t))
    if(t.value in tokens.type_list or t.value == tokens.T_Void):
        dataType = t.value
        next_token()
        if(t.type == tokens.T_Identifier):
            ident = t.value
            next_token()
            if(t.value == tokens.T_LP):
                node_id = find_node_id(t, "FnDecl")
                node_label = "  " + str(t.lineno) + "$" + "FnDecl:"
                astree.create_node( node_label, node_id, parent=parent)
                
                parent = node_id
                
                node_label = "   " + "$" + "(return type) Type: " + dataType
                astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                node_label = "  " + str(t.lineno) + "$" + "Identifier: " + ident
                astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)

                return functionDecl() and update_parent(prevPar)
            else:
                node_id = find_node_id(t, "VarDecl")
                node_label = "  " + str(t.lineno) + "$" + "VarDecl:"
                astree.create_node( node_label, node_id, parent=parent)
                
                parent = node_id

                node_label = "   " + "$" + "Type: " + dataType
                astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                node_label = "  " + str(t.lineno) + "$" + "Identifier: " + ident
                astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)

                return variableDecl() and next_token() and update_parent(prevPar)
        else:
            printDebug("Syntax Error 1 " + str(t))
            handleError(t)
            return False
    else:
        printDebug("Syntax Error 2 " + str(t))
        handleError(t)
        return False

def functionDecl():
    printDebug("------funtionDecl")
    next_token()
    params = formals()
    next_token()
    return params and stmtBlock()

def formals():
    printDebug("------formals")
    global parent
    prevPar = parent
    if t.value == tokens.T_RP:
        return True
    while True:
        if t.value in tokens.type_list:
            dataType = t.value
            next_token()
            if(t.type == tokens.T_Identifier):
                ident = t.value
                next_token()
                if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
                    node_id = find_node_id(t, "VarDecl")
                    node_label = "  " + str(t.lineno) + "$" + "(formals) VarDecl:"
                    astree.create_node( node_label, node_id, parent=parent)
                    
                    parent = node_id

                    node_label = "   " + "$" + "Type: " + dataType
                    astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                    node_label = "  " + str(t.lineno) + "$" + "Identifier: " + ident
                    astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)
                    update_parent(prevPar)
                    continue
                elif t.value == tokens.T_RP:

                    node_id = find_node_id(t, "VarDecl")
                    node_label = "  " + str(t.lineno) + "$" + "(formals) VarDecl:"
                    astree.create_node( node_label, node_id, parent=parent)
                    
                    parent = node_id

                    node_label = "   " + "$" + "Type: " + dataType
                    astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

                    node_label = "  " + str(t.lineno) + "$" + "Identifier: " + ident
                    astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)

                    return True and update_parent(prevPar)
            else:
                handleError(t)
                return False

def stmtBlock():
    printDebug("------stmtBlock" + str(t))
    
    global parent
    prevPar = parent
    node_label = "   " + "$" + "(body) StmtBlock:"
    node_id = find_node_id(t, "StmtBlock")
    astree.create_node( node_label, node_id , parent= parent)
    parent = node_id
    
    if t.value == tokens.T_LC:
        next_token()
        if t.value == tokens.T_RC:
            return True and update_parent(prevPar)
        else:
            stmtBlockParam = variableDecl_2() and t.value == tokens.T_RC
            printDebug("~~~~~~ " + str(t))
            next_token()
            return stmtBlockParam and update_parent(prevPar)

def variableDecl():
    printDebug("------variableDecl")
    if(t.value == tokens.T_SemiColon):
        return True
    else:
        handleError(t)
        return False

def variableDecl_2():
    global parent
    prevPar = parent
    printDebug("------variableDecl_2")
    #if t.value == tokens.T_RC:
    #        return True
    dataType = t.value
    if t.value in tokens.type_list and next_token() and t.type == tokens.T_Identifier:
        ident = t.value
        next_token()
        
        node_id = find_node_id(t, "VarDecl")
        node_label = "  " + str(t.lineno) + "$" + "VarDecl:"
        astree.create_node( node_label, node_id, parent=parent)
        
        parent = node_id

        node_label = "   " + "$" + "Type: " + dataType
        astree.create_node( node_label, find_node_id(t, "Type"), parent=parent)

        node_label = "  " + str(t.lineno) + "$" + "Identifier: " + ident
        astree.create_node( node_label, find_node_id(t, "Identifier"), parent=parent)
        update_parent(prevPar)
        return variableDecl() and next_token() and variableDecl_2()
    else:
        while True:
            if stmt():
                if t.value == tokens.T_RC:
                    printDebug("true from varDecl_2")
                    return True
                if(t.value == tokens.T_Else):
                    printDebug("else found")
                    return True
                next_token()
                pass
            else:
                return True


def stmt():
    printDebug("------stmt")
    printDebug(t)
    if t.value == tokens.T_RC:
        printDebug("True Stmt for RightCurly")
        return True
    #next_token()
    if t.value == tokens.T_If:
        printDebug("If found from Stmt")
        if next_token() and ifStmt():
            if t.value == tokens.T_RC:
                printDebug("RightCurly found after ifStmt")
                return True
            else:
                printDebug("stmt from ifStmt")
                return stmt()
    
    elif t.value == tokens.T_While:
        printDebug("While found from Stmt")
        if next_token() and whileStmt():
            if t.value == tokens.T_RC:
                printDebug("RightCurly found after whileStmt")
                return True
            else:
                printDebug("stmt from whileStmt")
                return stmt()
    
    elif t.value == tokens.T_For:
        printDebug("For found from Stmt")
        if next_token() and forStmt():
            if t.value == tokens.T_RC:
                printDebug("RightCurly found after forStmt")
                return True
            else:
                printDebug("stmt from forStmt")
                return stmt()
    
    elif t.value == tokens.T_Break:
        printDebug("Break found from Stmt")
        return  next_token() and breakStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_Return:
        printDebug("Return found from Stmt")
        return  next_token() and returnStmt() # and next_token() and stmt()
    
    elif t.value == tokens.T_Print: # and next_token() and t.value == tokens.T_LP:
        printDebug("printDebug found from Stmt")
        return  next_token() and printStmt() and next_token() and stmt()
    
    elif t.value == tokens.T_LC:
        return stmtBlock()
    
    elif t.value == tokens.T_SemiColon:
        printDebug("Semicolon found from stmt")
        return True
    
    elif initExprTree() and expr() and t.value == tokens.T_SemiColon: #need to work:  prev work expr() semi nexttok stmt
        printDebug("Expr and Semicolon found from stmt " + str(t.value))
        return True
    
    else:
        handleError(t)
        return False

def ifStmt():
    printDebug("-----ifStmt")

    prevPar = parent
    node_id = find_node_id(t, "IfStmt")
    astree.create_node( "   " + "$" + "IfStmt:", node_id, parent= prevPar)
    update_parent(node_id)

    if t.value == tokens.T_LP:
        set_prefix("(test) ")
        ifParam = next_token() and initExprTree() and expr() and t.value == tokens.T_RP
        if not ifParam:
            printDebug("error from if ")
            handleError(t)
            return False
        
        clear_prefix()
        printDebug("inside ifParam true" + t.value)
        
        set_prefix("(then) ")
        if next_token() and not stmt():
            printDebug("false from ifStmt")
            handleError(t)
            return False
        clear_prefix()
        #if(t!=None and t.value != tokens.T_Else):
        if t.value == tokens.T_SemiColon:
            next_token()
        
        if t != None and t.value == tokens.T_Else:
            set_prefix("(else) ")
            printDebug("else found")
            next_token()
            if not stmt():
                printDebug("False from if.. else..")
                handleError(t)
                return False
            else:
                printDebug("true for if with else..")
                return True and clear_prefix() and update_parent(prevPar)
        else:
            printDebug("true for if----------------------")
            return True and clear_prefix() and update_parent(prevPar)
    else:
        handleError(t)
        return False


def whileStmt():
    printDebug("------whileStmt")

    prevPar = parent
    node_id = find_node_id(t, "WhileStmt")
    astree.create_node( "   " + "$" + "WhileStmt:", node_id, parent= prevPar)
    update_parent(node_id)
    set_prefix("(test) ")
    
    if t.value == tokens.T_LP:
        whileParam = next_token() and initExprTree() and expr() and t.value == tokens.T_RP
        if not whileParam:
            printDebug("error from whileStmt")
            handleError(t)
            return False
        if next_token() and not stmt():
            printDebug("returnning false from whileStmt")
            handleError(t)
            return False
        printDebug("true for while----------------------")
        return True and clear_prefix() and update_parent(prevPar)
    else:
        handleError(t)
        return False 

def forStmt():
    printDebug("------forStmt")

    prevPar = parent
    node_id = find_node_id(t, "ForStmt")
    astree.create_node( "   " + "$" + "ForStmt:", node_id, parent= prevPar)
    update_parent(node_id)
    

    if t.value == tokens.T_LP:
        printDebug("LeftParen found forStmt")
        set_prefix("(init) ")
        #1 for null init
        if next_token() and t.value == tokens.T_SemiColon:
            printDebug("First expr not present inside forStmt")
            astree.create_node( "   " + "$" + prefix + "Empty:", find_node_id(t, "Empty"), parent= node_id)
            pass
        #1 for init
        elif initExprTree() and not expr() or t.value != tokens.T_SemiColon:
            printDebug("false for wrong first expr part inside forStmt")
            handleError(t)
            return False
        clear_prefix()

        set_prefix("(test) ")
        #2 for cond test
        printDebug("inside forStmt token -> " + str(t))
        next_token()
        if initExprTree() and not expr() or not t.value == tokens.T_SemiColon:
            printDebug("False for wrong second part inside forStmt")
            handleError(t)
            return False
        clear_prefix()

        #3 for update step
        set_prefix("(step) ")
        next_token()
        printDebug("start forStmt last part -> " + str(t))
        if t.value == tokens.T_RP:
            printDebug("No third part inside forStmt")
            astree.create_node( "   " + "$" + prefix + "Empty:", find_node_id(t, "Empty"), parent= node_id)
            return next_token() and stmt() and clear_prefix() and update_parent(prevPar)
        elif initExprTree() and expr() and t.value == tokens.T_RP:
            return next_token() and stmt() and clear_prefix() and update_parent(prevPar)
    else:
        handleError(t)
        return False

def breakStmt():
    printDebug("------breakStmt")
    if t.value == tokens.T_SemiColon:
        printDebug("True from breakStmt" + str(t))

        prevPar = parent
        astree.create_node( "  " + str(t.lineno) + "$" + prefix + "BreakStmt:", find_node_id(t, "BreakStmt"), parent= prevPar)

        return True and update_parent(prevPar)
    else:
        handleError(t)
        return False

def returnStmt():
    printDebug("------returnStmt")
    prevPar = parent
    node_id = find_node_id(t, "ReturnStmt")
    node_label = "  " + str(t.lineno) + "$" + "ReturnStmt:"
    astree.create_node( node_label, node_id, parent= prevPar)

    if t.value == tokens.T_SemiColon:
        printDebug("return done without expr" + str(t))
        astree.create_node( "   " + "$" + "Empty:", find_node_id(t, "Empty"), parent= node_id)
        return True and update_parent(prevPar)
    elif initExprTree() and expr() and t.value == tokens.T_SemiColon and next_token(): # next_token should be removed?
        printDebug("return done with expr" + str(t))
        return True and update_parent(prevPar)
    else:
        handleError(t)
        return False
        
def printStmt():
    printDebug("------printStmt")
    prevPar = parent
    node_id = find_node_id(t, "PrintStmt")
    node_label = "   " + "$" + "PrintStmt:"
    astree.create_node( node_label, node_id, parent= prevPar)
    set_prefix("(args) ")
    if t.value == tokens.T_LP:
        while True and update_parent(node_id):
            printDebug("enter printDebug loop--")
            next_token()        
            if initExprTree() and not expr():
                printDebug("false from printStmt")
                handleError(t)
                return False
            if t.value == tokens.T_Comma:
                printDebug("Comma inside printStmt")
                update_parent(prevPar)
                continue
            elif t.value == tokens.T_RP:
                printDebug("RightParen found in printStmt")
                next_token()
                if t != None and t.value == tokens.T_SemiColon:
                    printDebug("semicolon after printDebug")
                    return True and clear_prefix() and update_parent(prevPar)
                else:
                    handleError(t)
                    return False
    else:
        handleError(t)
        return False

exprTreeRoot = ""
lastTreeRoot = ""
currentTreeRoot = ""
prevOperator = ""
assignTreeRoot = ""
exprTree = Tree()

def initExprTree():
    global exprTree
    exprTree = Tree()
    global exprTreeRoot
    exprTreeRoot = ""
    global lastTreeRoot
    lastTreeRoot = ""
    global prevOperator
    prevOperator = ""
    global currentTreeRoot
    currentTreeRoot = ""
    global assignTreeRoot
    assignTreeRoot = ""
    return True

unary = False
def expr():
    printDebug("------expr " + str(t))
    global exprTreeRoot
    global lastTreeRoot
    global assignTreeRoot
    global exprTree
    global prevOperator
    global currentTreeRoot
    prevPar = parent
    global unary

    if t.value == tokens.T_Minus:
        astree.create_node("  " + str(t.lineno) + "$" + prefix + "ArithmeticExpr:", find_node_id(t, "ArithmeticExpr"), parent=prevPar)
        astree.create_node("  " + str(t.lineno) + "$Operator: " + str(t.value), find_node_id(t, "Operator"), parent=find_node_id(t, "ArithmeticExpr"))
        update_parent(prevPar)
        unary = True
        assignTreeRoot = find_node_id(t, "ArithmeticExpr")
        return next_token() and expr()
    
    elif t.value == tokens.T_LP:
        printDebug("LeftParen found from expr")
        if next_token() and expr() and t.value == tokens.T_RP:
            next_token()
            if t.value in tokens.op_list:
                printDebug("op_list found inside LeftParen expr")
                return next_token() and expr()
            else:
                printDebug("true from expr LeftParen cond")
                return True

    elif t.value == tokens.T_Not:
        astree.create_node("  " + str(t.lineno) + "$" + prefix + "LogicalExpr:", find_node_id(t, "LogicalExpr"), parent=prevPar)
        astree.create_node("  " + str(t.lineno) + "$Operator: " + str(t.value), find_node_id(t, "Operator"), parent=find_node_id(t, "LogicalExpr"))
        update_parent(prevPar)
        unary = True
        assignTreeRoot = find_node_id(t, "LogicalExpr")
        return next_token() and expr()

    elif t.type == tokens.T_Identifier:
        ident = t.value
        next_token()

        if(t.value == tokens.T_Equal):
            exprType = "AssignExpr"
            astree.create_node("  " + str(t.lineno) + "$" + prefix + exprType + ":", find_node_id(t, exprType), parent=prevPar)
            clear_prefix()
            assignTreeRoot = find_node_id(t, exprType)
            astree.create_node("  " + str(t.lineno) + "$" + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=assignTreeRoot)
            astree.create_node("  " + str(t.lineno) + "$" + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
            astree.create_node("  " + str(t.lineno) + "$" + "Operator" + ": " + str(t.value), find_node_id(t, "Operator"), parent=assignTreeRoot)
        elif t.value in tokens.arithmatic_op:
            exprType = "ArithmeticExpr"
        elif t.value in tokens.relational_op:
            exprType = "RelationalExpr"
        elif t.value in tokens.equality_op:
            exprType = "EqualityExpr"
        elif t.value in tokens.logical_op:
            exprType = "LogicalExpr"
        
        if assignTreeRoot == "":
            assignTreeRoot = prevPar

        if t.value == tokens.T_LP:
            if assignTreeRoot == "":
                astree.create_node("  " + str(t.lineno) + "$" + prefix + "Call:", find_node_id(t, "Call"), parent= prevPar)
                astree.create_node("  " + str(t.lineno) + "$" + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "Call"))
            else:
                astree.create_node("  " + str(t.lineno) + "$" + prefix + "Call:", find_node_id(t, "Call"), parent= assignTreeRoot)
                astree.create_node("  " + str(t.lineno) + "$" + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "Call"))
           
            update_parent(find_node_id(t, "Call"))
            next_token()
            return actuals() and update_parent(prevPar)

        elif (t.value == tokens.T_Equal) or (t.value in tokens.op_list):

            if t.value in tokens.op_list:
                currOperator = str(t.value)
                if prevOperator == "":
                    exprTreeRoot = find_node_id(t, exprType)
                    exprTree.create_node("  " + str(t.lineno) + "$" + exprType + ":", exprTreeRoot)
                    exprTree.create_node("  " + str(t.lineno) + "$" + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=exprTreeRoot)
                    exprTree.create_node("  " + str(t.lineno) + "$" + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                    exprTree.create_node("  " + str(t.lineno) + "$" + "Operator" + ": " + currOperator, find_node_id(t, "Operator"), parent=exprTreeRoot)
                    prevOperator = currOperator
                    lastTreeRoot = exprTreeRoot

                elif tokens.precedence_list[prevOperator] >= tokens.precedence_list[currOperator]:

                    if currentTreeRoot != "":
                        exprTree.create_node("  " + str(t.lineno) + "$FieldAccess:", find_node_id(t, "FieldAccess"), parent=currentTreeRoot)
                        exprTree.create_node("  " + str(t.lineno) + "$Identifier: " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                        currentTreeRoot = ""
                    
                    else:
                        exprTree.create_node("  " + str(t.lineno) + "$FieldAccess:", find_node_id(t, "FieldAccess"), parent=exprTreeRoot)
                        exprTree.create_node("  " + str(t.lineno) + "$Identifier: " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                    
                    tempTree=Tree()
                    tempTreeRoot = find_node_id(t, exprType)
                    tempTree.create_node("  " + str(t.lineno) + "$" + exprType + ":", tempTreeRoot)
                    tempTree.paste(tempTreeRoot, exprTree)
                    tempTree.create_node("  " + str(t.lineno) + "$Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                    exprTree = tempTree
                    exprTreeRoot = tempTreeRoot
                    prevOperator = currOperator
                    lastTreeRoot = tempTreeRoot

                elif tokens.precedence_list[prevOperator] < tokens.precedence_list[currOperator]:
                    tempTree=Tree()
                    tempTreeRoot = find_node_id(t, exprType)
                    tempTree.create_node("  " + str(t.lineno) + "$" + exprType + ":", tempTreeRoot)
                    tempTree.create_node("  " + str(t.lineno) + "$FieldAccess:", find_node_id(t, "FieldAccess"), parent=tempTreeRoot)
                    tempTree.create_node("  " + str(t.lineno) + "$Identifier: " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                    tempTree.create_node("  " + str(t.lineno) + "$Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                    exprTree.paste(exprTreeRoot, tempTree)
                    prevOperator = currOperator
                    lastTreeRoot = tempTreeRoot
                    currentTreeRoot = tempTreeRoot
                
            next_token()
            return expr()
        else:
            if exprTree:
                exprTree.create_node("  " + str(t.lineno) + "$" + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=lastTreeRoot)
                exprTree.create_node("  " + str(t.lineno) + "$" + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
                label = exprTree.__getitem__(exprTree.root).tag
                label = label.split("$")[0] + "$" + prefix + label.split("$")[1]
                exprTree.update_node(exprTree.root, label)
                astree.paste(assignTreeRoot, exprTree)
                initExprTree()
            else:
                if unary == False:
                    astree.create_node("  " + str(t.lineno) + "$" + prefix + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=assignTreeRoot)
                else:
                    astree.create_node("  " + str(t.lineno) + "$" + "FieldAccess" + ":", find_node_id(t, "FieldAccess"), parent=assignTreeRoot)
                unary = False
                astree.create_node("  " + str(t.lineno) + "$" + "Identifier" + ": " + ident, find_node_id(t, "Identifier"), parent=find_node_id(t, "FieldAccess"))
            return True and update_parent(prevPar)
    
    elif t.type in tokens.const_list:
        
        constantVal = str(t.value)
        # done for doublecontants only hex and int needed to add
        if t.type == tokens.T_DoubleConstant:
            if(constantVal[-2:] == '.0'):
                constantVal = constantVal[:-2]

        # need update for constant without args
        constant = str(t.type).split("_")[1]

        """node_id = find_node_id(t, constant)
        node_label = "  " + str(t.lineno) + "." + "(args) " + constant + ": " + constantVal
        astree.create_node( node_label, node_id, parent=parent)"""
        
        next_token()
        
        if t.value in tokens.arithmatic_op:
            exprType = "ArithmeticExpr"
        elif t.value in tokens.relational_op:
            exprType = "RelationalExpr"
        elif t.value in tokens.equality_op:
            exprType = "EqualityExpr"
        elif t.value in tokens.logical_op:
            exprType = "LogicalExpr"
        if assignTreeRoot == "":
            assignTreeRoot = prevPar

        if (t.value in tokens.op_list):
            currOperator = str(t.value)
            if prevOperator == "":
                exprTreeRoot = find_node_id(t, exprType)
                exprTree.create_node("  " + str(t.lineno) + "$" + exprType + ":", exprTreeRoot)
                exprTree.create_node("  " + str(t.lineno) + "$" + constant + ": " +  constantVal, find_node_id(t, constant), parent=exprTreeRoot)
                exprTree.create_node("  " + str(t.lineno) + "$" + "Operator" + ": " + currOperator, find_node_id(t, "Operator"), parent=exprTreeRoot)
                prevOperator = currOperator
                lastTreeRoot = exprTreeRoot

            elif tokens.precedence_list[prevOperator] >= tokens.precedence_list[currOperator]:

                if currentTreeRoot != "":
                    exprTree.create_node("  " + str(t.lineno) + "$" + constant + ": " +  constantVal, find_node_id(t, constant), parent=currentTreeRoot)
                    currentTreeRoot = ""
                
                else:
                    exprTree.create_node("  " + str(t.lineno) + "$" + constant + ": " +  constantVal, find_node_id(t, constant), parent=exprTreeRoot)
                
                tempTree=Tree()
                tempTreeRoot = find_node_id(t, exprType)
                tempTree.create_node("  " + str(t.lineno) + "$" + exprType + ":", tempTreeRoot)
                tempTree.paste(tempTreeRoot, exprTree)
                tempTree.create_node("  " + str(t.lineno) + "$Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                exprTree = tempTree
                exprTreeRoot = tempTreeRoot
                prevOperator = currOperator
                lastTreeRoot = tempTreeRoot

            elif tokens.precedence_list[prevOperator] < tokens.precedence_list[currOperator]:
                tempTree=Tree()
                tempTreeRoot = find_node_id(t, exprType)
                tempTree.create_node("  " + str(t.lineno) + "$" + exprType + ":", tempTreeRoot)
                tempTree.create_node("  " + str(t.lineno) + "$" + constant + ": " +  constantVal, find_node_id(t, constant), parent=tempTreeRoot)
                tempTree.create_node("  " + str(t.lineno) + "$Operator: " + currOperator, find_node_id(t, "Operator"), parent=tempTreeRoot)            
                exprTree.paste(exprTreeRoot, tempTree)
                prevOperator = currOperator
                lastTreeRoot = tempTreeRoot
                currentTreeRoot = tempTreeRoot

            return next_token() and expr()
        elif t.value == ".":
            next_token()
            handleError(t)
            return False
        else:
            printDebug("ture from expr Constant" + str(t.value))

            if exprTree:
                exprTree.create_node("  " + str(t.lineno) + "$" + constant + ": " +  constantVal, find_node_id(t, constant), parent=lastTreeRoot)
                label = exprTree.__getitem__(exprTree.root).tag
                label = label.split("$")[0] + "$" + prefix + label.split("$")[1]
                exprTree.update_node(exprTree.root, label)
                astree.paste(assignTreeRoot, exprTree)
                initExprTree()
            else:
                if unary == False:
                    astree.create_node("  " + str(t.lineno) + "$" + prefix + constant + ": " +  constantVal, find_node_id(t, constant), parent=assignTreeRoot)
                else:
                    astree.create_node("  " + str(t.lineno) + "$" + constant + ": " +  constantVal, find_node_id(t, constant), parent=assignTreeRoot)
                unary = False
            return True and update_parent(prevPar)
    
    elif t.value == tokens.T_ReadInteger or t.value == tokens.T_ReadLine:
        if assignTreeRoot == "":
            assignTreeRoot = prevPar
        printDebug("ReadInteger or ReadLine found")
        exprType = str(t.value) + "Expr"
        astree.create_node("  " + str(t.lineno) + "$" + exprType + ":", find_node_id(t, exprType), parent=assignTreeRoot)

        if (next_token() and t.value == tokens.T_LP) and (next_token() and t.value == tokens.T_RP):
            next_token()
            return True
        else:
            handleError(t)
            return False

    else:
        printDebug("exit expr false " + str(t.value))
        handleError(t)
        return False


def actuals():
    printDebug("------actuals")
    set_prefix("(actuals) ")
    if t.value == tokens.T_RP:
        return True

    while True:
        printDebug("insilde actual loop " + str(t))    
        if initExprTree() and not expr():
            handleError(t)
            return False
        
        if t.value == tokens.T_Comma and (next_token() and t.value != tokens.T_RP):
            continue
        if t.value == tokens.T_RP:
            next_token()
            return clear_prefix() and True
        else:
            handleError(t)
            return False


def getAstree():
    if program_start():
        return astree

#start program
def main():
    printDebug(program_start())
    if errorFound == False:
        print()
        astree.show(key = False, line_type = 'ascii-sp')

if __name__ == "__main__":
    main()