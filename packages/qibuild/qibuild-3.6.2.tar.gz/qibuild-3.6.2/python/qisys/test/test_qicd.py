import os

import qicd

def get_best_match(worktree, token):
    # qicd.find_best_match returns an absolute path,
    # this is used to simplify assertions
    res = qicd.find_best_match(worktree, token)
    if res:
        return os.path.relpath(res, worktree.root)

def test_matches_closest(worktree):
    worktree.create_project("apps/behaviors")
    worktree.create_project("behavior")
    worktree.create_project("chuck")
    worktree.create_project("core/naoqicore")
    worktree.create_project("gui/choregraphe")
    worktree.create_project("sdk/libnaoqi")
    assert get_best_match(worktree, "behaviors") == "apps/behaviors"
    assert get_best_match(worktree, "naoqic") == "core/naoqicore"
    assert get_best_match(worktree, "lnaoqi") == "sdk/libnaoqi"
    assert get_best_match(worktree, "chor") == "gui/choregraphe"
