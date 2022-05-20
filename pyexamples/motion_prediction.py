try:
    from pycore.tikzeng import *
except ImportError:
    import sys
    sys.path.append('../')
    from pycore.tikzeng import *

from pycore.blocks import *


arch = [
    to_head('..'),
    to_cor(),
    to_begin(),

    # input
    to_input(pathfile='2layer-perceptron.pdf', to="(0,0,0)", name="lidar_input"),

    *block_ConvPoolConv(
        "C1",
        next=None,
        prev="lidar_input",
        offset="(10, 0, 0)",
        dim=(480, 480),
        in_channels=32,
        out_channels=32,
        add_pool=False,
        conv_layers=2
    ),

    *block_ConvPoolConv(
        "C2",
        next=None,
        prev="C1_out",
        offset="(10, 0, 0)",
        dim=(480, 480),
        in_channels=64,
        out_channels=64,
        add_pool=True,
        conv_layers=2
    ),

    *block_ConvPoolConv(
        "C4",
        next=None,
        prev="C2_out",
        offset="(10, 0, 0)",
        dim=(240, 240),
        in_channels=128,
        out_channels=128,
        add_pool=True,
        conv_layers=3
    ),

    *block_ConvPoolConv(
        "C8",
        next=None,
        prev="C4_out",
        offset="(10, 0, 0)",
        dim=(120, 120),
        in_channels=256,
        out_channels=256,
        add_pool=True,
        conv_layers=6
    ),

    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
