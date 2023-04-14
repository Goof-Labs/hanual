package main

import (
	"errors"
	"sync"
)

type stack struct {
	lock sync.Mutex // you don't have to do this if you don't want thread safety
	s    []*HanualConstant
}

func NewStack() *stack {
	return &stack{sync.Mutex{}, make([]*HanualConstant, 0)}
}

func (s *stack) Push(v *HanualConstant) {
	s.lock.Lock()
	defer s.lock.Unlock()

	s.s = append(s.s, v)
}

func (s *stack) Pop() (*HanualConstant, error) {
	s.lock.Lock()
	defer s.lock.Unlock()

	l := len(s.s)
	if l == 0 {
		return nil, errors.New("Empty Stack")
	}

	res := s.s[l-1]
	s.s = s.s[:l-1]
	return res, nil
}

func run(spec *HanualFileFormat) {
	instructions := make([]HanualInstruction, spec.const_len)

	current := (*spec.instructions).Front()

	for i := 0; i < spec.instructions.Len(); i++ {
		instructions[i] = current.Value.(HanualInstruction)
		current = current.Next()
	}

	var pc uint64 = 0
	var program_stack stack

	for {
		instruction := instructions[pc]

		switch instruction.Raw {
		case NOP:
			pc++
			break

		case JMP:
			pc = uint64(*(instruction.Next))
			break

		case JEZ:
			val, sts := program_stack.Pop()

			if val == nil {
				sts.Error()
			}

			if val.bytes[0] == 0 {
				pc = uint64(*instruction.Next)
			} else {
				pc++
			}

			break

		case JNZ:
			val, sts := program_stack.Pop()

			if val == nil {
				sts.Error()
			}

			if val.bytes[0] != 0 {
				pc = uint64(*instruction.Next)
			} else {
				pc++
			}
			break

		case JIE:
			// TODO : this

		case PP1:
			program_stack.Pop()
			break

		case PP2:
			program_stack.Pop()
			program_stack.Pop()
			break

		case PP3:
			program_stack.Pop()
			program_stack.Pop()
			program_stack.Pop()
			break
		}
	}
}
