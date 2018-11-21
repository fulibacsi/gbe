from lxml.etree import Element, fromstring, tostring


class Action:

    def __init__(self, action, target):
        self.action = action
        self.target = target

    def as_xml(self):
        action = Element('action', target=f'#{self.target}')
        action.text = self.action
        return action
    
    def __repr__(self):
        return self.as_xml()

    def as_str(self, format='xml'):
        text = self.as_html() if format == 'html' else self.as_xml()
        return tostring(text, pretty_print=True, encoding='unicode')
        
    def __str__(self):
        return self.as_str()

    def as_html(self):
        action = Element('a', href=f'#{self.target}')
        action.set('class', 'action')
        action.text = self.action
        return action


class Chapter:

    def __init__(self, chapter_number, text, actions=None, end='not'):
        self.id = chapter_number
        self.text = text
        self.actions = actions or []
        if end not in ('fail', 'win', 'not'):
            raise Exception('Invalid chapter ending value.')
        self.end = end 

    def as_xml(self):
        chapter = Element('chapter', id=str(self.id), end=self.end)
        chapter.text = self.text
        for action in self.actions:
            chapter.append(action.as_xml())
        return chapter

    def __repr__(self):
        return self.as_xml()

    def as_str(self, format='xml'):
        text = self.as_html() if format == 'html' else self.as_xml()
        return tostring(text, pretty_print=True, encoding='unicode')

    def __str__(self):
        return self.as_str()

    def as_html(self):
        text = Element('p')
        text.text = self.text
        
        actionlist = Element('ul')
        for action in self.actions:
            li = Element('li')
            li.append(action.as_html())
            actionlist.append(li)

        chapter = Element('div', id=str(self.id), end=self.end)
        chapter.set('class', 'chapter')
        chapter.append(text)
        chapter.append(actionlist)

        return chapter


class Book:

    def __init__(self, title=None, chapters=None, filename=None):
        self.title = title
        self.chapters = chapters
        
        if filename is not None:
            self.load(filename)

    def as_xml(self):
        title = Element('h1')
        title.text = self.title

        book = Element('book', title=self.title)
        book.append(title)
        
        for chapter in self.chapters:
            book.append(chapter.as_xml())

        return book

    def __repr__(self):
        return self.as_xml()

    def as_str(self, format='xml'):
        text = self.as_html() if format == 'html' else self.as_xml()
        return tostring(text, pretty_print=True, encoding='unicode')

    def __str__(self):
        return self.as_str()

    def as_html(self):
        # TITLE
        title = Element('h1')
        title.text = self.title

        # CONTENT
        book = Element('div', title=self.title)
        book.append(title)
        book.append(Element('hr'))

        for chapter in self.chapters:
            book.append(chapter.as_html())

        # HEADER
        headtitle = Element('title')
        headtitle.text = self.title
        head = Element('head')
        head.append(headtitle)

        # FOOTER
        footerscript = Element('script', type="text/javascript")
        with open('./resources/click_and_hide.js') as f: #TODO: fixthis - dynamic path
            script = f.read() + f'reveal({self.chapters[0].id});'
        footerscript.text = script

        # BODY
        body = Element('body')
        body.append(book)
        body.append(footerscript)

        # HTML
        root = Element('html')
        root.append(head)
        root.append(body)
        
        return root

    def save(self, outpath):
        with open(outpath, 'w') as f:
            f.write(self.as_str())
    
    def load(self, inpath):
        with open(inpath) as f:
            book = fromstring(f.read())
        
        self.title = book.get('title')

        self.chapters = []
        for chapter in book.iter('chapter'):
            actions = [Action(action=action.get('action'), 
                              target=int(action.get('target')[1:]))
                       for action in chapter.iter('action')]
            chapter = Chapter(chapter_number=int(chapter.get('id')), 
                              text=chapter.text,
                              actions=actions,
                              end=chapter.get('end'))
            self.chapters.append(chapter)

    def export(self, outpath):
        with open(outpath, 'w') as f:
            f.write(self.as_str('html'))


if __name__ == '__main__':
    # TODO: move this part to a test file?
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('bookfile', help='book file')
    args = parser.parse_args()

    book = Book(
        title='You are the hero!',
        chapters=[
            Chapter(
                chapter_number=1, 
                text='''Your journey begins! 
                You are standing at the entrance of a cave 
                with a deep hole next to it. 
                What do you do?''',
                actions=[Action('Return home', 5),
                         Action('Jump into the hole', 4),
                         Action('Enter cave', 2)]
            ),
            Chapter(
                chapter_number=2,
                text="It's pitch black inside!",
                actions=[Action('Charge forward!', 3),
                         Action('Exit cave', 1)]
            ),
            Chapter(
                chapter_number=3,
                text='You ran into a deep hole and fell down.',
                actions=[Action("You know what's next, right?", 4)]
            ),
            Chapter(
                chapter_number=4,
                text='You have died!',
                actions=[],
                end='fail'
            ),
            Chapter(
                chapter_number=5,
                text='''Congratulations! 
                You have successfully survived the adventure!''',
                actions=[],
                end='win'
            )
        ]
    )

    book.save(args.bookfile + '.xml')
    book.export(args.bookfile + '.html')

