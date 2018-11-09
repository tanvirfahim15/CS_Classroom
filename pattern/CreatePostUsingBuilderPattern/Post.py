import re
regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'


class Post:
    post_text=''
    author=''
    course_id=''
    topic=''
    links=[]

    def __init__(self):
        pass

    class PostBuilder:
        post_text = ''
        author = ''
        course_id = ''
        topic = ''
        links =[]

        def __init__(self, course_id):
            self.course_id = course_id

        def with_text(self, text):
            self.post_text = text
            return self

        def with_author(self, author):
            self.author = author
            return self

        def with_topic(self, topic):
            self.topic = topic
            return self

        def with_links(self, links):
            self.links = self.get_separattionList(links)
            return self

        def build(self):
            post = Post()
            post.course_id = self.course_id
            post.post_text = self.post_text
            post.author = self.author
            post.topic = self.topic
            post.links = self.links
            return post

        def get_separattionList(self, links):
            # print("original: "+links)
            # urls = re.findall(regex, links)
            links = str(links)
            urls = links.split(',')
            #print(urls)
            return urls

    def get_post_text(self):
        return self.post_text

    def get_author(self):
        return self.author

    def get_course_id(self):
        return self.course_id

    def get_topic(self):
        return self.topic

    def get_links(self):
        return self.links

