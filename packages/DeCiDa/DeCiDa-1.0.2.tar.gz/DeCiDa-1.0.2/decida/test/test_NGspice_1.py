#!/usr/bin/env python
import user, decida, decida.test
from decida.NGspice import NGspice

test_dir = decida.test.test_dir()
NGspice(cktfile=test_dir + "hartley.ckt", xcol="time", ycols="v(c)")
