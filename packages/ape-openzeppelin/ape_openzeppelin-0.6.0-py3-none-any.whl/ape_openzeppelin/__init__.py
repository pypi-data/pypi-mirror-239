from ape import plugins

from .dependency import OpenZeppelinDependency


@plugins.register(plugins.DependencyPlugin)
def dependencies():
    yield "openzeppelin", OpenZeppelinDependency
