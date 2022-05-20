
from .tikzeng import *

# define new block


def block_input(name, to, offset=(0, 0, 0), size=(3, 3, 3), count=1, opacity=0.5, placement='north', caption=''):

    x, y, z = offset
    dx, dy, dz = size

    block_data = []
    for i in range(count):
        if not i:
            to = str(to)
            offset = str((x, y, z))
            caption = "{" + caption + "}"
        else:
            to = "({}{:02d}-{})".format(name, i-1, placement)
            offset = "(0,0,0)"
            caption = ""
        block_data.append(
            to_Box(
                name="{}{:02d}".format(name, i),
                offset=offset,
                to=to,
                n_filer=1,
                s_filer=None,
                width=dx,
                height=dy,
                depth=dz,
                caption=caption
            ),
        )

    return block_data


def block_2ConvPool(name, bottom, top, s_filer=None, n_filer=None, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5):

    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""

    return [
        to_ConvConvRelu(
            name="ccr_{}".format(name),
            s_filer=s_filer,
            n_filer=n_filer,
            offset=offset,
            to="({}-east)".format(bottom),
            width=(size[2], size[2]),
            height=size[0],
            depth=size[1],
        ),
        to_Pool(
            name="{}".format(top),
            offset="(0,0,0)",
            to="(ccr_{}-east)".format(name),
            width=1,
            height=size[0] - int(size[0]/4),
            depth=size[1] - int(size[0]/4),
            opacity=opacity, ),
        to_connection(
            "{}".format(bottom),
            "ccr_{}".format(name)
        )
    ]


def block_ConvPoolConv(name, next, prev, dim=(10, 10), offset="(0,0,0)", in_channels=1, out_channels=1, add_pool=False, conv_layers=2):
    dim_x, dim_y = dim

    scale_factor = 4
    channels = [in_channels//scale_factor]
    channels.extend([out_channels//scale_factor for _ in range(conv_layers - 1)])

    layers = []

    for layer_num in range(conv_layers):

        if not layer_num:
            layer_name = "{}_in".format(name)
            to = "{}-east".format(prev)
        else:
            if layer_num == conv_layers - 1:
                layer_name = "{}_out".format(name)
            else:
                layer_name = "{}_{:03d}".format(name, layer_num)
            to = "{}-east".format(last_name)
            offset = "(0,0,0)"

        layers.append(to_Conv(
            name=layer_name,
            s_filer="{}x{}".format(dim_x, dim_y),
            n_filer=channels[layer_num],
            offset=offset,
            to=to,
            width=channels[layer_num],
            height=dim_y,
            depth=dim_x,
        ))

        if not layer_num and add_pool:
            dim_x = max(1, dim_x // 2)
            dim_y = max(1, dim_y // 2)

            pool_name = "{}_pool".format(name)
            layers.append(to_Pool(
                pool_name,
                offset="(0,0,0)",
                to="{}-east".format(layer_name),
                width=2,
                height=dim_y,
                depth=dim_x,
            ))
            last_name = pool_name
        else:
            last_name = layer_name

    return layers


def block_Unconv(name, bottom, top, s_filer=None, n_filer=None, offset="(1,0,0)", size=(32, 32, 3.5), opacity=0.5):

    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""

    return [
        to_UnPool(name='unpool_{}'.format(name),    offset=offset,    to="({}-east)".format(bottom),
                  width=1,              height=size[0],       depth=size[1], opacity=opacity),
        to_ConvRes(name='ccr_res_{}'.format(name),   offset="(0,0,0)", to="(unpool_{}-east)".format(name),
                   s_filer=s_filer, n_filer=n_filer, width=size[2], height=size[0], depth=size[1], opacity=opacity),
        to_Conv(name='ccr_{}'.format(name),       offset="(0,0,0)", to="(ccr_res_{}-east)".format(name),
                s_filer=s_filer, n_filer=n_filer, width=size[2], height=size[0], depth=size[1]),
        to_ConvRes(name='ccr_res_c_{}'.format(name), offset="(0,0,0)", to="(ccr_{}-east)".format(name),
                   s_filer=s_filer, n_filer=n_filer, width=size[2], height=size[0], depth=size[1], opacity=opacity),
        to_Conv(name='{}'.format(top),            offset="(0,0,0)", to="(ccr_res_c_{}-east)".format(name),
                s_filer=s_filer, n_filer=n_filer, width=size[2], height=size[0], depth=size[1]),
        to_connection(
            "{}".format(bottom),
            "unpool_{}".format(name)
        )
    ]


def block_Res(num, name, bottom, top, s_filer=None, n_filer=None, offset="(0,0,0)", size=(32, 32, 3.5), opacity=0.5):

    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""

    lys = []
    layers = [*['{}_{}'.format(name, i) for i in range(num-1)], top]
    for name in layers:
        ly = [to_Conv(
            name='{}'.format(name),
            offset=offset,
            to="({}-east)".format(bottom),
            s_filer=s_filer,
            n_filer=n_filer,
            width=size[2],
            height=size[0],
            depth=size[1]
        ),
            to_connection(
                "{}".format(bottom),
                "{}".format(name)
        )
        ]
        bottom = name
        lys += ly

    lys += [
        to_skip(of=layers[1], to=layers[-2], pos=1.25),
    ]
    return lys


def add_connections(start, finish, begin, end=None, step=1):
    connections = []

    if end is None:
        begin = 0
        end = begin

    for i in range(begin, end, step):
        for j in range(begin, end, step):
            start = "L1{:02d}".format(i)
            finish = "L2{:02d}".format(j)

            connections.append(to_connection(start, finish))

    return connections
