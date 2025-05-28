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
            raise Excepption("Configuration file missing")

        if not force:
            vers = int(self.conf.get("core", "repositoryformatversion"))
            if vers != 0:
                raise Exception("Unsupported repositoryformatversion: {vers}")
#Next is Path manipulaiton of the repo with utility functions
'''These functions will compute the paths and create missing directorys structures if needed
First will be a general path building function'''
#the *path makes the function variadic so call with multiple path components as seperate args
#Recieves the path as a list
def repo_path(repo, *path):
    #Joins the .git directory of the repo with additional path components.
    """Compute path under repo's gitdir."""
    return os.path.join(repo.gitdir, path)

def repo_file(repo, *path, mkdir=False):
    #Returns full path inside/under .git/ ensures directory leading to file exists / the directory is real
    #This file fuction only creates directories up to the last component unlike the other 
    #Same as repo_path, but create dirname(*path) if absent
    if repo_dir(repo, *path[:-1], mkdir = mkdir):
        #The path[:-1] exlcudes the file name to ensure only directories are created
        return repo_path(repo, *path)
def repo_dir(repo, *path, mkdir=False):
    #Ensures the directory's path exists and optionally creating it
    """Same as repo_path, but mkdir *path if absent if mkdir"""
    #returns the full path
    path = repo_path(repo, *path)
    #if mkdir is true
    if os.path.exists(path):
        #edgecase to make sure the path is also a directory
        if(os.path.isdir(path)):
            #the os module is great from python because in this specific case i can ask the os 
            #"Hey is this path a directory?""
            return path
        else:
            raise Exception(f"Not a directory {path}")
        
    if mkdir:
        os.makedirs(path) #Creates the full directory path if it doesnt exist
        return path
    else:
        return None
    
    #Next we will work on creating a new repository(starting with the directory)
    #need import os?
def repo_create(path):
    """Create a new repository at path"""
    #path is where the user want the repo to be, true skips the validation(create a new repo)
    repo = GitRepository(path, force = true)
    #Force is here in CREATE because we need to overide the .git directory check because the thing we want to create doesnt even exist yet 

    #Now make sure we are not overwriting the exisiting non-empty repo
    if os.path.exists(repo.worktree):
        if not os.path.isdir(repo.worktree):
            #dont want to treat a file as a directory
            raise Exception(f"{path} is not a directory(a file most likey?)!")
        if os.path.exists(repo.gitdir) and os.listdir(repo.gitdir):
            #dont want to override .git data that already there for the path
            #only want to make a new repo is .git/ if msising or empty
            raise Exception(f"{path} is not empty")
    else:
        os.makedirs(repo.worktree)
"""If path exists,make sure its a directory ,Make sure .git is missing or empty ,If doesnt exist, create a directory """

    #assert to make sure doesnt fail in silence
    """This sets up gits needed structure(branch names,objects for gits data(blobs,trees,commits 
    and ref/tags and ref/heads for tracking tags and branchs)"""
    assert repo_dir(repo, "branches",mkdir=True)
    assert repo_dir(repo, "objects",mkdir =True)
    assert repo_dir(repo, "refs","tags",mkdir=True)
    assert repo_dir(repo,"refs","heads",mkdir =True)

    #.git/description
    with open(repo_file(repo, "HEAD"), "w") as f: 
        f.write("ref: refs/heads/master\n") #set default branch as master

    with open(repo_file(repo,"config"), "w") as f: #need config for format,file mode,if repo == bare?
        config = repo_default_config()
        config.write(f)
    return repo

    










    