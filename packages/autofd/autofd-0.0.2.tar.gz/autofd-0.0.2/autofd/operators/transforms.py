"""lu transformations"""
import numpy as np
import jax.linear_util as lu


@lu.transformation
def permute_args(perm, *args):
  inv_perm = tuple(np.argsort(perm))
  f_args = yield (args[i] for i in inv_perm), {}
  yield f_args


@lu.transformation
def return_at(i, *args):
  f_args = yield args, {}
  yield f_args[i]


@lu.transformation
def compose(gs, num_args, share_inputs, *args):
  i = 0
  if share_inputs:
    fargs = tuple(g(*args) for g in gs)
  else:
    fargs = []
    for g, na in zip(gs, num_args):
      fargs.append(g(*args[i:i + na]))
      i += na
    fargs = tuple(fargs)
  fgs_args = yield fargs, {}
  yield fgs_args
