# coding: utf-8


class Tokenizer(object):

    def __init__(self):
        import MeCab
        self.tagger = MeCab.Tagger()

    def wakati(self, text):
        return " ".join([token.split("\t")[0]
                         for token in self.tagger.parse(text).split("\n")[:-2]])


tokenizer = Tokenizer()

filename = "samples.tsv"

f = open(filename, "w")

columns = ["ID", "E_TEXT", "R_TEXT"]
template = "{%s}\n" % "}\t{".join(columns)
f.write(template.format(**{c: c for c in columns}))

sample1 = {
    "ID": "1111111",  # str
    "E_TEXT": tokenizer.wakati("今日はいい天気ですね。"),
    "R_TEXT": tokenizer.wakati("明日は晴れそうですね。"),
}
f.write(template.format(**sample1))

f.close()
