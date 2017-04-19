
# parsetab.py
# This file is automatically generated. Do not edit.
_tabversion = '3.10'

_lr_method = 'LALR'

_lr_signature = 'INTEGER STRING_LITERAL COLON NAME COMMA LCURL RCURL LBRAC RBRAC LPAREN RPAREN DOT SEMICOLON BOOLEAN EXTENDS IMPORT REF\n        start : doc post_parsing\n        \n        doc : dict_def\n        \n        doc : global_stmts SEMICOLON dict_def\n        \n        global_stmts : global_stmt SEMICOLON\n                     | global_stmt SEMICOLON global_stmts\n        \n        global_stmt : import_stmt\n        \n        import_stmt : IMPORT dotted_name\n        \n        dotted_name : NAME\n                    | NAME DOT dotted_name\n        \n        dict_def : empty_dict_def\n                 | non_empty_dict_def\n        \n        empty_dict_def : LCURL RCURL\n        \n        non_empty_dict_def : LCURL dict_entries RCURL\n        \n        dict_entries : dict_entry\n                     | dict_entry COMMA\n                     | dict_entry COMMA dict_entries\n        \n        dict_entry : dict_key COLON dict_val\n        \n        dict_key : STRING_LITERAL\n                 | BOOLEAN\n                 | number\n                 | ref\n        \n        ref : REF LBRAC dict_key RBRAC\n        \n        dict_val : STRING_LITERAL\n                 | BOOLEAN\n                 | number\n                 | ref\n                 | dict_def\n                 | list_def\n        \n        list_def : LBRAC RBRAC\n                 | LBRAC list_entries RBRAC\n        \n        list_entries : dict_val\n                     | dict_val COMMA\n                     | dict_val COMMA list_entries\n        \n        number : INTEGER\n        \n        number : INTEGER DOT INTEGER\n        \n        post_parsing :\n        '
    
_lr_action_items = {'LCURL':([0,12,30,42,51,],[8,8,8,8,8,]),'IMPORT':([0,13,],[10,10,]),'$end':([1,2,3,5,6,11,14,26,28,],[0,-36,-2,-10,-11,-1,-12,-3,-13,]),'SEMICOLON':([4,7,9,13,24,25,27,45,],[12,13,-6,-4,-7,-8,-5,-9,]),'COMMA':([5,6,14,16,22,28,35,36,37,38,39,40,41,43,46,48,49,50,],[-10,-11,-12,29,-34,-13,-17,-23,-24,-25,-26,-27,-28,-35,-29,51,-22,-30,]),'RCURL':([5,6,8,14,15,16,22,28,29,34,35,36,37,38,39,40,41,43,46,49,50,],[-10,-11,14,-12,28,-14,-34,-13,-15,-16,-17,-23,-24,-25,-26,-27,-28,-35,-29,-22,-30,]),'RBRAC':([5,6,14,18,19,20,21,22,28,36,37,38,39,40,41,42,43,44,46,47,48,49,50,51,52,],[-10,-11,-12,-18,-19,-20,-21,-34,-13,-23,-24,-25,-26,-27,-28,46,-35,49,-29,50,-31,-22,-30,-32,-33,]),'STRING_LITERAL':([8,29,30,32,42,51,],[18,18,36,18,36,36,]),'BOOLEAN':([8,29,30,32,42,51,],[19,19,37,19,37,37,]),'INTEGER':([8,29,30,31,32,42,51,],[22,22,22,43,22,22,22,]),'REF':([8,29,30,32,42,51,],[23,23,23,23,23,23,]),'NAME':([10,33,],[25,25,]),'COLON':([17,18,19,20,21,22,43,49,],[30,-18,-19,-20,-21,-34,-35,-22,]),'DOT':([22,25,],[31,33,]),'LBRAC':([23,30,42,51,],[32,42,42,42,]),}

_lr_action = {}
for _k, _v in _lr_action_items.items():
   for _x,_y in zip(_v[0],_v[1]):
      if not _x in _lr_action:  _lr_action[_x] = {}
      _lr_action[_x][_k] = _y
del _lr_action_items

_lr_goto_items = {'start':([0,],[1,]),'doc':([0,],[2,]),'dict_def':([0,12,30,42,51,],[3,26,40,40,40,]),'global_stmts':([0,13,],[4,27,]),'empty_dict_def':([0,12,30,42,51,],[5,5,5,5,5,]),'non_empty_dict_def':([0,12,30,42,51,],[6,6,6,6,6,]),'global_stmt':([0,13,],[7,7,]),'import_stmt':([0,13,],[9,9,]),'post_parsing':([2,],[11,]),'dict_entries':([8,29,],[15,34,]),'dict_entry':([8,29,],[16,16,]),'dict_key':([8,29,32,],[17,17,44,]),'number':([8,29,30,32,42,51,],[20,20,38,20,38,38,]),'ref':([8,29,30,32,42,51,],[21,21,39,21,39,39,]),'dotted_name':([10,33,],[24,45,]),'dict_val':([30,42,51,],[35,48,48,]),'list_def':([30,42,51,],[41,41,41,]),'list_entries':([42,51,],[47,52,]),}

_lr_goto = {}
for _k, _v in _lr_goto_items.items():
   for _x, _y in zip(_v[0], _v[1]):
       if not _x in _lr_goto: _lr_goto[_x] = {}
       _lr_goto[_x][_k] = _y
del _lr_goto_items
_lr_productions = [
  ("S' -> start","S'",1,None,None,None),
  ('start -> doc post_parsing','start',2,'p_start','yacc.py',47),
  ('doc -> dict_def','doc',1,'p_dict_doc','yacc.py',52),
  ('doc -> global_stmts SEMICOLON dict_def','doc',3,'p_doc_with_imports','yacc.py',58),
  ('global_stmts -> global_stmt SEMICOLON','global_stmts',2,'p_global_stmts','yacc.py',64),
  ('global_stmts -> global_stmt SEMICOLON global_stmts','global_stmts',3,'p_global_stmts','yacc.py',65),
  ('global_stmt -> import_stmt','global_stmt',1,'p_global_stmt','yacc.py',70),
  ('import_stmt -> IMPORT dotted_name','import_stmt',2,'p_import_stmt','yacc.py',75),
  ('dotted_name -> NAME','dotted_name',1,'p_dotted_name','yacc.py',80),
  ('dotted_name -> NAME DOT dotted_name','dotted_name',3,'p_dotted_name','yacc.py',81),
  ('dict_def -> empty_dict_def','dict_def',1,'p_dict_def','yacc.py',86),
  ('dict_def -> non_empty_dict_def','dict_def',1,'p_dict_def','yacc.py',87),
  ('empty_dict_def -> LCURL RCURL','empty_dict_def',2,'p_empty_dict_def','yacc.py',93),
  ('non_empty_dict_def -> LCURL dict_entries RCURL','non_empty_dict_def',3,'p_non_empty_dict_def','yacc.py',99),
  ('dict_entries -> dict_entry','dict_entries',1,'p_dict_entries','yacc.py',106),
  ('dict_entries -> dict_entry COMMA','dict_entries',2,'p_dict_entries','yacc.py',107),
  ('dict_entries -> dict_entry COMMA dict_entries','dict_entries',3,'p_dict_entries','yacc.py',108),
  ('dict_entry -> dict_key COLON dict_val','dict_entry',3,'p_dict_entry','yacc.py',114),
  ('dict_key -> STRING_LITERAL','dict_key',1,'p_dict_key','yacc.py',120),
  ('dict_key -> BOOLEAN','dict_key',1,'p_dict_key','yacc.py',121),
  ('dict_key -> number','dict_key',1,'p_dict_key','yacc.py',122),
  ('dict_key -> ref','dict_key',1,'p_dict_key','yacc.py',123),
  ('ref -> REF LBRAC dict_key RBRAC','ref',4,'p_ref','yacc.py',131),
  ('dict_val -> STRING_LITERAL','dict_val',1,'p_dict_val','yacc.py',144),
  ('dict_val -> BOOLEAN','dict_val',1,'p_dict_val','yacc.py',145),
  ('dict_val -> number','dict_val',1,'p_dict_val','yacc.py',146),
  ('dict_val -> ref','dict_val',1,'p_dict_val','yacc.py',147),
  ('dict_val -> dict_def','dict_val',1,'p_dict_val','yacc.py',148),
  ('dict_val -> list_def','dict_val',1,'p_dict_val','yacc.py',149),
  ('list_def -> LBRAC RBRAC','list_def',2,'p_list_def','yacc.py',155),
  ('list_def -> LBRAC list_entries RBRAC','list_def',3,'p_list_def','yacc.py',156),
  ('list_entries -> dict_val','list_entries',1,'p_list_entries','yacc.py',163),
  ('list_entries -> dict_val COMMA','list_entries',2,'p_list_entries','yacc.py',164),
  ('list_entries -> dict_val COMMA list_entries','list_entries',3,'p_list_entries','yacc.py',165),
  ('number -> INTEGER','number',1,'p_integer_number','yacc.py',171),
  ('number -> INTEGER DOT INTEGER','number',3,'p_float_number','yacc.py',177),
  ('post_parsing -> <empty>','post_parsing',0,'p_finish','yacc.py',183),
]
