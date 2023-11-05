"""Top-level package for pygraid."""
import csv
import logging
import re

import importlib_resources

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

__author__ = "Florian Matter"
__email__ = "fmatter@mailbox.org"
__version__ = "0.0.1.dev"

data = importlib_resources.files(__name__) / "data"
BOUNDARY_TYPE = "clause_tag"
symbol_dic = {}

# "syn"

# other
# nc

# ln  NP-internal subconstituent occurring to the left of NP head
# rn  NP-internal subconstituent occurring to the right of NP head
# lv  subconstituent of verb complex occurring to the left of verbal head
# rv  subconstituent of verb complex occurring to the right of verbal head


for key in ["ref", "pred", "anim", "syn", "boundaries"]:
    symbol_dic[key] = {}
    with open(data / f"{key}.csv") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            symbol_dic[key][row["ID"]] = row["Description"]
symbol_dic["func"] = {
    "pred": "predicative function",
    "predex": "predicative function in existential / presentational constructions",
}

# symbol_dic looks like this:
# {
#     "ref": {
#         "np": "noun phrase",
#         "pro": "pronoun",
#         "0": "null argument",
#         "refl": "REFL or RECP pronoun",
#         "wpro": "weak pronoun",
#         "x": "non-referential",
#         "other": "other",
#     },
#     "pred": {
#         "v": "verb or verb complex",
#         "vother": "non-canonical verb-form",
#         "cop": "(overt) copular verb",
#         "aux": "auxiliary",
#     },
#     "anim": {
#         "1": "1st person referent(s)",
#         "2": "2nd person referent(s)",
#         "h": "human referent(s)",
#         "d": "anthropomorphized referent(s); the use of this symbol is optional",
#         "nh": "nonhuman referent(s)",
#     },
#     "syn": {
#         "s": "intransitive subject",
#         "a": "transitive subject",
#         "p": "transitive object",
#         "ncs": "non-canonical subject",
#         "g": "goal, recipient, addressee",
#         "l": "locative argument of verbs of location",
#         "obl": "oblique argument (no goal or locative)",
#         "p2": "secondary object",
#         "voc": "vocative",
#         "poss": "possessor",
#         "appos": "appositional",
#         "other": "other function",
#     },
#     "boundaries": {
#         "rc": "relative clause",
#         "cc": "complement clause",
#         "ac": "adverbial clause",
#         "ds": "direct speech",
#         "neg": "negative polarity",
#         "nc": "non-classifiable",
#     },
#     "func": {
#         "pred": "predicative function",
#         "predex": "predicative function in existential / presentational constructions",
#     },
# }

# morpheme separators
seps = ["-", "="]
# ...and how they translate to boundedness
bound_dic = {"=": "clitic", "-": "bound"}
# the main types of entries
type_dic = {"pred": "predicate", "ref": "referring expression"}
# what is a verb?
verb_list = ["v", "vother"]


def get_boundness(ann):
    """For a given annotation, establishes whether it is free, weak, a clitic or an affix."""
    for sep in seps:
        if sep in ann:
            return bound_dic[sep]
    if ann.startswith("w"):
        return "weak"
    return "free"


def is_empty(ann):
    if is_boundary(ann):
        return True
    if is_ref(ann) and "0" in ann:
        return True
    return False


def escape(l):
    """Escape a list"""
    return [re.escape(x) for x in l]


def join_group(x):
    # For composing regexes
    return "|".join(escape(x))


nouns = (
    r"(?P<ref>"
    + join_group(symbol_dic["ref"])
    + ")"
    + r"\.?"
    + "(?P<anim>"
    + join_group(symbol_dic["anim"])
    + r")?"
)
noun_pattern = re.compile(nouns)
ref_pattern = re.compile(
    rf'^(?P<formglosses>.*?_)?{nouns}\:(?P<syn>(dt_)?{join_group(symbol_dic["syn"])}|dt)(?P<funcglosses>_.*?)?$'
)  #

# remove auxiliary from the pred dict temporarily
temp = symbol_dic["pred"].pop("aux")
pred = (
    r"^(?P<glosses>.*?_)?"
    + "(?:(?P<pred>"
    + join_group(symbol_dic["pred"])
    + ")"
    + ":"
    + "(?P<func>"
    + join_group(["pred", "predex"])
    + ")|(?P<aux>aux))"
)
pred_pattern = re.compile(pred)
symbol_dic["pred"]["aux"] = temp

boundaries = (
    r"^(?P<btype>##|#|%)(?P<type>" + join_group(symbol_dic["boundaries"]) + ")?"
)
boundary_pattern = re.compile(boundaries)


def is_boundary(ann):
    res = [
        m.groupdict()
        for m in boundary_pattern.finditer(ann.strip(rf"({'|'.join(seps)})"))
    ]
    if not res:
        return False
    return True


def resolve_ref(hit, bound="free"):
    # print(f"resolving ref {hit}")
    # res = ref_pattern.findall()
    res = [
        m.groupdict() for m in ref_pattern.finditer(hit.strip(rf"({'|'.join(seps)})"))
    ]
    # print(ref_pattern)
    # print(res)
    if len(res) == 1:
        res = res[0]
        res["anim"] = res["anim"] or "nh"
        res["type"] = "ref"
        for fill in ["formglosses", "funcglosses"]:
            if not res[fill]:
                res[fill] = ""
        res["form"] = get_boundness(hit)
        return res
    elif len(res) > 1:
        log.error(f"This looks like more than one reference: {res}")
        return None
    return None


def resolve_pred(hit, bound="free"):
    # print(f"Resolving pred {hit}")
    if "pred_" in hit or "predex_" in hit:
        ann, funcglosses = hit.rsplit("_", 1)
    else:
        ann = hit
        funcglosses = ""
    if "_" in ann:
        glosses, ann = ann.split("_", 1)
    else:
        glosses = ""
    kind, pred = ann.rsplit(":", 1)  # np:l:pred needs to be np:l, pred
    if kind not in ["other", "adp", "nc", "v", "vother"]:
        ref_dict = resolve_ref(kind)
        if not ref_dict:
            ref_dict = resolve_ref(kind + ":s")
    else:
        ref_dict = None
    # print(ref_dict)
    if ref_dict:
        del ref_dict["type"]
        del ref_dict["ref"]
        res_dict = {
            **{"func": pred, "pred": kind, "type": "pred", "form": bound},
            **ref_dict,
        }
        # print(res_dict)
        return res_dict
    if kind in verb_list:
        return {
            "func": pred,
            "pred": kind,
            "type": "pred",
            "form": bound,
            "formtags": glosses,
            "functags": funcglosses,
        }
    if kind == "np":
        return {
            "pred": "np",
            "anim": "nh",
            "type": "pred",
            "form": bound,
            "formtags": glosses,
            "func": pred,
            "functags": funcglosses,
        }
    if kind == "other":
        return {
            "pred": "other",
            "type": "pred",
            "form": bound,
            "formtags": glosses,
            "func": pred,
            "functags": funcglosses,
        }
    if kind == "adp":
        return {
            "pred": "adp",
            "type": "pred",
            "form": bound,
            "formtags": glosses,
            "func": pred,
            "functags": funcglosses,
        }
    print("now what")
    print(kind)
    exit()


boundary_dict = {"##": "main_clause", "#": "subr_clause", "%": "subr_end"}


def resolve_boundary(hit):
    good = False
    for key, value in boundary_dict.items():
        if key in hit and not good:
            kind = value
            good = True
    if not good:
        raise ValueError(hit)
    b_dict = {"type": kind}
    data = hit.strip("#")
    if data:
        if "_" in data:
            b_dict["ds"], data = data.split("_")
        if ":" in data:
            data, b_dict["syn"] = data.split(":")
        if "." in data:
            data, b_dict["polarity"] = data.split(".")
        else:
            b_dict["polarity"] = "aff"
    b_dict[BOUNDARY_TYPE] = data
    return b_dict


def ann_label(data):
    out_str = [data.pop("form")]
    typelabel = "(" + type_dic[data.pop("type")] + ")"
    for k, v in data.items():
        out_str.append(symbol_dic[k][v])
    out_str.append(typelabel)
    return ", ".join(out_str[0:-1]) + " " + out_str[-1]


def is_ref(ann):
    # print(f"Checking if {ann} is a ref")
    # print(ref_pattern)
    # print(ref_pattern.findall(ann))
    if ref_pattern.findall(ann):
        return True
    return False


def is_referential(ann):
    if is_ref(ann):
        return True
    if is_boundary(ann):
        res = resolve_boundary(ann)
        if res.get("syn") in ["s", "a", "p"]:
            return True
        else:
            return False
    items = list(filter(None, re.split(rf"({'|'.join(seps)})", ann)))
    for item in items:
        if is_ref(item):
            return True
    return False


def is_pred(ann):
    if ":pred" in ann or ":predex" in ann:
        return True
    return False


def add_seps(item, items, i):
    if i + 1 < len(items) and items[i + 1] in seps:
        item += items[i + 1]
    if i - 1 >= 0 and items[i - 1] in seps:
        item = items[i - 1] + item
    return item


def iter_list(annlist):
    for x in annlist:
        for y in parse_graid_item(x):
            yield y


def parse_graid_item(ann):
    # print(f"Parsing annotation {ann}")
    clause_id = 1
    parsed_items = []
    items = list(filter(None, re.split(rf"({'|'.join(seps)})", ann)))
    for i, item in enumerate(items):
        if item in seps:
            continue
        if is_pred(item):
            parsed_items.append(resolve_pred(item))
        elif is_ref(item):
            item = add_seps(item, items, i)
            parsed_items.append(resolve_ref(item))
        elif is_boundary(item):
            clause_id += 1
            parsed_items.append(resolve_boundary(item))
        else:
            if "_" in item:
                glosses, item = item.split("_", 1)
            else:
                glosses = ""
            if "_" in item:
                item, funcglosses = item.split("_", 1)
            else:
                funcglosses = ""
            item = add_seps(item, items, i)
            item_dict = {"formtags": glosses, "functags": funcglosses, "form": "free"}
            if "adp" in item:
                parsed_items.append(
                    {
                        **item_dict,
                        **{
                            "type": "other",
                            "func": "adp",
                        },
                    }
                )
            elif item == "vother":
                parsed_items.append(
                    {
                        **item_dict,
                        **{
                            "func": "vother",
                            "type": "other",
                        },
                    }
                )
            elif item == "cop":
                parsed_items.append(
                    {
                        **item_dict,
                        **{
                            "type": "other",
                            "func": "cop",
                        },
                    }
                )
            elif "aux" in item:
                parsed_items.append(
                    {
                        **item_dict,
                        **{
                            "type": "other",
                            "func": "aux",
                        },
                    }
                )
            elif item == "other":
                parsed_items.append(
                    {
                        **item_dict,
                        **{
                            "type": "other",
                        },
                    }
                )
            elif item == "nc":
                parsed_items.append({**item_dict, **{"type": "nc"}})
            elif item[0] == "x":
                parsed_items.append({**item_dict, **{"type": "other", "ref": "np"}})
            else:
                log.warning(f"Unparsable annotation: {item}")
    return parsed_items


def parse_annotation(ann, sep=" ", mode="linear"):
    parsed = {"pre": [], "data": [], "post": []}
    main = False
    for x in ann.split(sep):
        if not main:
            position = "pre"
        else:
            position = "post"
        res = parse_graid_item(x)
        if res:
            for item in res:
                if (
                    item.get("ref", "np") == "0"
                    or item.get("type", "unimportant") in boundary_dict.values()
                ):
                    parsed[position].append(item)
                else:
                    parsed["data"].append(item)
                    main = True
    if len(parsed["data"]) == 0:
        parsed["data"] = [{}]
    if mode == "linear":
        return parsed["pre"] + parsed["data"] + parsed["post"]
    return parsed


def to_string(ann):
    if not ann:
        return ""
    if isinstance(ann, dict):
        res = [ann["type"]]
        for key, values in symbol_dic.items():
            if key in ann:
                if ann[key] in values:
                    res.append(values[ann[key]])
                elif ann[key] == "adp":
                    return "adposition"
                elif ann[key] == "aux":
                    return "auxiliary"
                elif ann[key] == "cop":
                    return "copula"
                elif ann[key] == "vother":
                    return "non-finite verb"
                else:
                    raise ValueError(ann[key])
        return "; ".join(res)
    elif isinstance(ann, str):
        return to_string(parse_annotation(ann))
    elif isinstance(ann, list):
        return "\n".join([to_string(x) for x in ann])
    return ""
