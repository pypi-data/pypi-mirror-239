#
# [name] nkj.plot.py
#
# Written by Yoshikazu NAKAJIMA (Wed Apr 14 18:59:31 JST 2021)
#
_LIB_DEBUGLEVEL = 1

def barplot_annotate_brackets(num1, num2, data, center, height, yerr=None, dh=.05, barh=.05, fs=None, maxasterix=None):
    #
    # reference (Japanese): https://omedstu.jimdofree.com/2019/02/11/matplotlib%E3%81%A7%E6%A3%92%E3%82%B0%E3%83%A9%E3%83%95%E9%96%93%E3%81%AE%E6%9C%89%E6%84%8F%E5%B7%AE%E3%81%AE%E6%8F%8F%E7%94%BB%E3%82%92%E3%81%99%E3%82%8B/
    # reference (English):  https://matplotlib.org/2.0.2/examples/api/barchart_demo.html
    #
    """
    Annotate barplot with p-values.
    :param num1: number of left bar to put bracket over
    :param num2: number of right bar to put bracket over
    :param data: string to write or number for generating asterixes
    :param center: centers of all bars (like plt.bar() input)
    :param height: heights of all bars (like plt.bar() input)
    :param yerr: yerrs of all bars (like plt.bar() input)
    :param dh: height offset over bar / bar + yerr in axes coordinates (0 to 1)
    :param barh: bar height in axes coordinates (0 to 1)
    :param fs: font size
    :param maxasterix: maximum number of asterixes to write (for very small p-values)
    """

    if type(data) is str:
        text = data
    else:
        # * is p < 0.05
        # ** is p < 0.005
        # *** is p < 0.0005
        # etc.
        text = ''
        p = .05

        while data < p:
            text += '*'
            p /= 10.

            if maxasterix and len(text) == maxasterix:
                break

        if len(text) == 0:
            text = 'n. s.'

    lx, ly = center[num1], height[num1]
    rx, ry = center[num2], height[num2]

    if yerr:
        ly += yerr[num1]
        ry += yerr[num2]

    ax_y0, ax_y1 = plt.gca().get_ylim()
    dh *= (ax_y1 - ax_y0)
    barh *= (ax_y1 - ax_y0)

    y = max(ly, ry) + dh

    barx = [lx, lx, rx, rx]
    bary = [y, y+barh, y+barh, y]
    mid = ((lx+rx)/2, y+barh)

    plt.plot(barx, bary, c='black')

    kwargs = dict(ha='center', va='bottom')
    if fs is not None:
        kwargs['fontsize'] = fs

    plt.text(*mid, text, **kwargs)

#-- main
