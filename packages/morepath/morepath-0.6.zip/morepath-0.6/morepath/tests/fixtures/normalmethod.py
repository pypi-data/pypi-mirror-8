import morepath


class app(morepath.App):
    pass


class NormalMethod(object):
    pass


class Root(object):
    def __init__(self):
        self.value = 'ROOT'

    @app.path(model=NormalMethod, path='normal')
    def normal_method(self):
        return NormalMethod()


@app.view(model=NormalMethod)
def normal_method_default(self, request):
    return "Normal Method"
