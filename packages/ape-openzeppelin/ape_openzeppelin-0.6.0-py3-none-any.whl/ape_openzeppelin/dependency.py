from ape.api import DependencyAPI
from ape.managers.project import GithubDependency
from ethpm_types import PackageManifest
from ethpm_types.utils import AnyUrl


class OpenZeppelinDependency(DependencyAPI):
    name: str = "openzeppelin"
    openzeppelin: str

    @property
    def github(self) -> GithubDependency:
        return GithubDependency(
            name=self.name,
            version=self.openzeppelin,
            github="OpenZeppelin/openzeppelin-contracts",
        )

    @property
    def version_id(self) -> str:
        return self.github.version_id

    @property
    def uri(self) -> AnyUrl:
        return self.github.uri

    def extract_manifest(self, use_cache: bool = True) -> PackageManifest:
        return self.github.extract_manifest(use_cache=use_cache)
