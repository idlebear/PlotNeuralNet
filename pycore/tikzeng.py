
import os


def to_head(projectpath):
    pathlayers = os.path.join(projectpath, 'layers/').replace('\\', '/')
    return r"""
\documentclass[border=8pt, multi, tikz]{standalone}
\usepackage{import}
\subimport{""" + pathlayers + r"""}{init}
\usetikzlibrary{positioning}
\usetikzlibrary{3d} %for including external image
"""


def to_cor():
    return r"""
\def\ConvColor{rgb:yellow,5;red,2.5;white,5}
\def\ConvReluColor{rgb:yellow,5;red,5;white,5}
\def\PoolColor{rgb:red,1;black,0.3}
\def\UnpoolColor{rgb:blue,2;green,1;black,0.3}
\def\FcColor{rgb:blue,5;red,2.5;white,5}
\def\FcReluColor{rgb:blue,5;red,5;white,4}
\def\SoftmaxColor{rgb:magenta,5;black,7}
\def\SumColor{rgb:blue,5;green,15}
\def\BoxColor{rgb:yellow,2;white,0.3}
"""


def to_begin():
    return r"""
\newcommand{\copymidarrow}{\tikz \draw[-Stealth,line width=0.8mm,draw={rgb:blue,4;red,1;green,1;black,3}] (-0.3,0) -- ++(0.3,0);}

\begin{document}
\begin{tikzpicture}
\tikzstyle{connection}=[ultra thick,every node/.style={sloped,allow upside down},draw=\edgecolor,opacity=0.7]
\tikzstyle{copyconnection}=[ultra thick,every node/.style={sloped,allow upside down},draw={rgb:blue,4;red,1;green,1;black,3},opacity=0.7]
"""

# layers definition


def to_input(pathfile, to='(-3,0,0)', width=8, height=8, name="temp"):
    return r"""
\node[canvas is zy plane at x=0] (""" + name + """-east) at """ + to + """
     {\includegraphics[width=""" + str(width)+"cm"+""",height=""" + str(height)+"cm"+"""]{""" + pathfile + """}};
"""


def parse_to(to):
    if type(to) is tuple:
        return str(to)
    return to if to[0] == '(' and to[-1] == ')' else '(' + to + ')'


def to_Box(name, offset="(0,0,0)", to="(0,0,0)", s_filer=None, n_filer=None, width=2, height=2, depth=2, caption=""):
    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""
    to = parse_to(to)

    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name =""" + name + """,
        caption = """ + caption + r""",
        xlabel = {""" + n_filer + """ },
        zlabel = """ + s_filer + """,
        fill=\BoxColor,
        height = """ + str(height) + """,
        width = """ + str(width) + """,
        depth = """ + str(depth) + """
        }
    };
"""


# Conv
def to_Conv(name, s_filer=None, n_filer=None, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""

    to = parse_to(to)

    if type(width) is tuple:
        width_str = []
        for w in width:
            width_str.append(str(w))
        width_str = ", ".join(width_str)
    else:
        width_str = str(width)

    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name =""" + name + """,
        caption = """ + caption + r""",
        xlabel = {""" + str(n_filer) + """ },
        zlabel = """ + str(s_filer) + """,
        fill=\ConvColor,
        height = """ + str(height) + """,
        width = { """ + width_str + """ },
        depth = """ + str(depth) + """
        }
    };
"""

# Conv,Conv,relu
# Bottleneck


def to_ConvConvRelu(name, s_filer=None, n_filer=None, offset="(0,0,0)", to="(0,0,0)", width=(2, 2), height=40, depth=40, caption=" "):
    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""

    to = parse_to(to)

    if type(width) is tuple:
        width_str = []
        for w in width:
            width_str.append(str(w))
        width_str = ", ".join(width_str)
    else:
        width_str = str(width)

    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {Box={
        name = """ + name + """,
        caption = """ + caption + """,
        xlabel = { """ + n_filer + """ },
        zlabel = """ + s_filer + """,
        fill=\ConvColor,
        height = """ + str(height) + """,
        width = { """ + width_str + """ },
        depth = """ + str(depth) + """
        }
    };
"""


# Pool
def to_Pool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    to = parse_to(to)

    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {Box={
        name="""+name+""",
        caption = """ + caption + r""",
        fill=\PoolColor,
        opacity = """ + str(opacity) + """,
        height = """ + str(height) + """,
        width = """ + str(width) + """,
        depth = """ + str(depth) + """
        }
    };
"""

# unpool4,


def to_UnPool(name, offset="(0,0,0)", to="(0,0,0)", width=1, height=32, depth=32, opacity=0.5, caption=" "):
    to = parse_to(to)

    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {Box={
        name = """ + name + r""",
        caption = """ + caption + r""",
        fill=\UnpoolColor,
        opacity = """ + str(opacity) + """,
        height = """ + str(height) + """,
        width = """ + str(width) + """,
        depth = """ + str(depth) + """
        }
    };
"""


def to_ConvRes(name, s_filer=None, n_filer=None, offset="(0,0,0)", to="(0,0,0)", width=6, height=40, depth=40, opacity=0.2, caption=" "):
    s_filer = str(s_filer) if s_filer is not None else ""
    n_filer = str(n_filer) if n_filer is not None else ""

    to = parse_to(to)

    return r"""
\pic[shift={ """ + offset + """ }] at """ + to + """
    {RightBandedBox={
        name =""" + name + """,
        caption =""" + caption + """,
        xlabel ={{ """ + str(n_filer) + """, }},
        zlabel = """ + str(s_filer) + r""",
        fill={rgb:white,1;black,3},
        bandfill={rgb:white,1;black,2},
        opacity = """ + str(opacity) + """,
        height = """ + str(height) + """,
        width = """ + str(width) + """,
        depth = """ + str(depth) + """
        }
    };
"""


# ConvSoftMax
def to_ConvSoftMax(name, s_filer=None, offset="(0,0,0)", to="(0,0,0)", width=1, height=40, depth=40, caption=" "):
    s_filer = str(s_filer) if s_filer is not None else ""

    to = parse_to(to)

    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name =""" + name + """,
        caption = """ + caption + """,
        zlabel = """ + str(s_filer) + """,
        fill=\SoftmaxColor,
        height = """ + str(height) + """,
        width = """ + str(width) + """,
        depth = """ + str(depth) + """
        }
    };
"""

# SoftMax


def to_SoftMax(name, s_filer=None, offset="(0,0,0)", to="(0,0,0)", width=1.5, height=3, depth=25, opacity=0.8, caption=" "):
    s_filer = str(s_filer) if s_filer is not None else ""
    to = parse_to(to)

    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Box={
        name =""" + name + """,
        caption = """ + caption + """,
        xlabel={{" ","dummy"}},
        zlabel = """ + str(s_filer) + """,
        fill=\SoftmaxColor,
        opacity = """ + str(opacity) + """,
        height = """ + str(height) + """,
        width = """ + str(width) + """,
        depth = """ + str(depth) + """
        }
    };
"""


def to_Sum(name, offset="(0,0,0)", to="(0,0,0)", radius=2.5, opacity=0.6):
    to = parse_to(to)
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {Ball={
        name =""" + name + """,
        fill=\SumColor,
        opacity = """ + str(opacity) + """,
        radius = """ + str(radius) + """,
        logo=$+$
        }
    };
"""


def to_FC(name, offset="(0,0,0)", to="(0,0,0)", n_layers=1, radius=4):
    to = parse_to(to)
    return r"""
\pic[shift={""" + offset + """}] at """ + to + """
    {FC={
        name =""" + name + """,
        fill=\SumColor,
        opacity = """ + str(opacity) + """,
        radius = """ + str(radius) + """,
        logo=$+$
        }
    };
    """


def to_connection(start, finish):
    return r"""
\draw [connection]  ("""+start+"""-east)    -- node {\midarrow} ("""+finish+"""-west);
"""


def to_skip(of, to, pos=1.25):
    return r"""
\path (""" + of + """-southeast) -- (""" + of + """-northeast) coordinate[pos=""" + str(pos) + """] (""" + of + """-top) ;
\path (""" + to + """-south)  -- (""" + to + """-north)  coordinate[pos=""" + str(pos) + """] (""" + to + """-top) ;
\draw [copyconnection]  ("""+of+"""-northeast)
-- node {\copymidarrow}("""+of+"""-top)
-- node {\copymidarrow}("""+to+"""-top)
-- node {\copymidarrow} ("""+to+"""-north);
"""


def to_end():
    return r"""
\end{tikzpicture}
\end{document}
"""


def to_generate(arch, pathname="file.tex"):
    with open(pathname, "w") as f:
        for c in arch:
            print(c)
            f.write(c)
