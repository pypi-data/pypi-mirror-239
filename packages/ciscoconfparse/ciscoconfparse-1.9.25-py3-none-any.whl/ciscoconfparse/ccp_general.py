from collections.abc import MutableSequence, Sequence
import inspect
import re
import os

from loguru import logger


ALL_VALID_SYNTAX = (
    "ios",
    "nxos",
    "asa",
    "junos",
)

# Maximum ipv6 as an integer
IPV4_MAXINT = 4294967295
IPV6_MAXINT = 340282366920938463463374607431768211455
IPV4_MAXSTR_LEN = 31  # String length with periods, slash, and netmask
IPV6_MAXSTR_LEN = 39 + 4  # String length with colons, slash and masklen

IPV4_MAX_PREFIXLEN = 32
IPV6_MAX_PREFIXLEN = 128

_IPV6_RGX_CLS = r"[0-9a-fA-F]{1,4}"
_CISCO_RANGE_ATOM_STR = r"""\d+\s*\-*\s*\d*"""
_CISCO_RANGE_STR = r"""^(?P<intf_prefix>[a-zA-Z\s]*)(?P<slot_prefix>[\d\/]*\d+\/)*(?P<range_text>(\s*{})*)$""".format(
    _CISCO_RANGE_ATOM_STR
)
_RGX_CISCO_RANGE = re.compile(_CISCO_RANGE_STR)

####################### Begin IPv6 #############################

_IPV6_REGEX_STR = r"""(?!:::\S+?$)       # Negative Lookahead for 3 colons
 (?P<addr>                               # Begin a group named 'addr'
 (?P<opt1>{0}(?::{0}){{7}})              # no double colons, option 1
|(?P<opt2>(?:{0}:){{1}}(?::{0}){{1,6}})  # match fe80::1
|(?P<opt3>(?:{0}:){{2}}(?::{0}){{1,5}})  # match fe80:a::1
|(?P<opt4>(?:{0}:){{3}}(?::{0}){{1,4}})  # match fe80:a:b::1
|(?P<opt5>(?:{0}:){{4}}(?::{0}){{1,3}})  # match fe80:a:b:c::1
|(?P<opt6>(?:{0}:){{5}}(?::{0}){{1,2}})  # match fe80:a:b:c:d::1
|(?P<opt7>(?:{0}:){{6}}(?::{0}){{1,1}})  # match fe80:a:b:c:d:e::1
|(?P<opt8>:(?::{0}){{1,7}})              # ipv6 with leading double colons
|(?P<opt9>(?:{0}:){{1,7}}:)              # ipv6 with trailing double colons
|(?P<opt10>(?:::))                       # ipv6 bare double colons (default route)
)([/\s](?P<masklen>\d+))*                # match 'masklen' and end 'addr' group
""".format(_IPV6_RGX_CLS)

_IPV6_REGEX_STR_COMPRESSED1 = r"""(?!:::\S+?$)(?P<addr1>(?P<opt1_1>{0}(?::{0}){{7}})|(?P<opt1_2>(?:{0}:){{1}}(?::{0}){{1,6}})|(?P<opt1_3>(?:{0}:){{2}}(?::{0}){{1,5}})|(?P<opt1_4>(?:{0}:){{3}}(?::{0}){{1,4}})|(?P<opt1_5>(?:{0}:){{4}}(?::{0}){{1,3}})|(?P<opt1_6>(?:{0}:){{5}}(?::{0}){{1,2}})|(?P<opt1_7>(?:{0}:){{6}}(?::{0}){{1,1}})|(?P<opt1_8>:(?::{0}){{1,7}})|(?P<opt1_9>(?:{0}:){{1,7}}:)|(?P<opt1_10>(?:::)))""".format(_IPV6_RGX_CLS)

_IPV6_REGEX_STR_COMPRESSED2 = r"""(?!:::\S+?$)(?P<addr2>(?P<opt2_1>{0}(?::{0}){{7}})|(?P<opt2_2>(?:{0}:){{1}}(?::{0}){{1,6}})|(?P<opt2_3>(?:{0}:){{2}}(?::{0}){{1,5}})|(?P<opt2_4>(?:{0}:){{3}}(?::{0}){{1,4}})|(?P<opt2_5>(?:{0}:){{4}}(?::{0}){{1,3}})|(?P<opt2_6>(?:{0}:){{5}}(?::{0}){{1,2}})|(?P<opt2_7>(?:{0}:){{6}}(?::{0}){{1,1}})|(?P<opt2_8>:(?::{0}){{1,7}})|(?P<opt2_9>(?:{0}:){{1,7}}:)|(?P<opt2_10>(?:::)))""".format(_IPV6_RGX_CLS)

_IPV6_REGEX_STR_COMPRESSED3 = r"""(?!:::\S+?$)(?P<addr3>(?P<opt3_1>{0}(?::{0}){{7}})|(?P<opt3_2>(?:{0}:){{1}}(?::{0}){{1,6}})|(?P<opt3_3>(?:{0}:){{2}}(?::{0}){{1,5}})|(?P<opt3_4>(?:{0}:){{3}}(?::{0}){{1,4}})|(?P<opt3_5>(?:{0}:){{4}}(?::{0}){{1,3}})|(?P<opt3_6>(?:{0}:){{5}}(?::{0}){{1,2}})|(?P<opt3_7>(?:{0}:){{6}}(?::{0}){{1,1}})|(?P<opt3_8>:(?::{0}){{1,7}})|(?P<opt3_9>(?:{0}:){{1,7}}:)|(?P<opt3_10>(?:::)))""".format(_IPV6_RGX_CLS)

####################### Begin IPv4 #############################

_IPV4_REGEX_STR = r"^(?P<addr>\d+\.\d+\.\d+\.\d+)"
_RGX_IPV4ADDR = re.compile(_IPV4_REGEX_STR)
_RGX_IPV4ADDR_WITH_MASK = re.compile(
    r"""
     (?:
       ^(?P<v4addr_nomask>\d+\.\d+\.\d+\.\d+)$
      |(?:^
         (?:(?P<v4addr_netmask>\d+\.\d+\.\d+\.\d+))(\s+|\/)(?:(?P<netmask>\d+\.\d+\.\d+\.\d+))
       $)
      |^(?:\s*(?P<v4addr_prefixlen>\d+\.\d+\.\d+\.\d+)(?:\/(?P<masklen>\d+))\s*)$
    )
    """,
    re.VERBOSE,
)

if False:
    @logger.catch(reraise=True)
    def junos_unsupported(func):
        """A function wrapper to warn junos users of unsupported features"""

        @logger.catch(reraise=True)
        def wrapper(*args, **kwargs):
            warn = f"syntax='junos' does not fully support config modifications such as .{func.__name__}(); see Github Issue #185.  https://github.com/mpen  ning/ciscoconfparse/issues/185"
            syntax = kwargs.get("syntax", None)
            if len(args) >= 1:
                if isinstance(args[0], ciscoconfparse.ConfigList):
                    syntax = args[0].syntax
                else:
                    # print("TYPE", type(args[0]))
                    syntax = args[0].confobj.syntax
            if syntax == "junos":
                logger.warning(warn, UnsupportedFeatureWarning)
            func(*args, **kwargs)

        return wrapper


class PythonOptimizeCheck(object):
    """
    Check if we're running under "python -O ...".  The -O option removes
    all `assert` statements at runtime.  ciscoconfparse depends heavily on
    `assert` and running ciscoconfparse under python -O is a really bad idea.

    __debug__ is True unless run with `python -O ...`.  __debug__ is False
    under `python -O ...`.

    Also throw an error if PYTHONOPTIMIZE is set in the windows or unix shell.

    This class should be run in <module_name_dir>/__init__.py.

    This condition is not unique to ciscoconfparse.

    Simple usage (in __init__.py):
    ------------------------------

    # Handle PYTHONOPTIMIZE problems...
    from ciscoconfparse.ccp_general import PythonOptimizeCheck
    _ = PythonOptimizeCheck()


    """
    @logger.catch(reraise=True)
    def __init__(self):

        self.PYTHONOPTIMIZE_env_value = os.environ.get("PYTHONOPTIMIZE", None)

        error = "__no_error__"
        try:
            # PYTHONOPTIMIZE is not supported...  in the linux shell
            # disable it with `unset PYTHONOPTIMIZE`
            if isinstance(self.PYTHONOPTIMIZE_env_value, str) and self.PYTHONOPTIMIZE_env_value.strip()!="":
                # This condition explicitly allows PYTHONOPTIMIZE="", which
                # is not a problem.
                error = "Your environment has PYTHONOPTIMIZE set.  ciscoconfparse doesn't support running under PYTHONOPTIMIZE."
            # PYTHONOPTIMIZE is not supported...  in the linux shell
            # disable it with `unset PYTHONOPTIMIZE`
            elif self.PYTHONOPTIMIZE_env_value is not None:
                error = "Your environment has PYTHONOPTIMIZE set.  ciscoconfparse doesn't support running under PYTHONOPTIMIZE."
            # Throw an error if we're running under `python -O`.  `python -O` is not supported
            # We should keep the __debug__ check for `-O` at the end, otherwise it
            # masks identifying problems with PYTHONOPTIMIZE set in the shell...
            elif __debug__ is False:
                # Running under 'python -O'
                error = "You're using `python -O`. Please don't.  ciscoconfparse doesn't support `python -O`"

            else:
                # whew...
                pass

        except Exception as exception_info:
            print("exception_info", str(exception_info))
            raise RuntimeError("Something bad happened in PYTHONOPTIMIZE checks.  Please report this problem as a ciscoconfparse bug")

        if error != "__no_error__":
            raise PythonOptimizeException(error)


