class Joke:
    joke_id = 1

    def __init__(self,id, value, created_at, updated_at, removed):

        if id == "new":
            self.id = Joke.joke_id
        else:
            self.id = id
        self.value = value
        self.created_at = created_at
        self.updated_at = updated_at
        # self.created_at = 'created_at'
        # self.updated_at = 'updated_at'
        self.removed = removed
        self.type = 'Joke'
        Joke.joke_id += 1

    def set_value(self, value):
        self.value = value

    def set_created_at(self, created_at):
        self.created_at = created_at

    def set_updated_at(self, updated_at):
        self.updated_at = updated_at

    def set_removed(self, removed):
        self.removed = removed

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def get_created_at(self):
        return self.created_at

    def get_updated_at(self):
        return self.updated_at

    def get_removed(self):
        return self.removed


class ImageJoke(Joke):
    def __init__(self,id, value, created_at, updated_at, removed,image_url):
        super().__init__(id, value, created_at, updated_at, removed)
        self.image_url = image_url
        self.type = 'ImageJoke'

    def get_url(self):
        return self.image_url

    def set_url(self, image_url):
        self.image_url = image_url

    def __repr__(self):
        return f"ImageJoke(id={self.id}, value='{self.value}', image_url='{self.image_url}')"

