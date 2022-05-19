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
    *block_input("v", to=(0, 0, 0), offset=(0, 0, 0), size=(3, 3, 3), count=3, caption="Velocity"),
    *block_input("omega", to="(v00-west)", offset=(0, -2, 0), size=(3, 3, 3), count=3, caption="Angular Velocity"),
    *block_input("control", to="(omega00-west)", offset=(0, -2, 0), size=(3, 3, 3), count=2, caption="Actions"),
    *block_input("time", to="(control00-west)", offset=(0, -2, 0), size=(3, 3, 3), count=1, caption="Time"),

    # hidden layers
    *block_input("L1", to="(omega01-east)", offset=(2, -10, -3), size=(3, 3, 3), count=51, opacity=0.9, placement='northwest', caption="100"),
    *block_input("L2", to="(L101-east)", offset=(4, 0, 0), size=(3, 3, 3), count=51, placement='northwest', caption="100"),

    # output
    *block_input("displacement", to="(L225-east)", offset=(2, 0, 0), size=(3, 3, 3), count=3, caption="Displacement"),


    # connections
    to_connection("v01", "L125"),
    to_connection("omega01", "L125"),
    to_connection("control01", "L125"),
    to_connection("time00", "L125"),
    *add_connections("L1", "L2", 0, 51, 5),

    to_connection("L225", "displacement00"),


    to_end()
]


def main():
    namefile = str(sys.argv[0]).split('.')[0]
    to_generate(arch, namefile + '.tex')


if __name__ == '__main__':
    main()
