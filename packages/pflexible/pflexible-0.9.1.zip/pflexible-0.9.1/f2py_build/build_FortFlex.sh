#!/bin/bash

rm FortFlex.pyf
f2py -m FortFlex -h FortFlex.pyf FortFlex.f
f2py -c --fcompiler=gfortran FortFlex.pyf FortFlex.f
cp FortFlex.so ../.

