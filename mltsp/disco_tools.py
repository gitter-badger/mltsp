from disco.ddfs import DDFS
import ntpath
import os

def push_by_tag(file_paths, tag=None):
    '''
    '''
    ddfs = DDFS()
    if tag is None:
        for file_path in file_paths:
            tag = os.path.splitext(ntpath.basename(file_path))[0]
            try:
                ddfs.push(tag, [file_path])
            except IOError:
                print("Invalid file path specified.")
    else:
        try:
            ddfs.push(tag, file_paths)
        except IOError:
            print("Invalid file path specified.")


def push_all_objects(file_paths, tags=None):
    '''
    '''
    if tags is not None:
        if len(file_paths) == len(tags):
            tags_to_fname_list_dict = {}
            for i in range(len(file_paths)):
                if tags[i] not in tags_to_fname_list_dict:
                    tags_to_fname_list_dict[tags[i]] = [file_paths[i]]
                else:
                    tags_to_fname_list_dict[tags[i]].append(file_paths[i])
            for tag_name in list(tags_to_fname_list_dict.keys()):
                push_by_tag(
                    file_paths=tags_to_fname_list_dict[tag_name],
                    tag=tag_name)
        else:
            raise ValueError(
                "file_paths and tags lists are not of the same length!")
    else:
        push_by_tag(file_paths)
    print("All files pushed to DDFS")


def headerfile_to_fname_dict(headerfile_path):
    '''Parses headerfile and returns dict with key=fname,
    value=dict of attributes (class/meta feats)
    '''
    with open(headerfile_path) as f:
        all_lines = f.readlines()
    column_titles = all_lines[0].strip().split(",")
    dict_of_dicts = {"column_titles": column_titles[:]}
    for line in all_lines[1:]:
        els = line.strip().split(",")
        if len(els) <= 1:
            continue
        this_dict = {}
        if len(els) == len(column_titles):
            for i in range(1, len(els)):
                this_dict[column_titles[i]] = els[i]
            dict_of_dicts[els[0]] = this_dict
            dict_of_dicts[els[0].replace(".", "_")] = this_dict
            dict_of_dicts[os.path.splitext(els[0])[0]] = this_dict
        else:
            print(("Column titles (" + str(column_titles) +
                   ") and line elements (" + str(els) +
                   ") not of the same length.. "))

    return dict_of_dicts


def url_to_class_and_meta_feats_dict(url, big_dict):
    """DDFS URL to class name and meta feats dict"""
    fname = url.split("/")[-1].split("$")[0]
    if fname in big_dict:
        return big_dict[fname]
    elif fname.split("_")[0] in big_dict:
        return big_dict[fname.split("_")[0]]
    elif os.path.splitext(fname)[0] in big_dict:
        return big_dict[os.path.splitext(fname)[0]]
    else:
        raise KeyError("{} not in fname_class_dict.".format(fname))


def list_by_tag(tag):
    """List all blobs pushed to DDFS by tag"""
    ddfs = DDFS()
    return ddfs.list(tag)


def delete_pushed_objects(tag_prefix=""):
    '''
    Deletes all tags in DDFS, thus orphaning all blobs and making them
    subject to eventual removal by the garbage collector.
    '''
    ddfs = DDFS()
    for tag in ddfs.list(tag_prefix):
        ddfs.delete(tag)
