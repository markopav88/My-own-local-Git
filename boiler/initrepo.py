class GitRepository (object):
    """A git repository"""
    worktree = None
    gitdir = None
    conf = None
#Force argument will disable all checks to be able to have a way to create such objects from a still,
#invalid filesystem location
    def __init__(self, path,force = False):
        self.worktree = path
        self.gitdir = os.path.join(path,".git")

        if not (force or os.path.isdir(self.gitdir)):
            raise Exception(f"Not a Git repository {path}")
        #Read the configuation file in .git/config
        self.conf = configparser.ConfigParser()
        cf = repo_file(self, "config")

        if cf and os.path.exists(cf):
            self.conf.read([cf])
        elif not force:
            raise Execption("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion: {vers}")
