Copy `wggen.conf.dist` to `wggen.conf`.

To generate private keys, use `wggen genkey`. Public keys are automatically
derived from private keys.

Generate server and client configurations:

    $ ./wggen.py

Configs will be written to `out/`.
