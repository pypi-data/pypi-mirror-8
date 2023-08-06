// Copyright (c) 2012. Los Alamos National Security, LLC. 

// This material was produced under U.S. Government contract DE-AC52-06NA25396
// for Los Alamos National Laboratory (LANL), which is operated by Los Alamos 
// National Security, LLC for the U.S. Department of Energy. The U.S. Government 
// has rights to use, reproduce, and distribute this software.  

// NEITHER THE GOVERNMENT NOR LOS ALAMOS NATIONAL SECURITY, LLC MAKES ANY WARRANTY, 
// EXPRESS OR IMPLIED, OR ASSUMES ANY LIABILITY FOR THE USE OF THIS SOFTWARE.  
// If software is modified to produce derivative works, such modified software should
// be clearly marked, so as not to confuse it with the version available from LANL.

// Additionally, this library is free software; you can redistribute it and/or modify
// it under the terms of the GNU Lesser General Public License v 2.1 as published by the 
// Free Software Foundation. Accordingly, this library is distributed in the hope that 
// it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of 
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See LICENSE.txt for more details.

const char file1cfg[] = "CONFIG_DEBUG_LOG  TestData/file1.log\nOne  1\nOne.Two  1.2\nZero 0\nTrue true\nFalse false\nKeyWithSpace Foo Bar\n";
const char include1cfg[] = "CONFIG_DEBUG_LOG  include.log\ninclude TestData/include2.cfg\nKey1 inc1\nKey4 inc1\ninclude TestData/include3.cfg\n";
const char include2cfg[] = "Key2 inc2\nKey4 inc2";
const char include3cfg[] = "Key3 inc3\nKey4 inc3\ninclude TestData/include4.cfg";
const char include4cfg[] = "Key4 inc4\n";
const char listcfg[] = "CONFIG_DEBUG_LOG  list.log\n# regular key\nTESTLIST  1;2;3;4\nTESTSPSTRLIST ONE TWO THREE FOUR\nTESTBADLIST ONE;TWO;THREE;FOUR;\nTESTEMPTYLIST";
const char multikeyscfg[] = "CONFIG_DEBUG_LOG  multikeys.log\nKey first\nKey second\nKey last";
const char pathcfg[] = "CONFIG_DEBUG_LOG  path.log\n$PATH /path/to/some/file\nFILE $PATH/file.txt";
const char setscfg[] = "CONFIG_DEBUG_LOG  TestData/sets.log\n\n# test with good sets\nset TEST1 A active\n{\nOne  1\nOne.Two  1.2\nKeyWithSpace Foo Bar\n}\n\nset TEST1 B inactive\n{\nZero 0\nTrue true\nFalse false\n}\n\n$var1 Sub1\nset Test2 C active\n{\nKey1 $var1\nKey2 Value$var1.ext\n}\n\nset Test2 D active\n   {\nKey3 Value${var1}Value\n  }\n\n# test with empty sets\nset test3 A active\n\nset test3 B active\n{\n}\n\n#test with bad sets\nset Test4 A     # no active|inactive\n{\nJUNK junk\n}\n\nset Test5 A active {   # { not on separate line\nKey4 Key4\n}\nset Test6 A active\n{}             # treated as a comment\n\nset Test7 A active\n{ }            # subsequent keys are erroneously in this set\n\nKey5 Key5";
const char variablescfg[] = "CONFIG_DEBUG_LOG  variables.log\n# regular key\nKey1  Key1\n\n# define three variables\n$var1 Sub1\n$var2 Sub1\n$var3 Sub1\n$var_with_underscore Sub1\n\n# regular substitution\nKey2  $var1\n\n# key doesn't change if variable changed after key defined\nKey3  $var2\n$var2 Sub2\n\n# key set to last value variable is set to\nKey4 $var3\n$var3 Sub3\nKey4 $var3\n\n# key set to a variable not yet seen\nKeyWithUnknownVar $novar\n\n# embedded variables\nKey5 Value$var1\nKey6 Value$var1.ext\nKey7 Value${var1}Value\nKey8 Value$$notavar\n# invalid\n# Key9 Value$$$var1\n\n# test underscores\nKey10 $var_with_underscore\nKey11 ${var_with_underscore}\n";
const char commentscfg[] = "# this is a config file with some comments\n# define a key\n# Key inside\nKey outside\n# Key inside";
