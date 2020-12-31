import genanki

style = """
.question {
 text-align: center;
}

.answer {
 font-family: arial;
 font-size: 24px;
 color: black;
 background-color: white;
}
"""

# 定义 model
model = genanki.Model(
        1380120064,
        '综合素质',
        fields=[
            {'name': 'question'},
            {'name': 'answer'},
            ],
        templates=[
            {
                'name': 'Card 1',
                'qfmt': '<div class="question"> {{question}} </div>',
                'afmt': '{{FrontSide}} <hr id="answer"> <div class="answer">{{answer}}</div>',
                },
            ],
        css=style)



def create_note(question_content, answer_content):
    # 给 model 传参，添加一个note， 可以添加多个note
    note = genanki.Note(
            model=model,
            fields=[question_content, answer_content])

    return note


def create_deck(deck_id, deck_name, note_list):

    # 创建牌组
    deck = genanki.Deck(deck_id, deck_name)

    for note in note_list:
        deck.add_note(note)

    return deck


def create_package(deck):
   # 创建压缩包
    package = genanki.Package(deck)

    # 添加图片
    # my_package.media_files = ['format.jpg']

    return package

def generate_anki_file(package, file_name):

    package.write_to_file(file_name)


