# VCV Rack loader for (Eventually) Raspberry PI

The goal of this is to provide a silly simple screen interface so that I can run VCV Rack on a Raspberry pi and have
a few simple synths that I can fiddle with.

## TODO:

* Figure out how to use `xdotool` to interact with stuff in X-windows; note that it is highly unlikely that closing and
  opening VCV rack will be a good way to do this, as it is pretty slow.
* Redo the interface to make it suit the 16 x 2 screen
* It sounds like [`python-libxdo`](https://pypi.org/project/python-libxdo/) should work as a library