class OutdatedPackagesError(Exception):
    '''
    Error raised when there is an outdated package found
    '''
    def __init__(self, packages: list[str]) -> None:
        self.packages = packages

    def __str__(self) -> str:
        return f'{len(self.packages)} Packages Require Attention: {self.packages}'
    
    def __repr__(self) -> str:
        return f'<OutdatedPackagesError({self.packages})>'