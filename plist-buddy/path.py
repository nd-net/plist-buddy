class Path:
    
    def __init__(self, *components):
        items = []
        for component in components:
            ctype = type(component)
            if ctype == str:
                if component:
                    items.append(component)
            elif ctype == Path:
                items += component.components
            else:
                raise TypeError("expected 'str' or 'Path', but received a '{}'".format(ctype))
        self.components = tuple(items)
    
    def __str__(self):
        if not self.components:
            return ":"
        else:
            return ":" + ":".join(self.components)
    
    def __repr__(self):
        return "Path({})".format(", ".join(repr(component) for component in self.components))
    
    def __bool__(self):
        return bool(self.components)
    
    def __eq__(self, other):
        if type(other) != Path:
            return False
        return self.components == other.components
    
    def join(self, *rest):
        if not rest:
            return self
        
        return Path(self, *rest)
