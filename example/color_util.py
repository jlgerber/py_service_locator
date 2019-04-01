"""
Utility classes relating to coloring text output to the terminal.
"""
import sys
__all__ = (
    "BgColors",
    "printit",
    "ColorCM"
)

class BgColors(object):
    """
    set of hex codes to change color of terminal output
    """
    def __init__(self, use_colors):
        """
        Parameters
        ----------
        use_colors: bool
            Whether to actuall print out hex codes or simply print out '' when accessed
            via properties
        """
        self.use_colors = use_colors

    @property
    def header(self):
        """
        header color
        """
        if self.use_colors:
            return '\033[95m'
        return ''

    @property
    def blue(self):
        """
        blue color
        """
        if self.use_colors:
            return '\033[94m'
        return ''

    @property
    def green(self):
        """green color"""
        if self.use_colors:
            return '\033[92m'
        return ''

    @property
    def red(self):
        """red color"""
        if self.use_colors:
            return '\033[93m'
        return ''

    @property
    def darkred(self):
        """dark red color"""
        if self.use_colors:
            return '\033[91m'
        return ''

    @property
    def endc(self):
        """end of color"""
        if self.use_colors:
            return '\033[0m'
        return ''

    @property
    def bold(self):
        """bold (sure its not a color. but you get it for free)"""
        if self.use_colors:
            return '\033[1m'
        return ''

    @property
    def underline(self):
        """again. not a color i know"""
        if self.use_colors:
            return '\033[4m'
        return ''


def printit(main, *args):
    """print function for TestColors"""
    # when main is passed in, it will be at minimum len(4) if there is only
    # a color specified. we need to print the color code without
    # introducing spaces or newlines
    if len(main) == 4 and len(args) == 0:
        sys.stdout.write(main)
        sys.stdout.flush()
        return
    if len(args) > 0:
        main = main.format(*args)
    print main


class ColorCM(object):
    """
    Context manager for setting a color.
    """
    def __init__(self, func, color_name):
        """
        pass a func function and a color_name

        Parameters
        ----------
        func: impl __call__
            A func function which will be invoked when the context manager is active.
            eg. with ColoCM(foo, blue) as cm: cm("blaa") -> foo("blaa")
        color_name: string
            The name of the color to format the output string with.
        """
        self.func = func
        self.color_name = color_name.lower()
        self.colors = BgColors(use_colors=True)

    def __enter__(self):
        return self

    def __call__(self, *args, **kwargs):
        self.func(getattr(self.colors, self.color_name) + " ".join(args))

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.func("{}".format(self.colors.endc))
