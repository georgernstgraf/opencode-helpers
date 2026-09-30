"""Hermetic tests for skills/repo-sync/scripts/repo-sync.sh.

The script is run as a subprocess against a throwaway HOME containing a
fixture tree: local bare repositories used as `origin` (so `git fetch` works
without a network) and a local `svnadmin` repository. Nothing here touches the
real ~/repos, the real remotes, or the network.
"""

import os
import shutil
import subprocess
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRIPT = os.path.join(ROOT, "skills", "repo-sync", "scripts", "repo-sync.sh")

CONFIG = """\
{
  "roots": [
    { "type": "git", "path": "~/repos", "max_depth": 3 },
    { "type": "svn", "path": "~/svn", "max_depth": 2 }
  ],
  "push": {
    "allow_owners": ["acme", "org"],
    "deny_paths": ["~/repos/mirror"],
    "require_upstream": true
  },
  "commit": {
    "never_commit_globs": ["**/.env*", "**/*.key"],
    "max_review_files": 40
  },
  "host_steps": { "opencode_upgrade": false, "restart_service": false }
}
"""

# A token that must never reach the report or the log, in any form.
SECRET = "ghp_AAAABBBBCCCCDDDDEEEEFFFF1234567890"


def git(repo, *args):
    """Run a git command in `repo` and return its stripped stdout."""
    return subprocess.run(
        ("git", "-C", repo) + args,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


class RepoSyncTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="repo-sync-test-")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.home = os.path.join(self.tmp, "home")
        self.remotes = os.path.join(self.tmp, "remotes")
        os.makedirs(self.home)
        os.makedirs(self.remotes)
        self.config = os.path.join(self.tmp, "config.json")
        with open(self.config, "w", encoding="utf-8") as fh:
            fh.write(CONFIG)

        self.git_env = dict(os.environ)
        self.git_env.update(
            HOME=self.home,
            GIT_AUTHOR_NAME="t",
            GIT_AUTHOR_EMAIL="t@example.invalid",
            GIT_COMMITTER_NAME="t",
            GIT_COMMITTER_EMAIL="t@example.invalid",
            GIT_CONFIG_GLOBAL=os.path.join(self.tmp, "gitconfig"),
            GIT_CONFIG_NOSYSTEM="1",
        )

    # ------------------------------------------------------------ fixtures --

    def make_repo(self, owner, name, remote_url=None, push=True):
        """Create a work tree with one commit.

        With no explicit remote_url a local bare repository is used as origin so
        that `git fetch` succeeds without a network. Pass remote_url for a
        hosted remote; those fixtures are not pushed to.
        """
        path = os.path.join(self.home, "repos", owner, name)
        os.makedirs(path, exist_ok=True)
        subprocess.run(("git", "init", "-q", path), check=True, env=self.git_env)
        with open(os.path.join(path, "file.txt"), "w", encoding="utf-8") as fh:
            fh.write("base\n")
        git(path, "add", "-A")
        git(path, "commit", "-qm", "base")
        if remote_url is None:
            bare = os.path.join(self.remotes, name + ".git")
            subprocess.run(("git", "init", "-q", "--bare", bare), check=True, env=self.git_env)
            remote_url = bare
        git(path, "remote", "add", "origin", remote_url)
        if push:
            git(path, "push", "-q", "origin", "HEAD:refs/heads/main")
            tracked = git(path, "rev-parse", "--abbrev-ref", "HEAD")
            git(path, "branch", "--set-upstream-to=origin/main", tracked)
        return path

    def write(self, path, text):
        with open(path, "a", encoding="utf-8") as fh:
            fh.write(text + "\n")

    # -------------------------------------------------------------- runner --

    def run_sync(self):
        env = dict(self.git_env)
        env["REPO_SYNC_CONFIG"] = self.config
        env["REPO_SYNC_LOG_DIR"] = os.path.join(self.tmp, "log")
        return subprocess.run(
            ("bash", SCRIPT),
            capture_output=True,
            text=True,
            env=env,
        )

    def block(self, out, path):
        """Return the '## <type> <path>' report block for one repository."""
        lines = out.splitlines()
        header = "## git " + path
        self.assertIn(header, lines, "no report block for %s" % path)
        start = lines.index(header)
        collected = []
        for line in lines[start + 1:]:
            if line.startswith("## "):
                break
            collected.append(line)
        return dict(
            item.split("=", 1)
            for item in collected
            if "=" in item and not item.startswith("---")
        ), "\n".join(collected)

    # --------------------------------------------------------------- tests --

    def test_reports_dirty_ahead_and_missing_upstream(self):
        clean = self.make_repo("acme", "clean")
        dirty = self.make_repo("acme", "dirty")
        ahead = self.make_repo("acme", "ahead")

        self.write(os.path.join(dirty, "file.txt"), "changed")
        with open(os.path.join(dirty, "new.txt"), "w", encoding="utf-8") as fh:
            fh.write("new\n")

        self.write(os.path.join(ahead, "file.txt"), "a1")
        git(ahead, "commit", "-qam", "a1")
        self.write(os.path.join(ahead, "file.txt"), "a2")
        git(ahead, "commit", "-qam", "a2")

        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

        clean_state, _ = self.block(result.stdout, clean)
        self.assertEqual(clean_state["dirty"], "0")
        self.assertEqual(clean_state["ahead"], "0")

        dirty_state, dirty_block = self.block(result.stdout, dirty)
        self.assertEqual(dirty_state["dirty"], "2")
        self.assertIn("?? new.txt", dirty_block)
        self.assertIn("file.txt", dirty_block)

        ahead_state, _ = self.block(result.stdout, ahead)
        self.assertEqual(ahead_state["ahead"], "2")
        self.assertEqual(ahead_state["dirty"], "0")

    def test_repo_without_remote_is_not_an_error(self):
        path = self.make_repo("acme", "norem")
        git(path, "remote", "remove", "origin")

        result = self.run_sync()
        # A repository with no remote has nothing to fetch; that is not a failure.
        self.assertNotIn("fetch origin failed", result.stdout)
        self.assertIn("no remote: fetch skipped", result.stdout)

        state, _ = self.block(result.stdout, path)
        self.assertEqual(state["upstream"], "")
        self.assertEqual(state["remote"], "")

    def test_credentials_are_redacted_everywhere(self):
        url = "https://acme:%s@github.com/acme/secret.git" % SECRET
        path = self.make_repo("acme", "secret", remote_url=url, push=False)

        result = self.run_sync()
        _, block = self.block(result.stdout, path)

        self.assertNotIn(SECRET, result.stdout, "token leaked into the report")
        self.assertNotIn(SECRET, result.stderr, "token leaked into stderr")
        self.assertIn("https://acme:***@github.com/acme/secret.git", block)

        # ... and into the log file, which is the other place output can land.
        log_dir = os.path.join(self.tmp, "log")
        logs = [os.path.join(log_dir, n) for n in os.listdir(log_dir)]
        self.assertTrue(logs, "no log written")
        for name in logs:
            with open(name, encoding="utf-8") as fh:
                self.assertNotIn(SECRET, fh.read(), "token leaked into %s" % name)

    def test_fetch_failure_sets_exit_code_one(self):
        path = self.make_repo("acme", "gone")
        git(path, "remote", "set-url", "origin",
            "https://github.com/acme/definitely-does-not-exist-9182.git")

        result = self.run_sync()
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("fetch origin failed", result.stdout)
        self.assertIn("failures=1", result.stdout)

    def test_owner_is_parsed_from_hosted_remote(self):
        cases = {
            "git@github.com:acme/ssh.git": "acme",
            "https://github.com/org/https.git": "org",
        }
        for url, expected in cases.items():
            with self.subTest(url=url):
                name = "owner-%s-%d" % (expected, len(cases))
                self.make_repo(expected, name, remote_url=url, push=False)
                result = self.run_sync()
                path = os.path.join(self.home, "repos", expected, name)
                state, _ = self.block(result.stdout, path)
                self.assertEqual(state["owner"], expected)

    def test_max_depth_limits_enumeration(self):
        # owner/repo/.git is depth 3; a deeper nesting must not be picked up.
        self.make_repo("acme", "atdepth")
        deep = os.path.join(self.home, "repos", "acme", "group", "deep")
        os.makedirs(deep, exist_ok=True)
        subprocess.run(("git", "init", "-q", deep), check=True, env=self.git_env)

        result = self.run_sync()
        self.assertIn(os.path.join(self.home, "repos", "acme", "atdepth"), result.stdout)
        self.assertNotIn(deep, result.stdout)

    def test_unknown_root_type_is_reported(self):
        with open(self.config, "w", encoding="utf-8") as fh:
            fh.write('{"roots": [{"type": "hg", "path": "~/repos", "max_depth": 2}]}')
        result = self.run_sync()
        self.assertEqual(result.returncode, 1)
        self.assertIn("unknown root type 'hg'", result.stdout)

    def test_missing_root_is_a_warning_not_a_failure(self):
        # The skill is meant to run on any host; a root configured for another
        # host must not turn the run red.
        with open(self.config, "w", encoding="utf-8") as fh:
            fh.write('{"roots": [{"type": "git", "path": "~/nowhere", "max_depth": 2}]}')
        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertIn("WARN: git root does not exist on this host", result.stdout)
        self.assertIn("failures=0", result.stdout)

    def test_unparsable_config_aborts(self):
        # A broken config must not degrade into an empty report that looks like
        # "nothing to do".
        with open(self.config, "w", encoding="utf-8") as fh:
            fh.write("{ this is not json")
        result = self.run_sync()
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertNotIn("## git", result.stdout)

    def test_shipped_config_is_valid_json_with_known_shape(self):
        import json
        path = os.path.join(ROOT, "skills", "repo-sync", "config.json")
        with open(path, encoding="utf-8") as fh:
            cfg = json.load(fh)
        for key in ("roots", "push", "commit", "host_steps"):
            self.assertIn(key, cfg)
        for root in cfg["roots"]:
            self.assertEqual(set(root), {"type", "path", "max_depth"})
        for key in ("opencode_upgrade", "restart_service"):
            self.assertIn(key, cfg["host_steps"])
        # A restart ends the calling session, so it must be opt-in.
        self.assertFalse(cfg["host_steps"]["restart_service"])
        self.assertFalse(cfg["host_steps"]["opencode_upgrade"])


@unittest.skipUnless(shutil.which("svnadmin") and shutil.which("svn"),
                     "subversion tools not available")
class RepoSyncSvnTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp(prefix="repo-sync-svn-")
        self.addCleanup(shutil.rmtree, self.tmp, ignore_errors=True)
        self.home = os.path.join(self.tmp, "home")
        os.makedirs(os.path.join(self.home, "svn"))
        self.repo = os.path.join(self.tmp, "svnrepo")
        subprocess.run(("svnadmin", "create", self.repo), check=True)
        self.wc = os.path.join(self.home, "svn", "wc")
        subprocess.run(("svn", "-q", "checkout", "file://" + self.repo, self.wc), check=True)
        with open(os.path.join(self.wc, "tracked.txt"), "w", encoding="utf-8") as fh:
            fh.write("base\n")
        subprocess.run(("svn", "-q", "add", "tracked.txt"), cwd=self.wc, check=True)
        subprocess.run(("svn", "-q", "commit", "-m", "init"), cwd=self.wc, check=True)

        self.config = os.path.join(self.tmp, "config.json")
        with open(self.config, "w", encoding="utf-8") as fh:
            fh.write(CONFIG)

    def run_sync(self):
        env = dict(os.environ, HOME=self.home, REPO_SYNC_CONFIG=self.config,
                   REPO_SYNC_LOG_DIR=os.path.join(self.tmp, "log"))
        return subprocess.run(("bash", SCRIPT), capture_output=True, text=True, env=env)

    def test_svn_status_is_reported_without_committing(self):
        with open(os.path.join(self.wc, "tracked.txt"), "a", encoding="utf-8") as fh:
            fh.write("changed\n")
        with open(os.path.join(self.wc, "loose.txt"), "w", encoding="utf-8") as fh:
            fh.write("untracked\n")

        result = self.run_sync()
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("## svn " + self.wc, result.stdout)
        self.assertIn("modified=1", result.stdout)
        self.assertIn("unversioned=1", result.stdout)
        self.assertIn("?       loose.txt", result.stdout)

        # The script must never commit on its own: the modification and the
        # unversioned file both have to still be pending afterwards.
        status = subprocess.run(("svn", "status"), cwd=self.wc,
                                capture_output=True, text=True).stdout
        self.assertIn("M", status, "script committed the change itself")
        self.assertIn("?", status, "script added the unversioned file itself")
        head = subprocess.run(("svn", "info", "--show-item", "revision"), cwd=self.wc,
                              capture_output=True, text=True).stdout.strip()
        self.assertEqual(head, "1", "script made a commit itself")


if __name__ == "__main__":
    unittest.main()
