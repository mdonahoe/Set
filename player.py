import Image
from random import shuffle


def colorize(im, color):
    cleared = Image.new('RGBA',im.size,(0,0,0,0))
    colored = Image.new('RGBA',im.size,color)
    return Image.composite(colored,cleared,im)


# create colored versions of all shapes
class Card(object):
    def __init__(self, fill,shape,number,color):
        name = 'gen/%s%s%s.png' % (fill,shape,number)
        im = Image.open(name)
        self.im = colorize(im, color)
        self.props = (fill,shape,number,color)


def compare(A,B,C):
    for a,b,c in zip(A,B,C):
        if a == b == c: continue
        if a != b != c != a: continue
        return False
    return True

fills = 'lsf'
shapes = 'tcs'
numbers = '123'
colors = [
    (255,0,0,255),
    (0,255,0,255),
    (0,0,255,255),
]

cards = [
        Card(f,s,n,c)
        for f in fills
        for s in shapes
        for n in numbers
        for c in colors
        ]


class Board(object):
    def __init__(self, cards):
        self.cards = cards[:]
        self.X = 3
        self.Y = 3

    def check_set(self):
        N = self.X * self.Y
        sets = [
            (i,j,k)
            for i in range(N)
            for j in range(N)
            for k in range(N)
            if self.compare_cards(i,j,k)
            and i < j < k
        ]
        return sets

    def compare_cards(self, *indexes):
        cards = [self.cards[i] for i in indexes]
        props = [c.props for c in cards]
        return compare(*props)

    def render(self):
        # take the top 12, and draw a grid
        attempts = 1000
        shuffle(self.cards)
        while attempts and len(self.check_set()) != 1:
            attempts -= 1
            shuffle(self.cards)

        W,H = self.cards[0].im.size
        X,Y = self.X,self.Y
        board = Image.new('RGBA',(X*W,Y*H),(255,255,255,255))
        i = 0
        for y in range(Y):
            for x in range(X):
                c = self.cards[i].im
                board.paste(c, (W*x,H*y), c)
                i+=1
        board.save('board.png')


b = Board(cards)
b.render()
