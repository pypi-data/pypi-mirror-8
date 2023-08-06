#-------------------------------------------------------------------------------
# fsm.py
#
# Finite State Machine and Value Binding#
#
# Copyright (C) 2013, Shinya Takamaeda-Yamazaki
# License: Apache 2.0
#-------------------------------------------------------------------------------
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))) )
import pyverilog.vparser.ast as vast

class Bind(object):
    def __init__(self, dst, value, cond=None):
        self.dst = dst
        self.value = value
        self.cond = cond
    def __repr__(self):
        ret = []
        ret.append(str(self.dst))
        ret.append('<-')
        ret.append(str(self.value))
        if self.cond is not None:
            ret.append(' if ')
            ret.append(str(self.cond))
        return ''.join(ret)

class FsmNode(object):
    def __init__(self, src, dst, cond, elsedst):
        self.src = src
        self.dst = dst
        self.cond = cond
        self.elsedst = elsedst
    def __repr__(self):
        ret = []
        ret.append('SRC:%d' % self.src)
        ret.append(' DST:%d' % self.dst)
        if self.cond:
            ret.append(' COND:%s' % str(self.cond))
        if self.elsedst:
            ret.append(' ELSE:%s' % str(self.elsedst))
        return ''.join(ret)
    def __eq__(self, other):
        if not isinstance(other, FsmNode): return False
        if self.src != other.src: return False
        if self.dst != other.dst: return False
        if self.cond != other.cond: return False
        if self.elsedst != other.elsedst: return False
        return True
    def __nq__(self, other):
        return not self.__eq__(other)
    def __hash__(self):
        return hash( (self.src, self.dst, self.cond, self.elsedst) )

class Fsm(object):
    def __init__(self):
        self.dict = {}
        self.count = 0
        self.bind = {}
        self.object_bind = {}
        self.constant = {}
        self.loop = {}
        self.loop_bind = {}

    def set(self, src=None, dst=None, cond=None, elsedst=None):
        if src is None:
            src = self.getCount()
        if dst is None:
            dst = src + 1
        self.add(src, dst, cond, elsedst)

    def add(self, src, dst, cond, elsedst):
        if src not in self.dict:
            self.dict[src] = []
        for n in self.dict[src]:
            if n.cond == cond or n.cond is None:
                n.cond = cond
                n.dst = dst
                n.elsedst = elsedst
                return
        self.dict[src].append( FsmNode(src, dst, cond, elsedst) )

    def get(self, src):
        if src not in self.dict: return ()
        return tuple(self.dict[src])

    def getCount(self):
        return self.count

    def incCount(self):
        self.count += 1

    def setBind(self, dst, value, st=None, cond=None):
        state = self.getCount() if st is None else st
        if state not in self.bind:
            self.bind[state] = []
        self.bind[state].append( Bind(dst, value, cond=cond) )
        if isinstance(value, vast.Constant):
            self.setConstant(dst, value)
        else:
            self.unsetConstant(dst)

    def setObjectBind(self, dst, value, st=None, cond=None):
        state = self.getCount() if st is None else st
        if state not in self.object_bind:
            self.object_bind[state] = []
        self.object_bind[state].append( Bind(dst, value, cond=cond) )

    def setConstant(self, dst, value):
        self.constant[dst] = value
        
    def unsetConstant(self, dst):
        if dst not in self.constant:
            return
        self.constant[dst] = None

    def getConstant(self, dst):
        if dst not in self.constant:
            return None
        return self.constant[dst]

    def setLoop(self, begin, end, iter_node=None, step_node=None):
        self.loop[begin] = (end, iter_node, step_node)

    def getCandidateLoops(self, pos):
        candidates = [ (b, e) for b, (e, inode, unode) in self.loop.items() if b <= pos and pos <= e ]
        return candidates

    def getLoops(self):
        return self.loop
        
    def __repr__(self):
        ret = []
        ret.append('Count:%d' % self.count)
        ret.append(' Fsm:')
        ret.append(str(self.dict))
        ret.append(' Bind:')
        ret.append(str(self.bind))
        ret.append(' Loop:')
        ret.append(str(self.loop))
        return ''.join(ret)

    #---------------------------------------------------------------------------
    # dataflow analysis methods
    #---------------------------------------------------------------------------
    def getSources(self, n):
        if n is None: return []
        if isinstance(n, vast.Constant): return []
        if isinstance(n, vast.Operator):
            return self.getSources(n.left) + self.getSources(n.right)
        return [n]

    def getBindmap(self):
        # bind map for each destination
        bindmap = {}
        for state, bindlist in self.bind.items():
            for bind in bindlist:
                if bind.dst is None:
                    continue
                if bind.dst not in bindmap:
                    bindmap[bind.dst] = []
                bindmap[bind.dst].append( (state, bind) )
        return bindmap

    def getReadSet(self):
        # read set by CoRAM method
        read_set = {}
        for state, bindlist in self.bind.items():
            candidateloops = sorted(self.getCandidateLoops(state), key=lambda x:len(x))
            if len(candidateloops) == 0: continue
            innermostloop = candidateloops[0]
            for bind in bindlist:
                if isinstance(bind.value, vast.SystemCall):
                    if innermostloop not in read_set:
                        read_set[innermostloop] = set([])
                    for x in bind.value.args[1:]:
                        read_set[innermostloop] |= set( self.getSources(x) )
        return read_set

    def getWriteSet(self):
        # write set of CoRAM method
        write_set = {}
        for state, bindlist in self.bind.items():
            candidateloops = sorted(self.getCandidateLoops(state), key=lambda x:len(x))
            if len(candidateloops) == 0: continue
            innermostloop = candidateloops[0]
            for bind in bindlist:
                if (isinstance(bind.value, vast.SystemCall) and
                    (bind.value.syscall == 'coram_channel_read' or
                     bind.value.syscall == 'coram_register_read')):
                    if innermostloop not in write_set:
                        write_set[innermostloop] = set([])
                    write_set[innermostloop].add(bind.value.args[-1])
        return write_set
        
    def analysis(self):
        read_set = self.getReadSet()
        write_set = self.getWriteSet()
        bindmap = self.getBindmap()
        print('read_set', read_set)
        print('write_set', write_set)
        print('bindmap', bindmap)
