import os
import platform
import collections
import datetime
import calendar
import time

import dateutil.parser
import pkginfo

from contextlog import get_logger

from . import context
from . import imprules
from . import rules


# =====
InstanceInfo = collections.namedtuple("InstanceInfo", ("node", "pid"))


def get_instance_info():
    return InstanceInfo(
        node=platform.uname()[1],
        pid=os.getpid(),
    )


def get_version():
    pkg = pkginfo.get_metadata("powny")
    return (pkg.version if pkg is not None else None)  # None if not installed


def get_user_agent():
    return "Powny/{}".format(get_version() or "0.001")  # FIXME: crutch for not installed package


# =====
def make_isotime(unix=None):  # ISO 8601
    if unix is None:
        unix = time.time()
    return datetime.datetime.utcfromtimestamp(unix).strftime("%Y-%m-%d %H:%M:%S.%fZ")


def from_isotime(line):
    dt = dateutil.parser.parse(line)
    return calendar.timegm(dt.utctimetuple()) + dt.microsecond / 10 ** 6  # pylint: disable=maybe-no-member


# =====
def make_rules_path(rules_root, head):
    return os.path.join(rules_root, head)


def make_loader(rules_base):
    return imprules.Loader(
        module_base=rules_base,
        group_by=(
            ("handlers", rules.is_event_handler),
            ("methods", lambda _: True),
        ),
    )


def get_exposed(backend, loader, rules_root):
    head = backend.rules.get_head()
    exposed = None
    errors = None
    exc = None
    if head is not None:
        try:
            (exposed, errors) = loader.get_exposed(make_rules_path(rules_root, head))
        except Exception as err:
            exc = "{}: {}".format(type(err).__name__, err)
            get_logger().exception("Can't load HEAD '%s'", head)
    return (head, exposed, errors, exc)


def get_dumped_method(name, kwargs, exposed):
    method = exposed.get("methods", {}).get(name)
    if method is None:
        return None
    else:
        return context.dump_call(method, kwargs)


def get_dumped_handlers(kwargs, exposed):
    return {
        name: context.dump_call(handler, kwargs)
        for (name, handler) in exposed.get("handlers", {}).items()
        if rules.check_match(handler, kwargs)
    }
