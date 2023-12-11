from common import *


def depth_fs_pedigree(family_id, tree):
    """
    The `depth_fs_pedigree` function is meant to be recursive so we need to add
    a stop for when we reach the end of a branch.
    """
    if family_id == None:
        return

    # Get the requested family; we gave you this code already.
    req_family = Request_thread(f"{TOP_API_URL}/family/{family_id}")
    req_family.start()
    req_family.join()

    # Make sure to add this family to the tree you're building; modified from what we did last time.
    new_family = Family(req_family.get_response())
    tree.add_family(new_family)

    husband = None
    wife = None

    # Get husband details:
    husband_id = new_family.get_husband()
    req_person1 = Request_thread(f"{TOP_API_URL}/person/{husband_id}")
    req_person1.start()

    # Get wife details:
    wife_id = new_family.get_wife()
    req_person2 = Request_thread(f"{TOP_API_URL}/person/{wife_id}")
    req_person2.start()

    # Retrieve the children:
    children = []
    for child_id in new_family.get_children():
        # Don't request a person if that person is in the tree already.
        if not tree.does_person_exist(child_id):
            # Request the next childs data...
            pass

    # Wait on the children threads...
    pass

    # Convert the children data into a Person object.
    pass

    # Wait on the husband and wife details threads...
    pass

    # Convert the parents data into Person objects.
    husband = Person(req_person1.get_response())
    wife = Person(req_person2.get_response())

    # Go up the path of the husband's parents:
    husband_thread = None
    if husband != None:
        pass

    # Go up the path of the wife's parents:
    wife_thread = None
    if wife != None:
        pass

    # Wait on the husband and wife parents threads....
    pass
