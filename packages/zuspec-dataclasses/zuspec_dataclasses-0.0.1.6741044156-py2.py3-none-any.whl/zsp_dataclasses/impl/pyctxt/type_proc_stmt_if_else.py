#****************************************************************************
#* type_proc_stmt_if_else.py
#*
#* Copyright 2022 Matthew Ballance and Contributors
#*
#* Licensed under the Apache License, Version 2.0 (the "License"); you may 
#* not use this file except in compliance with the License.  
#* You may obtain a copy of the License at:
#*
#*   http://www.apache.org/licenses/LICENSE-2.0
#*
#* Unless required by applicable law or agreed to in writing, software 
#* distributed under the License is distributed on an "AS IS" BASIS, 
#* WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.  
#* See the License for the specific language governing permissions and 
#* limitations under the License.
#*
#* Created on:
#*     Author: 
#*
#****************************************************************************
import zsp_dataclasses.impl.context as ctxt_api

class TypeProcStmtIfElse(ctxt_api.TypeProcStmtIfElse):

    def __init__(self,
                 cond,
                 true_s,
                 false_s):
        self._cond = cond
        self._true_s = true_s
        self._false_s = false_s

    def getCond(self):
        return self._cond
    
    def setTrue(self, s):
        self._true_s = s

    def getTrue(self):
        return self._true_s

    def setFalse(self, s):
        self._false_s = s

    def getFalse(self):
        return self._false_s

    def accept(self, v):
        v.visitTypeProcStmtIfElse(self)
