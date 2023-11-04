import shutil
from dataclasses import dataclass
import os
import re
from pathlib import Path
from typing import List, Set, Tuple
import xml.etree.ElementTree as ET
import zipfile
import urllib.request


ROOT = Path(__file__).absolute().parent


@dataclass
class Library:
    variables: Set[str]
    loopvariables: Set[str]
    calls: Set[str]
    # if true, accumulate everything found to library
    teaching: bool


# aggregate full report here
full_report = {}


def do_import(fnames: str):
    target_dir = get_app_local_dir()
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)
    for f in fnames:
        if f.startswith("http"):
            lastpart = f.split("/")[-1]
            print(lastpart)
            if not lastpart.endswith(".zip"):
                lastpart = "downloaded.zip"
            tfile = Path(target_dir) / lastpart
            print("Fething:", f, "->", tfile)
            urllib.request.urlretrieve(f, tfile)
        elif f.endswith(".zip"):
            print("Copying:", f, "->", target_dir)
            shutil.copy(f, target_dir)
        else:
            print("Not a zip file:", f)


def get_app_local_dir():
    local_app_data = os.getenv("LOCALAPPDATA")
    if local_app_data:
        return Path(local_app_data) / "anyerplint"
    return None


def do_check(libs: List[str], targets: List[str], teaching: bool) -> int:
    lib_vars = Library(
        variables=set(), calls=set(), teaching=teaching, loopvariables=set()
    )

    # always feed the "standard library"

    stdlib = ROOT / "reflib"
    feed_lib(lib_vars, stdlib)

    local_app_data = get_app_local_dir()
    if local_app_data:
        feed_lib(stdlib, Path(local_app_data) / "anyerplint")

    for lib in libs:
        feed_lib(lib_vars, lib)

    has_errors = False
    for target in targets:
        if os.path.isdir(target):
            errs, count = check_dir(lib_vars, Path(target))
        else:
            assert target.lower().endswith(".xml")
            r = parse_file(target, teaching)
            errs = report(lib_vars, target, r)
        if errs:
            has_errors = True

    if lib_vars.teaching:
        print("Writing found function to:")

        def write_file(fname, lines):
            print("  - ", fname)
            f = open(fname, "wb")
            for line in lines:
                try:
                    enc = line.strip().encode()
                except UnicodeEncodeError:
                    # skip bad lines for now
                    ...
                f.write(enc)
                f.write(b"\n")

        functions_file = stdlib / "builtin_calls.txt"
        write_file(functions_file, sorted(lib_vars.calls))

        vars_file = stdlib / "builtin_vars.txt"
        write_file(vars_file, sorted(lib_vars.variables))

        loopvars_file = stdlib / "builtin_loopvars.txt"
        write_file(loopvars_file, sorted(lib_vars.loopvariables))

    if has_errors:
        print("Errors found: >")
        rep = sorted((k, v) for (k, v) in full_report.items())
        for line in rep:
            print("  ", line[0], ";", line[1])


def feed_lib(lib_vars: Library, libdir: str):
    def feed_set(set: Set, fobj):
        set.update(fobj.readlines())

    def visit_file(fname: str, fobj):
        if fname.endswith("_calls.txt"):
            feed_set(lib_vars.calls, fobj)
        elif fname.endswith("_vars.txt"):
            feed_set(lib_vars.variables, fobj)
        elif fname.endswith("_loopvars.txt"):
            feed_set(lib_vars.loopvariables, fobj)

    pth = Path(libdir)
    if not pth.exists():
        return

    # files on file system
    for p in pth.glob("*_*.txt"):
        visit_file(str(p), p.open())

    # files in all the zip files
    for f in pth.glob("*.zip"):
        zf = zipfile.ZipFile(f, "r")
        for zn in zf.namelist():
            visit_file(zn, zf.open(zn, "r"))


def check_dir(lib_vars: Library, root: Path) -> Tuple[bool, int]:
    errs = False
    counter = 0
    for f in root.glob("**/*.xml"):
        counter += 1
        try:
            r = parse_file(f, lib_vars.teaching)
        except ET.ParseError as e:
            print(str(f) + ": XmlError " + str(e))
            continue
        except PermissionError as e:
            print(f"{f}: PermissionError " + str(e))
        errcount = report(lib_vars, f, r)
        if errcount:
            errs = True
            full_report[str(f)] = errcount

    return errs, counter


@dataclass
class Parsed:
    var_decl: Set[str]
    var_used: Set[str]
    calls: Set[str]
    syntax_errors: List[str]
    loop_var_decl: Set[str]
    loop_var_use: Set[str]


def report(lib_vars: Library, fname: str, p: Parsed) -> int:
    undeclared_vars = p.var_used - p.var_decl
    undeclared_vars.difference_update(lib_vars.variables)
    unknown_loop_variables = p.loop_var_use - p.loop_var_decl
    unknown_loop_variables.difference_update(lib_vars.loopvariables)

    if lib_vars.teaching:
        lib_vars.calls.update(p.calls)
        lib_vars.variables.update(undeclared_vars)
        lib_vars.loopvariables.update(unknown_loop_variables)

    errors = []

    if undeclared_vars:
        errors.append("Unknown variables: [" + ", ".join(undeclared_vars) + "]")

    unknown_calls = p.calls
    unknown_calls.difference_update(lib_vars.calls)

    if unknown_calls:
        errors.append(
            "Unknown calls:\n" + "\n".join("    - " + c for c in sorted(unknown_calls))
        )

    if p.syntax_errors:
        errors.append(
            "Syntax errors:\n" + "\n".join("    - " + c for c in p.syntax_errors)
        )

    if unknown_loop_variables:
        errors.append("Unknown loop variables: " + ", ".join(unknown_loop_variables))

    if errors:
        print(str(fname) + ":")
        for err in errors:
            print("  " + err)

    return len(errors)


key_params = {
    "bw_file_functions": "command",
    "bw_table_method": "command",
    "bw_string_functions": "operation",
    "bw_ws_function": "method",
}


def summarize_call(node):
    name = node.attrib["name"].lower()
    full = name
    params = {p.attrib["name"]: p.text for p in node.iter("parameter")}
    if name in key_params:
        full += "." + params.get(key_params[name], "UNK")

    return full + " - " + ",".join(sorted(params))


def summarize_tag(node):
    if node.attrib:
        at = " " + " ".join(sorted(node.attrib.keys()))
    else:
        at = ""

    full = "<" + node.tag + at + ">"
    return full


def brace_check(s: bytes):
    stack: List[str] = []
    lines = s.splitlines()
    closers = {"{": "}", "[": "]", "(": ")"}
    lnum = 0
    errors = []
    for l in lines:
        lnum += 1
        cnum = 0
        flush_stack = False
        in_quote = False
        for ch in l:
            ch_as_string = chr(ch)
            cnum += 1
            if ch == ord('"'):
                # only care about quotes if we are in some nested operation already, top level quotes are not considered
                if stack:
                    in_quote = not in_quote

            if in_quote:
                continue

            if ch in b"{([":
                stack.append((ch_as_string, lnum))
            if ch in b"})]":
                try:
                    from_stack, _ = stack.pop()
                except IndexError:
                    errors.append(
                        f"Too many closing braces at line {lnum}, looking at '{ch_as_string}' on col {cnum}: ==> {l[cnum-10:cnum].decode()} <==: {l.decode().strip()}"
                    )
                    flush_stack = True
                    break

                expected = closers[from_stack]
                if expected != ch_as_string:
                    errors.append(
                        f"Expected brace {expected}, got {ch_as_string} at line {lnum} col {cnum}: {l.decode().strip()}"
                    )
                    flush_stack = True
                    break
        if flush_stack:
            stack = []
    if stack:
        errors.append(
            f"File ended with mismatched braces, remaining in stack (char, linenum): {stack}"
        )
    return errors


# xxx not really needed due to new logic
MAGIC_VAR_NAMES = set(["error", "return", "response", "invoice.i"])


def describe_node(n):
    return "<" + n.tag + str(n.attrib) + ">"


def describe_jump(n):
    params = sorted(
        child.attrib.get("name", "NONAME").strip() for child in n.iter("parameter")
    )
    target = str(n.attrib["jumpToXPath"])
    prefix = "//section[@name='"
    if target.startswith(prefix):
        target = "..." + target[len(prefix) :].rstrip("]'")

    desc = (
        "Jump "
        + n.attrib.get("jumpToXmlFile", "NOFILE")
        + " -- "
        + target
        + " -- "
        + " ".join(params)
    )
    return desc.strip()


def replace_commented_xml_with_empty_lines(xml_string):
    # Define a regular expression pattern to match XML comments
    comment_pattern = b"<!--(.*?)-->"

    # Use re.sub to replace the matched comments with an equivalent number of empty lines
    def replace(match):
        comment = match.group(0)
        empty_lines = b"\n" * comment.count(b"\n")
        return empty_lines

    result = re.sub(comment_pattern, replace, xml_string, flags=re.DOTALL)
    return result


def parse_file(fname: str, teaching: bool = False):
    tree = ET.parse(fname)
    cont = ET.tostring(tree.getroot())
    vardecl = set(v.attrib.get("name", "unknown_var") for v in tree.iter("variable"))
    propaccess = set(
        (m.group(1).decode(), m.group(2).decode())
        for m in re.finditer(b"([a-zA-Z.]+),(\w+)", cont)
    )
    # print("prop", propaccess)
    varuse = set(n for k, n in propaccess if k == "v")
    # varuse = set(m.group(1).decode().lower() for m in re.finditer(b"v,(\w+)", cont))
    expruse = set("f," + n for k, n in propaccess if k == "f")

    # what to do with p params?
    otherpropaccess = set(k for k, v in propaccess if k.lower() not in ["v", "f", "p"])
    otherpropaccess.difference_update(MAGIC_VAR_NAMES)
    calls = set(summarize_call(v) for v in tree.iter("builtInMethodParameterList"))
    alltags = set(summarize_tag(t) for t in tree.iter())
    loop_data_source_attribs = set(n.attrib.get("loopDataSource") for n in tree.iter())
    loop_data_sources = set(
        ls.split(";")[0].lower() for ls in loop_data_source_attribs if ls
    )
    return_names = set(
        n.attrib.get("name", "UNNAMED_RETURN").lower() for n in tree.iter("return")
    )
    loop_data_sources.update(return_names)

    jumps = (
        describe_jump(n) for n in tree.iter("method") if n.attrib.get("jumpToXmlFile")
    )

    calls.update(expruse)
    calls.update(alltags)
    calls.update(jumps)
    errors = []

    if not teaching:
        raw_cont = open(fname, "rb").read()
        parsed_cont = replace_commented_xml_with_empty_lines(raw_cont)

        errors.extend(brace_check(parsed_cont))

        no_text_allowed_tags = [
            "sections",
            "section",
            "method",
            "output",
            "outputCommands",
            "builtInMethodParameterList",
        ]
        for notext in no_text_allowed_tags:
            nodes = tree.iter(notext)
            for n in nodes:
                if n and n.text.strip():
                    errors.append(
                        "Node should not contain text: "
                        + describe_node(n)
                        + " -- "
                        + n.text.strip()
                    )

    return Parsed(
        var_decl=vardecl,
        var_used=varuse,
        calls=calls,
        syntax_errors=errors,
        loop_var_decl=loop_data_sources,
        loop_var_use=otherpropaccess,
    )
