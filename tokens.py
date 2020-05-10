#tokens with regex types
T_Identifier = "T_Identifier"
T_IntConstant = "T_IntConstant"
T_DoubleConstant = "T_DoubleConstant"
T_BoolConstant = "T_BoolConstant"
T_StringConstant = "T_StringConstant"

#simple tokens
T_Int = "int"
T_Double = "double"
T_Bool = "bool"
T_String = "string"
T_Void = "void"
T_Null = "null"
T_If = "if"
T_Else = "else"
T_While = "while"
T_For = "for"
T_Return = "return"
T_Break = "break"
T_Print = "Print"
T_Plus = "+"
T_Minus = "-"
T_Multiply = "*"
T_Divide = "/"
T_Modulus = "%"
T_Greater = ">"
T_Less = "<"
T_Equal = "="
T_Not = "!"
T_GreaterEqual = ">="
T_LessEqual = "<="
T_EqualEqual = "=="
T_NotEqual = "!="
T_And = "&&"
T_Or = "||"
#T_Dot = "."
T_ReadInteger = "ReadInteger"
T_ReadLine = "ReadLine"
T_SemiColon = ";"
T_Comma = ","
T_LP = "("
T_RP = ")"
T_LC = "{"
T_RC = "}"

type_list = [T_Int, T_Double, T_Bool, T_String]
op_list = [T_GreaterEqual, T_Greater, T_LessEqual, T_Less, T_EqualEqual, 
            T_NotEqual, T_Multiply, T_Divide, T_Modulus, T_Plus, T_Minus, T_And, T_Or]
precedence_list = {"!": 8, "*": 7, "/": 7, "%": 7 , "+": 6, "-": 6, "<":5, "<=": 5, ">": 5, ">=": 5, "==": 4, "!=": 4, "&&": 3, "||": 2, "=": 1}
const_list = [T_IntConstant, T_DoubleConstant, T_BoolConstant, T_StringConstant, T_Null]

relational_op = [T_Less, T_LessEqual, T_Greater, T_GreaterEqual]
equality_op = [T_EqualEqual, T_NotEqual]
logical_op = [T_Not, T_And, T_Or]
arithmatic_op = [T_Multiply, T_Divide, T_Modulus, T_Plus, T_Minus]

boolOP = relational_op + equality_op