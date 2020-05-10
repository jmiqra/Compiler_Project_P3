#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb 17 23:11:31 2020

@author: iqrah
"""
from __future__ import division

import sys
import lex
#import ply.lex as lex

tokens = [

    'T_Identifier',
	'T_IntConstant',
	'T_DoubleConstant',
	'T_BoolConstant',
	'T_StringConstant',
	'Plus',
	'Minus',
	'Multiply',
	'Divide',
	'Modulus',
	'T_GreaterEqual',
	'Greater',
	'T_LessEqual',
	'Less',
	'T_Equal',
	'T_NotEqual',
	'Eq',
	'T_And',
	'T_Or',
	'Not',
	'Semicolon',
	'Comma',
	'Dot',
	'LeftParen',
	'RightParan',
    'LeftCurly',
	'RightCurly',
	'Comment'   
]
reserved = {
	'void' : 'T_Void',
	'int' : 'T_Int',
	'double' : 'T_Double',
	'bool' : 'T_Bool',
	'string' : 'T_String',
	'null' : 'T_Null',
	'for' : 'T_For',
	'while' : 'T_While',
	'if' : 'T_If',
	'else' : 'T_Else',
	'return' : 'T_Return',
	'break' : 'T_Break',
	'Print' : 'T_Print',
	'ReadInteger' : 'T_ReadInteger',
	'ReadLine' : 'T_ReadLine'
}
tokens += list(reserved.values())

operators = {
	'Plus' : '+',
	'Minus' : '-',
	'Multiply' : '*',
	'Divide' : '/',
	'Modulus' : '%',
	'Greater' : '>',
	'Less' : '<',
	'Eq' : '=',
	'Not' : '!',
	'Semicolon' : ';',
	'Comma' : ',',
	'Dot' : '.',
	'LeftParen' : '(',
	'RightParan' : ')',
    'LeftCurly' : '{',
	'RightCurly' : '}'
}

t_ignore = ' \t'
t_Plus = r'\+'
t_Minus = r'\-'
t_Multiply = r'\*'
t_Divide = r'\/'
t_Modulus = r'\%'
t_Greater = r'>'
t_Less = r'<'
t_Eq = r'='
t_Not = r'\!'
t_Semicolon = r';'
t_Comma = r','
t_Dot = r'\.'
t_LeftParen = r'\('
t_RightParan = r'\)'
t_LeftCurly = r'{'
t_RightCurly = r'}'

def t_GreaterEqual(t):
	r'>='
	t.type = 'T_GreaterEqual'
	return t

def t_LessEqual(t):
	r'<='
	t.type = 'T_LessEqual'
	return t

def t_Equal(t):
	r'=='
	t.type = 'T_Equal'
	return t

def t_NotEqual(t):
	r'\!='
	t.type = 'T_NotEqual'
	return t

def t_And(t):
	r'\&\&'
	t.type = 'T_And'
	return t

def t_Or(t):
	r'\|\|'
	t.type = 'T_Or'
	return t

def t_BoolConstant(t):
	r'(true|false)'
	t.type = 'T_BoolConstant'
	return t

def t_Identifier(t):
	r'[a-zA-Z_][a-zA-Z_0-9]*'
	if reserved.get(t.value) != None:
		t.type = reserved.get(t.value)
		return t
	t.type = 'T_Identifier'
	if len(t.value) > 31:
		t_error(t)
		return
	return t

def t_StringConstant(t):
	r'"[^\n|"]*(")?'
	t.type = 'T_StringConstant'
	if ((t.value[-1] != '\"') or (t.value[0] == '\"' and len(t.value) == 1)):
		t_error(t)
		t.lexer.lineno += 1
		return
	return t

def t_DoubleConstant(t): #decimal points done 2.10 and 1200.0 vs 1200
	r'\d+\.\d*([eE]?)[+-]?\d+'
	#t.value = float(t.value)
	t.type = 'T_DoubleConstant'
	return t

def t_IntConstant(t): # solved hex vs int
	#r'\d+'
	r'(0[xX][\da-fA-F]+)|\d+'
	t.type = 'T_IntConstant'
	return t

def t_Comment(t):
	r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)'
	lines = t.value.count('\n')
	t.lexer.lineno += lines
	pass

def t_newline(t):
     r'\n+'
     t.lexer.lineno += len(t.value)

# Compute column.
#     input is the input text string
#     token is a token instance
def find_column(input, token):
	line_start = input.rfind('\n', 0, token.lexpos) + 1
	return (token.lexpos - line_start) + 1

def t_error(t):
	#print("\n*** Error line", t.lineno, ".")
	write_to_file("\n*** Error line " + str(t.lineno) + ".")
	if (t.type == 'T_Identifier'):
		#print("*** Identifier too long: \"", t.value, "\"\n")
		write_to_file("*** Identifier too long: \"" + t.value + "\"\n")
		corrected_value = "(truncated to " + t.value[:31] + ")"
		#print(t.value, "line ", t.lineno, "cols ", find_column(input_str, t), "-", find_column(input_str, t)+len(str(t.value))-1, " is ", t.type, corrected_value)
		write_to_file(t.value + " line " + str(t.lineno) + " cols " + str(find_column(input_str, t)) + "-" + str(find_column(input_str, t)+len(str(t.value))-1) + " is " + t.type + " " + corrected_value)
	elif (t.type == 'T_StringConstant'):
		#print("*** Unterminated string constant: %s" % t.value, "\n")
		write_to_file("*** Unterminated string constant: " + t.value + "\n")
	else:
		#print("*** Unrecognized char: '%s'" % t.value[0], "\n")
		write_to_file("*** Unrecognized char: '%s'"  % str(t.value[0]) + "\n")
	t.lexer.skip(1)

lexer = lex.lex()

input_str = ''
'''
input_str = "120 45 012 0xa23 001 10 0 12.00 12.E+2 12.e+0"
lexer.input(input_str)
'''
#input_file = open("/home/iqrah/Desktop/Spring_02_2020/Compilers/Compiler_Project_Iqrah/samples/number.frag", "r")
input_file = open(str(sys.argv[1]), "r")
if input_file.mode == 'r':
	input_str = input_file.read()

lines = input_str.splitlines()
#print(lines)

lexer.input(input_str)

def get_next_token():
	return lexer.token()


#output_file = open(str(sys.argv[2]), "a+")
#output_file.truncate(0)
def write_to_file(output_str):
	#terminal = sys.stdout
	#sys.stdout = output_file
	print(output_str)
	#sys.stdout = terminal
"""
while True:
	t = lexer.token()
	if not t:
		break
	
	op_type = t.type
	if( operators.get(t.type) != None ):
		op_type = "'" + operators.get(t.type) + "'"
	
	value = ""
	if ( t.type == "T_BoolConstant" or t.type == "T_StringConstant" ):
		value = "(value = " + str(t.value) + ")"
	
	elif ( t.type == "T_IntConstant" ):
		if(t.value[0:2] == '0X' or t.value[0:2] == '0x'):
			int_val = str(int(t.value, 16))
		else:
			int_val = str(int(t.value))
		value = "(value = " + int_val + ")"
	
	elif ( t.type == "T_DoubleConstant" ):
		double_val = str(float(t.value))
		if(double_val[-2:] == '.0'):
			double_val = double_val[:-2]
		value = "(value = " + double_val + ")"
	#print(t)
	#print(t.value, "\t\tline ", t.lineno, "cols ", t.lexpos+1, "-", t.lexpos+len(str(t.value)), " ", t.type)
	#print(t.value, "\t\tline ", t.lineno, "cols ", find_column(input_str, t), "-",  find_column(input_str, t)+len(str(t.value))-1, " is ", op_type, value)
	write_to_file(t.value.ljust(12) + " line " + str(t.lineno) + " cols " + str(find_column(input_str, t)) + "-" + str(find_column(input_str, t)+len(str(t.value))-1) + " is " + op_type + " " + value)

	"""