import github3
import pytest
from tests.utils import BaseCase, load
from unittest import TestCase


class TestEvent(BaseCase):
    def __init__(self, methodName='runTest'):
        super(TestEvent, self).__init__(methodName)
        self.ev = github3.events.Event(load('event'))
        self.o = load('org')

    def setUp(self):
        super(TestEvent, self).setUp()
        self.ev = github3.events.Event(self.ev.as_dict())

    def test_equality(self):
        e = github3.events.Event(load('event'))
        assert self.ev == e
        e._uniq = 1
        assert self.ev != e

    def test_org(self):
        json = self.ev.as_dict().copy()
        json['org'] = self.o
        ev = github3.events.Event(json)
        assert isinstance(ev.org, github3.orgs.Organization)

    def test_repr(self):
        assert repr(self.ev).startswith('<Event')

    def test_list_types(self):
        Event, handlers = (github3.events.Event,
                           github3.events._payload_handlers)
        assert Event.list_types() == sorted(handlers.keys())


class TestPayloadHandlers(TestCase):
    def test_commitcomment(self):
        comment = {'comment': load('repo_comment')}
        comment = github3.events._commitcomment(comment, None)
        assert isinstance(comment['comment'],
                          github3.repos.comment.RepoComment)

    def test_follow(self):
        f = {'target': load('user')}
        github3.events._follow(f, None)
        assert isinstance(f['target'], github3.users.User)

    def test_forkev(self):
        f = {'forkee': load('repo')}
        github3.events._forkev(f, None)
        assert isinstance(f['forkee'], github3.repos.Repository)

    def test_gist(self):
        g = {'gist': load('gist')}
        github3.events._gist(g, None)
        assert isinstance(g['gist'], github3.gists.Gist)

    def test_issuecomm(self):
        c = {'issue': load('issue'), 'comment': load('issue_comment')}
        github3.events._issuecomm(c, None)
        assert isinstance(c['issue'], github3.issues.Issue)
        assert isinstance(c['comment'], github3.issues.comment.IssueComment)

    def test_issueevent(self):
        c = {'issue': load('issue')}
        github3.events._issueevent(c, None)
        assert isinstance(c['issue'], github3.issues.Issue)

    def test_member(self):
        m = {'member': load('user')}
        github3.events._member(m, None)
        assert isinstance(m['member'], github3.users.User)

    def test_pullreqev(self):
        p = {'pull_request': load('pull')}
        github3.events._pullreqev(p, None)
        assert isinstance(p['pull_request'], github3.pulls.PullRequest)

    def test_pullreqcomm(self):
        p = {'comment': load('review_comment')}
        github3.events._pullreqcomm(p, None)
        assert isinstance(p['comment'], github3.pulls.ReviewComment)

    @pytest.mark.xfail
    def test_team(payload):
        t = {'team': load('team'), 'repo': load('repo'), 'user': load('user')}
        github3.events._team(t, None)
        assert isinstance(t['team'], github3.orgs.Team)
        assert isinstance(t['repo'], github3.repos.Repository)
