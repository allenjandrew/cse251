"""
Course: CSE 251, week 14
File: functions.py
Author: <your name>

Instructions:

Depth First Search
https://www.youtube.com/watch?v=9RHO6jU--GU

Breadth First Search
https://www.youtube.com/watch?v=86g8jAQug04


Requesting a family from the server:
request = Request_thread(f'{TOP_API_URL}/family/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 6128784944, 
    'husband_id': 2367673859,        # use with the Person API
    'wife_id': 2373686152,           # use with the Person API
    'children': [2380738417, 2185423094, 2192483455]    # use with the Person API
}

Requesting an individual from the server:
request = Request_thread(f'{TOP_API_URL}/person/{id}')
request.start()
request.join()

Example JSON returned from the server
{
    'id': 2373686152, 
    'name': 'Stella', 
    'birth': '9-3-1846', 
    'parent_id': 5428641880,   # use with the Family API
    'family_id': 6128784944    # use with the Family API
}

You will lose 10% if you don't detail your part 1 and part 2 code below

Describe how to speed up part 1

    The basic flow of part 1 is to get the details for a family and add it to the tree, then grab details for the children and add them to the tree, then grab details for the parents and add them to the tree and **call the depth_fs_pedigree() function recursively** (first for the dad's family, then mom's). I create threads for each server request and for each recursive function call. The biggest issue I had while writing this program is that my computer wasn't hosting the server correctly (or something) so I was getting errors relating to 'connection reset by peer'. I implemented a semaphore that allows for five families to be processed at a time, and that helped reduce how often that error would show up when I ran my code. I can only hope that my code will work with the grader's server.


Describe how to speed up part 2

    To do part 2, I implemented a queue where I put families needing to be processed. One by one I take them off the queue and process them the same way as in part 1. Again, every time the function is run it uses threading. Instead of using recursion to loop through, the function uses while loops that make sure everything runs correctly until the whole tree is processed.


Extra (Optional) 10% Bonus to speed up part 3

<Add your comments here>

"""
from common import *
import queue


# -----------------------------------------------------------------------------
def depth_fs_pedigree(family_id, tree: Tree, sema_4=None):
    # KEEP this function even if you don't implement it
    # TODO - implement Depth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    if not sema_4:
        sema_4 = threading.Semaphore(5)

    # If this family is already accounted for, let's skip it
    if tree.does_family_exist(family_id) or not family_id:
        return

    # Send a request to get family details
    fam_req = Request_thread(f"{TOP_API_URL}/family/{family_id}")
    fam_req.start()
    fam_req.join()

    # Add this family to the tree
    the_fam = Family(fam_req.get_response())
    tree.add_family(the_fam)

    # Get parent ids
    daddy_i = the_fam.get_husband()
    momma_i = the_fam.get_wife()

    sema_4.acquire()

    # Send requests for the parents
    daddy_r = Request_thread(f"{TOP_API_URL}/person/{daddy_i}")
    daddy_r.start()
    momma_r = Request_thread(f"{TOP_API_URL}/person/{momma_i}")
    momma_r.start()

    # Send a request for each child's details
    kid_reqs = []

    for kid_id in the_fam.get_children():
        if not tree.does_person_exist(kid_id):
            kid_reqs.append(Request_thread(f"{TOP_API_URL}/person/{kid_id}"))

    # Start and join child requests
    for r in kid_reqs:
        r.start()
    for r in kid_reqs:
        r.join()

    # Do stuff with child responses
    for r in kid_reqs:
        if not r.get_response():
            continue

        kid = Person(r.get_response())

        # If this person isn't already on the tree, add them
        if not tree.does_person_exist(kid.get_id()):
            tree.add_person(kid)

    # Wait for mom & dad requests
    daddy_r.join()
    momma_r.join()

    sema_4.release()

    # This is where we'll store our threads
    fam_ts = []

    if daddy_r.get_response():
        daddy_p = Person(daddy_r.get_response())

        # If this person isn't already on the tree, add them
        if not tree.does_person_exist(daddy_i):
            tree.add_person(daddy_p)

        # depth_fs_pedigree(daddy_p.get_parentid(), tree)

        # Add a request for this person's family to our threads list
        daddy_t = threading.Thread(
            target=depth_fs_pedigree, args=(daddy_p.get_parentid(), tree, sema_4)
        )

        daddy_t.start()
        fam_ts.append(daddy_t)

    if momma_r.get_response():
        momma_p = Person(momma_r.get_response())

        # If this person isn't already on the tree, add them
        if not tree.does_person_exist(momma_i):
            tree.add_person(momma_p)

        # depth_fs_pedigree(momma_p.get_parentid(), tree)

        # Add a request for this person's family to our threads list
        momma_t = threading.Thread(
            target=depth_fs_pedigree, args=(momma_p.get_parentid(), tree, sema_4)
        )

        momma_t.start()
        fam_ts.append(momma_t)

    for t in fam_ts:
        t.join()


# -----------------------------------------------------------------------------
def breadth_fs_pedigree(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    fam_shopper = queue.Queue()
    fam_shopper.put(family_id)

    def _helper(fid):
        if tree.does_family_exist(fid) or not fid:
            return

        # Send a request to get family details
        fam_req = Request_thread(f"{TOP_API_URL}/family/{fid}")
        fam_req.start()
        fam_req.join()

        # Add this family to the tree
        the_fam = Family(fam_req.get_response())
        tree.add_family(the_fam)

        # Get parent ids
        daddy_i = the_fam.get_husband()
        momma_i = the_fam.get_wife()

        # sema_4.acquire()

        # Send requests for the parents
        daddy_r = Request_thread(f"{TOP_API_URL}/person/{daddy_i}")
        daddy_r.start()
        momma_r = Request_thread(f"{TOP_API_URL}/person/{momma_i}")
        momma_r.start()

        # Send a request for each child's details
        kid_reqs = []

        for kid_id in the_fam.get_children():
            if not tree.does_person_exist(kid_id):
                kid_reqs.append(Request_thread(f"{TOP_API_URL}/person/{kid_id}"))

        # Start and join child requests
        for r in kid_reqs:
            r.start()
        for r in kid_reqs:
            r.join()

        # Do stuff with child responses
        for r in kid_reqs:
            if not r.get_response():
                continue

            kid = Person(r.get_response())

            # If this person isn't already on the tree, add them
            if not tree.does_person_exist(kid.get_id()):
                tree.add_person(kid)

        # Wait for mom & dad requests
        daddy_r.join()
        momma_r.join()

        # sema_4.release()

        if daddy_r.get_response():
            daddy_p = Person(daddy_r.get_response())

            # If this person isn't already on the tree, add them
            if not tree.does_person_exist(daddy_i):
                tree.add_person(daddy_p)

            # Add a request for this person's family to our threads list
            fam_shopper.put(daddy_p.get_parentid())

        if momma_r.get_response():
            momma_p = Person(momma_r.get_response())

            # If this person isn't already on the tree, add them
            if not tree.does_person_exist(momma_i):
                tree.add_person(momma_p)

            # Add a request for this person's family to our threads list
            fam_shopper.put(momma_p.get_parentid())

    while not fam_shopper.empty():
        count = 0
        threads = []

        while count < 20 and not fam_shopper.empty():
            count += 1
            fam_id_to_process = fam_shopper.get()
            t = threading.Thread(target=_helper, args=(fam_id_to_process,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()


# -----------------------------------------------------------------------------
def breadth_fs_pedigree_limit5(family_id, tree):
    # KEEP this function even if you don't implement it
    # TODO - implement breadth first retrieval
    #      - Limit number of concurrent connections to the FS server to 5
    # TODO - Printing out people and families that are retrieved from the server will help debugging

    pass
