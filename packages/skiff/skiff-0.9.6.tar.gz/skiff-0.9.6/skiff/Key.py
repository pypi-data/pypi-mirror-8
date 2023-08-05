skiff = None


def setSkiff(s):
    global skiff
    skiff = s


class SkiffKey(object):
    """SkiffKey"""
    def __init__(self, options=None, **kwargs):
        super(SkiffKey, self).__init__()
        if not options:
            options = kwargs

        self._json = options
        self.__dict__.update(options)
        self.delete = self.destroy
        self.refresh = self.reload

    def __repr__(self):
        return '<%s (#%s)>' % (self.name, self.id or '??')

    def reload(self):
        return get(self.id)

    def update(self, new_name):
        options = {
            'name': new_name
        }

        r = skiff.put('/account/keys/%s' % (self.id), data=options)
        self.name = new_name
        return SkiffKey(r['ssh_key'])

    def destroy(self):
        return skiff.delete('/account/keys/%s' % (self.id))


def get(kid):
    try:
        r = skiff.get('/account/keys/%s' % (kid))
        return SkiffKey(r['ssh_key'])
    except ValueError, e:
        # try searching
        keys = all()
        for key in keys:
            if kid in key.name:
                return key
        raise e


def create(options=None, **kwargs):
    if not options:
        options = kwargs

    r = skiff.post('/account/keys', data=options)
    if 'message' in r:
        raise ValueError(r['message'])
    else:
        return SkiffKey(r['ssh_key'])


# alias new to create
new = create


def all(params=None, **kwargs):
    if not params:
        params = kwargs

    return skiff.get('/account/keys', (lambda r: [SkiffKey(d) for d in r['ssh_keys']]), params)
