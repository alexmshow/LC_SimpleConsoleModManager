from dataclasses import dataclass
import fetcher
import directory

class _t:
    def start(self):
        ...

@dataclass
class Mod:
    name:           str
    version:        str
    url:            str
    author:         str
    filename:       str
    relative_path:  str
    depends:        list

    @classmethod
    def from_url(cls, url):
        page = fetcher.get_page(url)
        if page:
            return fetcher.parse(page)
        return _t()

    def check_mod(self):
        return directory.check_file(self.relative_path)

    def download(self):
        if self.check_mod():
            return
        fetcher.download(self.url, self.relative_path)
    
    def unpack(self):
        directory.unpack(self.relative_path, "./mods/")
    
    def unpack_deps(self):
        for dep in self.depends:
            dep.unpack()

    def download_deps(self):
        for dep in self.depends:
            if not dep.check_mod():
                dep.download()
                dep.download_deps()
    
    def start(self):
        self.download_deps()
        self.download()
        self.unpack_deps()
        self.unpack()
    
    def __hash__(self) -> int:
        return hash(self.name) + hash(self.version)