def merge_collection(site, collection):
    """
        add items from collection (type MongoClient[<db_name>][<collection_name>])
        to site (type dict)

        collection's "find" method returns a cursor

        iteration over a cursor yields doc objects (type dict)

        this is a "bottom up" merge, attributes already already in "site" override attributes
        extracted from "collection"

        for each doc in collection:
            remove attribute "_id" from doc
            if doc["type"] is "constants" :
                for each attribute in doc except "type":
                    if there is no attribute with that name in site:
                        add attribute to site
            elif doc["type"] is "account":
                if doc["uri"] is not in site["Accounts"]:
                    add attribute doc["uri"] with value {} to site["Accounts"]
                for each attribute in doc except "type" and "uri":
                    if attribute is not in site["Accounts"][doc["uri"]]:
                        add attribute to site["Accounts"][doc["uri"]]
            elif doc["type"] is "domain":
                if doc["uri"] is not in site["Domains"]:
                    add attribute doc["uri"] with value {} to site["Domains"]
                for each attribute in doc except "type" and "uri":
                    if attribute is not in site["Domains"][doc["uri"]]:
                        add attribute to site["Domains"][doc["uri"]]
            elif doc["type"] is "user":
                if doc["uri"] is not in site["Users"]:
                    add attribute doc["uri"] with value {} to site["Users"]
                for each attribute in doc except "type" and "uri":
                    if attribute is not in site["Users"][doc["uri"]]:
                        add attribute to site["Users"][doc["uri"]]

    :param dict1: dictionary with initial values, which will contain final merged values
    :param dict2: dictionary with values to merge into dict1
    """
    for doc in collection.find():
        del doc["_id"]
        if doc["type"] == "constants":
            del doc["type"]
            for key in doc:
                if key not in site:
                    site[key] = doc[key]
        elif doc["type"] == "account":
            attr_name = doc["uri"]
            dict_name = "Accounts"
            del doc["uri"]
            del doc["type"]
            merge_attrs(attr_name, dict_name, doc, site)
        elif doc["type"] == "domain":
            attr_name = doc["domain"]
            dict_name = "Domains"
            del doc["domain"]
            del doc["type"]
            merge_attrs(attr_name, dict_name, doc, site)
        elif doc["type"] == "user":
            attr_name = doc["name"]
            dict_name = "Users"
            del doc["name"]
            del doc["type"]
            merge_attrs(attr_name, dict_name, doc, site)


def merge_attrs(attr_name, dict_name, doc, site):
    if dict_name not in site:
        site[dict_name] = {}
    if attr_name not in site[dict_name]:
        site[dict_name][attr_name] = doc
    else:
        for key in doc:
            if key not in site[dict_name][attr_name]:
                site[dict_name][attr_name][key] = doc[key]


