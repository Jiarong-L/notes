import graphviz
from xml.dom.minidom import parse


def parse_entry(entry):
    tpm_dict = {}
    tpm_dict["entry_id"] = entry.getAttribute('id')
    tpm_dict["entry_text"] = entry.getElementsByTagName('graphics').item(0).getAttribute('name')
    tpm_dict["contains"] = entry.getAttribute('name')
    tpm_dict["type"] = entry.getAttribute('type')
    tpm_dict["reaction"] = entry.getAttribute('reaction')
    tpm_dict["x"] = entry.getElementsByTagName('graphics').item(0).getAttribute('x')
    tpm_dict["y"] = entry.getElementsByTagName('graphics').item(0).getAttribute('y')
    tpm_dict["width"] = entry.getElementsByTagName('graphics').item(0).getAttribute('width')
    tpm_dict["height"] = entry.getElementsByTagName('graphics').item(0).getAttribute('height')
    tpm_dict["shape"] = entry.getElementsByTagName('graphics').item(0).getAttribute('type')
    tpm_dict["fgcolor"] = entry.getElementsByTagName('graphics').item(0).getAttribute('fgcolor')
    tpm_dict["bgcolor"] = entry.getElementsByTagName('graphics').item(0).getAttribute('bgcolor')
    tpm_dict["component"] = []
    for cc in entry.getElementsByTagName('component'):
        tpm_dict["component"].append(cc.getAttribute('id'))
    return tpm_dict




# def parse_relation(relation):
#     tpm_dict = {}
#     tpm_dict["entry1"] = relation.getAttribute('entry1')
#     tpm_dict["entry2"] = relation.getAttribute('entry2')
#     tpm_dict["PPrel"] = relation.getAttribute('PPrel')
#     tpm_dict["subtype_name"] = relation.getElementsByTagName('subtype').item(0).getAttribute('name')
#     tpm_dict["subtype_value"] = relation.getElementsByTagName('subtype').item(0).getAttribute('value')
#     return tpm_dict





dom = parse("/mnt/d/WSL_dir/workdir/KEGG/tt/ko00010.kgml").documentElement

for entry in dom.getElementsByTagName('entry'):
    tpm_dict = parse_entry(entry)



# for relation in dom.getElementsByTagName('relation'):
#     tpm_dict = parse_relation(relation)










