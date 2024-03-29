"""
Ada domain for sphinx.

:copyright: Copyright 2010 by Tero Koskinen.
:copyright: Copyright 2020 by AdaCore.
:license: BSD, see LICENSE for details

Some parts of the code copied from erlangdomain by SHIBUKAWA Yoshiki.
"""

from __future__ import annotations

import logging
import re
from typing import (
    Iterable, List, Protocol, Sequence, Union, cast, Any, Dict, NamedTuple,
    Iterator, Tuple
)

from docutils import nodes
from docutils.nodes import Element
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from docutils.parsers.rst.states import Inliner

from sphinx import addnodes
from sphinx.addnodes import desc_signature
from sphinx.application import Sphinx
from sphinx.builders import Builder
from sphinx.directives import ObjectDescription
from sphinx.domains import Domain, Index, IndexEntry, ObjType
from sphinx.environment import BuildEnvironment
from sphinx.locale import _, __
from sphinx.roles import XRefRole
from sphinx.util.docfields import Field, TypedField
from sphinx.util.nodes import make_refnode, make_id

try:
    import libadalang as lal

    USE_LAL = True
    lal_context = lal.AnalysisContext(unit_provider=lal.UnitProvider.auto([]))
except ImportError:
    USE_LAL = False


# TODO: Due to the inheritance structure hierarchy of docutils nodes, and to
# limitations in mypy's protocol typing, we have no way of saying that we  want
# a node that has a constructor as below, and that is also a Node (AFAICT). For
# the moment, we'll just enforce the proper constructor
class DescNodeProtocol(Protocol):

    def __init__(self, rawsource: str = '', text: str = '',
                 *args: nodes.Element,
                 **kwargs: Any) -> None:
        pass


logger = logging.getLogger(__name__)

ada_type_sig_re = re.compile(r"^type\s+(\w+)", re.VERBOSE)
ada_object_sig_re = re.compile(r"^(\w+)\s+(:\s+.+)", re.VERBOSE)
ada_package_inst_sig_re = re.compile(
    r"^package\s+(\w+)\s+is\s+new\s+([\w\.]+)\s*", re.VERBOSE
)
ada_subp_sig_re = re.compile(
    r"^(procedure|function)\s+(\w+|\".*?\")\s*(.*)", re.VERBOSE
)

ObjectEntry = NamedTuple(
    "ObjectEntry", [("docname", str), ("node_id", str), ("objtype", str)]
)


class AdaObject(ObjectDescription):
    """
    Description of an Ada language object.
    """

    doc_field_types = [
        TypedField(
            "parameter",
            label=_("Parameters"),
            names=("param", "parameter", "arg", "argument"),
            typerolename="type",
            typenames=("type",),
        ),
        TypedField(
            "component",
            label=_("Components"),
            names=("component", "comp"),
            typerolename="type",
            typenames=("type",),
        ),
        TypedField(
            "discriminant",
            label=_("Discriminants"),
            names=("discriminant", "discr"),
            typerolename="type",
            typenames=("type",),
        ),
        Field(
            "returnvalue",
            label=_("Returns"),
            has_arg=False,
            names=("returns", "return"),
        ),
        Field(
            "instpkg",
            label=_("Instantiated generic package"),
            has_arg=False,
            names=("instpkg",),
            bodyrolename="type",
        ),
        Field(
            "defval",
            label=_("Default value"),
            has_arg=False,
            names=("defval",),
            bodyrolename="type",
        ),
        Field(
            "objtype",
            label=_("Object type"),
            has_arg=False,
            names=("objtype",),
            bodyrolename="type",
        ),
        Field(
            "renames",
            label=_("Renames"),
            has_arg=False,
            names=("renames",),
            bodyrolename="type",
        ),
    ]

    option_spec = {
        "package": directives.unchanged,
    }

    def get_full_name(self, signode: desc_signature, name: str) -> str:
        """
        Get the full name for this Ada object.
        """
        env_modname = self.options.get(
            "package",
            self.env.temp_data.get("ada:package", "")
        )
        fullname = env_modname + "." + name if env_modname else name

        signode["package"] = env_modname
        signode["fullname"] = fullname

        return fullname

    def make_refnode(
        self,
        target: str,
        cont_node_type: type[DescNodeProtocol]
    ) -> addnodes.pending_xref:
        refnode = addnodes.pending_xref(
            "",
            refdomain="ada",
            refexplicit=False,
            reftype="type",
            reftarget=target,
        )
        env_modname = self.options.get(
            "package", self.env.temp_data.get("ada:package", "")
        )
        refnode["ada:package"] = env_modname
        refnode += cont_node_type("", target)
        return refnode

    def handle_subp_sig(self, sig: str, signode: desc_signature) -> str:

        subp_spec_unit = lal_context.get_from_buffer(
            "<input>", sig, rule=lal.GrammarRule.subp_spec_rule
        )
        subp_spec: lal.SubpSpec = subp_spec_unit.root.cast(lal.SubpSpec)

        if subp_spec is None:
            raise self.error("Couldn't parse the subp spec")

        if len(subp_spec_unit.diagnostics) > 0:
            raise self.error("Errors parsing the subp spec")

        is_func = subp_spec.f_subp_returns is not None

        subp_name, returntype = (
            subp_spec.f_subp_name.text,
            subp_spec.f_subp_returns.text if is_func else ""
        )

        kind = "function " if is_func else "procedure "
        signode += addnodes.desc_annotation(kind, kind)
        signode += addnodes.desc_name(signode, subp_name)

        signode += nodes.Text(" ")

        param_list = addnodes.desc_parameterlist()
        param_list.child_text_separator = "; "
        signode += param_list

        if subp_spec.f_subp_params:
            for p in subp_spec.f_subp_params.f_params:
                param = addnodes.desc_parameter()
                param_list += param
                for i, name in enumerate(p.f_ids):
                    param += addnodes.desc_sig_name("", name.text)
                    if i + 1 < len(p.f_ids):
                        param += addnodes.desc_sig_punctuation("", ", ")
                param += addnodes.desc_sig_punctuation("", " : ")

                refnode = self.make_refnode(
                    p.f_type_expr.text, addnodes.desc_sig_name
                )
                param += refnode

        if returntype:
            signode += self.make_refnode(returntype, addnodes.desc_returns)

        return subp_name

    def handle_type_sig(self, sig: str, signode: desc_signature) -> str:
        m = ada_type_sig_re.match(sig)
        if m is None:
            raise Exception(f"m did not match for sig {sig}")

        name = m.groups()[0]

        signode += addnodes.desc_annotation("type ", "type ")
        signode += addnodes.desc_name(signode, name)
        signode += addnodes.desc_type(name, "")

        return name

    def handle_object_sig(self, sig: str, signode: desc_signature) -> str:
        m = ada_object_sig_re.match(sig)
        if m is None:
            raise Exception(f"m did not match for sig {sig}")

        name, descr = m.groups()
        descr = " " + descr

        signode += addnodes.desc_name(signode, name)
        signode += addnodes.desc_annotation(descr, descr)
        signode += addnodes.desc_type(name, "")

        return name

    def handle_gen_package_sig(self, sig: str, signode: desc_signature) -> str:
        signode += addnodes.desc_annotation(
            "generic package ", "generic package "
        )
        signode += addnodes.desc_name(signode, sig)
        return sig

    def handle_package_sig(self, sig: str, signode: desc_signature) -> str:
        signode += addnodes.desc_annotation("package ", "package ")
        signode += addnodes.desc_name(signode, sig)
        return sig

    def handle_exception_sig(self, sig: str, signode: desc_signature) -> str:
        signode += addnodes.desc_name(signode, sig)
        signode += addnodes.desc_annotation(": exception", ": exception")
        return sig

    def handle_package_inst(self, sig: str, signode: desc_signature) -> str:
        m = ada_package_inst_sig_re.match(sig)
        if m is None:
            raise Exception(f"m did not match for sig {sig}")
        name, inst = m.groups()

        signode += addnodes.desc_annotation("package ", "package ")
        signode += addnodes.desc_name(signode, name)
        signode += addnodes.desc_name(" ", " ")
        signode += addnodes.desc_annotation(" is new ", " is new ")
        signode += addnodes.desc_name(inst, inst)

        return name

    def handle_signature(self, sig: str, signode: desc_signature) -> str:
        if self.objtype in ["function", "procedure"]:
            ret = self.handle_subp_sig(sig, signode)
        elif self.objtype == "type":
            ret = self.handle_type_sig(sig, signode)
        elif self.objtype == "object":
            ret = self.handle_object_sig(sig, signode)
        elif self.objtype == "exception":
            ret = self.handle_exception_sig(sig, signode)
        elif self.objtype == "generic-package-instantiation":
            ret = self.handle_package_inst(sig, signode)
        elif self.objtype == "generic_package":
            ret = self.handle_gen_package_sig(sig, signode)
        elif self.objtype == "package":
            ret = self.handle_package_sig(sig, signode)
        else:
            raise Exception(f"Unhandled ada object: {self.objtype} {sig}")

        return ret

    def get_index_text(self, name: str) -> str:
        if self.objtype == "function":
            return f"{name} (Ada function)"
        elif self.objtype == "procedure":
            return f"{name} (Ada procedure)"
        elif self.objtype == "type":
            return f"{name} (Ada type)"
        else:
            return ""

    def add_target_and_index(
        self, name: str, sig: str, signode: desc_signature
    ) -> None:

        full_name = self.get_full_name(signode, name)

        node_id = make_id(self.env, self.state.document, "", full_name)
        signode["ids"].append(node_id)

        # Assign old styled node_id(full_name) not to break old hyperlinks (if
        # possible) Note: Will removed in Sphinx-5.0 (RemovedInSphinx50Warning)
        if node_id != full_name and full_name not in self.state.document.ids:
            signode["ids"].append(full_name)

        self.state.document.note_explicit_target(signode)

        domain = cast(AdaDomain, self.env.get_domain("ada"))

        domain.note_object(full_name, self.objtype, node_id, location=signode)

        indextext = self.get_index_text(full_name)
        if indextext:
            self.indexnode["entries"].append(
                ("single", indextext, node_id, "", None)
            )


class AdaSetPackage(Directive):
    """
    Directive to mark description of a new package.
    """

    has_content = False
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {
        "platform": lambda x: x,
        "synopsis": lambda x: x,
        "noindex": directives.flag,
        "deprecated": directives.flag,
    }

    def run(self) -> Sequence[nodes.Node]:
        env = self.state.document.settings.env
        modname = self.arguments[0].strip()
        noindex = "noindex" in self.options
        env.temp_data["ada:package"] = modname
        env.domaindata["ada"]["packages"][modname] = (
            env.docname,
            self.options.get("synopsis", ""),
            self.options.get("platform", ""),
            "deprecated" in self.options,
        )
        targetnode = nodes.target(
            "", "", ids=["package-" + modname], ismod=True
        )
        node_id = make_id(env, self.state.document, "", modname)
        self.state.document.note_explicit_target(targetnode)
        targetnode["ids"].append(node_id)
        ret: List[nodes.Node] = [targetnode]
        # XXX this behavior of the module directive is a mess...
        if "platform" in self.options:
            platform = self.options["platform"]
            node = nodes.paragraph()
            node += nodes.emphasis("", _("Platforms: "))
            node += nodes.Text(platform, platform)
            ret.append(node)
        # the synopsis isn't printed; in fact, it is only used in the
        # modindex currently.
        if not noindex:
            indextext = _("%s (package)") % modname
            inode = addnodes.index(
                entries=[
                    ("single", indextext, "package-" + modname, modname, None)
                ]
            )
            ret.append(inode)

        # Register the module in the Ada domain index, so that we can reference
        # it.
        domain = cast(AdaDomain, env.get_domain("ada"))
        domain.note_object(modname, "module", node_id, location=targetnode)

        return ret


def rmlink(name: str, rawtext: str, text: str,
           lineno: int, inliner: Inliner, options: Dict[str, Any] = {},
           content: List[str] = []) -> Tuple[List[nodes.Node],
                                             List[nodes.system_message]]:
    """
    Role to reference an Ada Reference Manual entry, such as
    ``:ada:rmlink:`3.4.2` ``
    """
    rm_page = text.replace(".", "-")
    url = f"http://www.ada-auth.org/standards/2xrm/html/RM-{rm_page}.html"
    node = nodes.reference(rawtext, f"RM {text}", refuri=url, **options)
    return [node], []


class AdaXRefRole(XRefRole):

    def process_link(
        self,
        env: BuildEnvironment,
        refnode: Element,
        has_explicit_title: bool,
        title: str, target: str
    ) -> tuple[str, str]:

        refnode["reftype"] = "type"
        refnode["refexplicit"] = False
        refnode["refdomain"] = "ada"
        refnode["reftarget"] = target

        env_modname = self.env.temp_data.get("ada:package", "")
        refnode["ada:package"] = env_modname
        return title, target


class AdaPackageIndex(Index):
    """
    Index subclass to provide the Ada package index.
    """

    name = "modindex"
    localname = _("Ada Package Index")
    shortname = _("Ada packages")

    def generate(
        self, docnames: Union[Iterable[str], None] = None
    ) -> Tuple[List[Tuple[str, List[IndexEntry]]], bool]:

        content: Dict[str, List[IndexEntry]] = {}
        # list of prefixes to ignore
        ignores = self.domain.env.config["modindex_common_prefix"]
        ignores = sorted(ignores, key=len, reverse=True)
        # list of all modules, sorted by module name
        # (Python 3 has no iteritems, so use items).
        modules = sorted(
            self.domain.data["packages"].items(), key=lambda x: x[0].lower()
        )
        # sort out collapsable modules
        prev_modname = ""
        num_toplevels = 0
        for modname, (docname, synopsis, platforms, deprecated) in modules:
            if docnames and docname not in docnames:
                continue

            for ignore in ignores:
                if modname.startswith(ignore):
                    modname = modname[len(ignore):]
                    stripped = ignore
                    break
            else:
                stripped = ""

            # we stripped the whole module name?
            if not modname:
                modname, stripped = stripped, ""

            entries = content.setdefault(modname[0].lower(), [])

            package = modname.split(":")[0]
            if package != modname:
                # it's a submodule
                if not prev_modname.startswith(package):
                    # submodule without parent in list, add dummy entry
                    entries.append(
                        IndexEntry(stripped + package, 1, "", "", "", "", "")
                    )
                subtype = 2
            else:
                num_toplevels += 1
                subtype = 0

            qualifier = deprecated and _("Deprecated") or ""
            entries.append(
                IndexEntry(
                    stripped + modname,
                    subtype,
                    docname,
                    "package-" + stripped + modname,
                    platforms,
                    qualifier,
                    synopsis,
                )
            )
            prev_modname = modname

        # apply heuristics when to collapse modindex at page load:
        # only collapse if number of toplevel modules is larger than
        # number of submodules.
        collapse = len(modules) - num_toplevels < num_toplevels

        # sort by first letter
        # (Python 3 has no iteritems, so use items).
        list_content = sorted(content.items())

        return list_content, collapse


class AdaDomain(Domain):
    """Ada language domain."""

    name = "ada"
    label = "Ada"
    object_types = {
        "function": ObjType(_("function"), "func"),
        "procedure": ObjType(_("procedure"), "proc"),
        "type": ObjType(_("type"), "type"),
        "package": ObjType(_("package"), "pkg"),
    }

    directives = {
        "function": AdaObject,
        "procedure": AdaObject,
        "type": AdaObject,
        "set_package": AdaSetPackage,
        "package": AdaObject,
        "generic_package": AdaObject,
        "object": AdaObject,
        "exception": AdaObject,
        "generic-package-instantiation": AdaObject,
    }
    roles = {
        "func": AdaXRefRole(),
        "proc": AdaXRefRole(),
        "type": AdaXRefRole(),
        "ref": AdaXRefRole(),
        "mod": AdaXRefRole(),
        "rmlink": rmlink,
    }

    # TODO: Is this useful?
    initial_data: dict = {
        "objects": {},  # fullname -> docname, objtype
        "functions": {},  # fullname -> arity -> (targetname, docname)
        "procedures": {},  # fullname -> arity -> (targetname, docname)
        "packages": {},
        # packagename -> docname, synopsis, platform, deprecated
    }

    indices = [
        AdaPackageIndex,
    ]

    def clear_doc(self, docname: str) -> None:
        for fullname, obj in list(self.objects.items()):
            if obj.docname == docname:
                del self.objects[fullname]

    def _find_obj(
        self, env: BuildEnvironment, modname: str, name: str, objtype: str
    ) -> Tuple[str, str]:
        """
        Find a Ada object for "name", perhaps using the given module and/or
        classname.

        TODO: Handling references to overloaded functions.
        """
        # First try: try to find an object by that name (this is assuming that
        # the user used a fully qualified name)
        obj = self.objects.get(name, None)

        # Second try: try prefixing the object with the module name.
        if obj is None:
            fqn = f"{modname}.{name}"
            obj = self.objects.get(fqn)
            if obj is not None:
                name = fqn

        if obj:
            return name, obj.docname

        return ("", "")

    def resolve_xref(
        self, env: BuildEnvironment, fromdocname: str,
        builder: Builder,
        typ: str,
        target: str,
        node: addnodes.pending_xref,
        contnode: Element
    ) -> Union[Element, None]:

        # Resolve classwide type references to their base type
        real_target = target

        # We only handle the capitalized 'Class, because it is necessarily
        # formatted with a capital when the result is generated by Libadalang's
        # doc generator.
        if target.endswith("'Class"):
            real_target = target[:-6]

        modname = node.get("ada:package")
        name, obj = self._find_obj(env, modname, real_target, typ)
        if not obj:
            return None
        else:
            # If we correctly resolved the object and are able to make an
            # hyperlink, then use its relative name as a display name.

            # TODO: For some reason in old versions of Sphinx the contnode is
            # sometimes a `Text` node, which doesn't make any sense as far as I
            # understand. Ignore those cases:
            if not isinstance(contnode, nodes.Text):
                contnode[0] = nodes.Text(target.split(".")[-1])
            return make_refnode(
                builder, fromdocname, obj, name, contnode, name
            )

    def get_objects(self) -> Iterator[Tuple[str, str, str, str, str, int]]:
        for refname, obj in self.objects.items():
            yield refname, refname, obj.objtype, obj.docname, obj.node_id, 1

    @property
    def objects(self) -> Dict[str, ObjectEntry]:
        return self.data.setdefault("objects", {})  # fullname -> ObjectEntry

    def note_object(
        self, name: str, objtype: str, node_id: str, location: Any = None
    ) -> None:
        """
        Note an ada object for cross references.
        """
        if name in self.objects:
            other = self.objects[name]
            logger.warning(
                __(
                    "duplicate object description of %s, "
                    "other instance in %s, use :noindex: for one of them"
                ),
                name,
                other.docname,
            )
        self.objects[name] = ObjectEntry(self.env.docname, node_id, objtype)


def setup(app: Sphinx) -> None:
    app.add_domain(AdaDomain)
