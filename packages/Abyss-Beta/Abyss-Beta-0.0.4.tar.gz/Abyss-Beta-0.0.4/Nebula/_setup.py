try:
    from .NebulaObject import *
    from .NebulaCore import *
except ModuleNotFoundError:
    print("~| _setup SCRIPT IMPORT ERROR...")
    os.sys.exit()

ABYSS = None

class Main:
    def __init__(self, abyss, projectName:str="MyNebulaProject", projectType:str="pt", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject"), autoNCFG:bool=True, manNCFG:bool=False):
        self.abyss = abyss
        ABYSS = abyss
        if autoNCFG and not manNCFG:
            self.autoNCFG(abyss=abyss, projectType=projectType, projectName=projectName, projectPath=projectPath)
        if manNCFG and not autoNCFG:
            return 'manual config specified\n\n'

    def genCFG(self, abyss, projectType:str="pt", projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        ncfgTemplate = {
            "env": {
                "debug": "False",
                "update": "False",
                "configured": "False"
            },
            "project": {
                "cfg":"auto",
                "build ver": "v0.0.1",
                "project name": f"{projectName}",
                "project type": f"{projectType}",
                "project path": f"{projectPath}",
                "tilesize": 8,
                "tilemap size": [5000,5000],
                "screen size": [1400, 800],
                "canvas size": [700, 400],
                "target FPS": 60
            }
        }
        try:
            with open(f"{projectPath}\\.ncfg", "r") as check:
                c = check.read()
                check.close()
            
            if "env" not in c:
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
                    cache = json.load(f)
                    f.close()
                cache['Nebula'][projectName] = {}
                cache['current project'] = projectName
                cache['Nebula'][projectName]['path'] = projectPath
                cache['Nebula'][projectName]['project name'] = projectName
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
                    json.dump(cache, f, indent=4)
                    f.close()
                
                with open(f"{projectPath}\\.ncfg", "w") as f:
                    json.dump(
                        ncfgTemplate,
                        f,
                        indent=4
                    )
                    f.close()
            
            if "env" in c:
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
                    cache = json.load(f)
                    f.close()
                cache['Nebula'][projectName] = {}
                cache['current project'] = projectName
                cache['Nebula'][projectName]['path'] = projectPath
                cache['Nebula'][projectName]['project name'] = projectName
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
                    json.dump(cache, f, indent=4)
                    f.close()

                with open(f"{projectPath}\\.ncfg", "r") as f:
                    data = json.load(f)
                    f.close()

                if data['env']['configured'] == 'True':
                    abyss.custom_print('Nebula Project Configured.')
        
        
        except (FileNotFoundError):
            if not os.path.exists(f"{projectPath}"):
                os.mkdir(f"{projectPath}")
                abyss.custom_print('Project directory not found! Generating it now!')
            
            abyss.custom_print('Project .ncfg not found! Generating one now!')
            with open(f"{projectPath}\\.ncfg", "w") as check:
                json.dump(
                    ncfgTemplate,
                    check,
                    indent=4
                )
                check.close()
            
            with open(f"{projectPath}\\.ncfg", "r") as check:
                c = check.read()
                check.close()
            
            if "env" not in c:
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
                    cache = json.load(f)
                    f.close()
                cache['Nebula'][projectName] = {}
                cache['current project'] = projectName
                cache['Nebula'][projectName]['path'] = projectPath
                cache['Nebula'][projectName]['project name'] = projectName
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
                    json.dump(cache, f, indent=4)
                    f.close()
                
                with open(f"{projectPath}\\.ncfg", "w") as f:
                    json.dump(
                        ncfgTemplate,
                        f,
                        indent=4
                    )
                    f.close()
            
            if "env" in c:
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
                    cache = json.load(f)
                    f.close()
                cache['Nebula'][projectName] = {}
                cache['current project'] = projectName
                cache['Nebula'][projectName]['path'] = projectPath
                cache['Nebula'][projectName]['project name'] = projectName
                with open(f"C:\\.NebulaCache\\nebula-cache.json", "w") as f:
                    json.dump(cache, f, indent=4)
                    f.close()

                with open(f"{projectPath}\\.ncfg", "r") as f:
                    data = json.load(f)
                    f.close()

                if data['env']['configured'] == 'True':
                    abyss.custom_print('Nebula Project Configured.')
        

    def autoNCFG(self, abyss, projectType:str="pt", projectName:str="MyNebulaProject", projectPath:str=os.path.join(os.getcwd(), "MyNebulaProject")):
        self.genCFG(abyss, projectType=projectType, projectName=projectName, projectPath=projectPath)

        from ._autoCFG import Main as autoMain
        autoMain(abyss, projectType=projectType, projectName=projectName, projectPath=projectPath)


if not os.path.exists('C:\\.NebulaCache'):
    os.mkdir('C:\\.NebulaCache')

if not os.path.exists('C:\\.NebulaCache\\nebula-cache.json'):
    with open('C:\\.NebulaCache\\nebula-cache.json', 'w') as f:
        f.write("")
        json.dump({"Nebula":{}, "current project":""}, f, indent=4)
        f.close()

def loadCache() -> dict:
    with open(f"C:\\.NebulaCache\\nebula-cache.json", "r") as f:
        cache = json.load(f)
        f.close()
    return cache


def configRecentProject(abyss):
    cache = loadCache()
    recentProject = list(cache['Nebula'].keys())[len(cache['Nebula'])-1]
    projectPath= cache['Nebula'][recentProject]['path']
    abyss.custom_print(f'Configuring {recentProject}...')
    Main(
        abyss=abyss,
        projectName=recentProject,
        projectType="pt",
        projectPath=projectPath,
        autoNCFG=True,
        manNCFG=False
    )

def configLoadProject(abyss, choice:str):
    cache = loadCache()
    if choice in list(cache['Nebula'].keys()):
        projectPath=cache['Nebula'][choice]['path']
        abyss.custom_print(f'Configuring {choice}!')
        Main(
            abyss=abyss,
            projectName=choice,
            projectType="pt",
            projectPath=projectPath,
            autoNCFG=True,
            manNCFG=False
        )
    else:
        abyss.custom_print(f'Unable to locate {choice}!')
        abyss.custom_print(f'You can navigate to your project\'s .ncfg and take a look at the name if need be!')

def configNewProject(abyss, projectName:str="", projectPath:str=""):
    abyss.custom_print('New project!')
    abyss.custom_print('Lets get it set up!')
    Main(
        abyss=abyss,
        projectName=projectName,
        projectType="pt",
        projectPath=projectPath,
        autoNCFG=True,
        manNCFG=False
    )