# coding: utf-8


class Reader(object):

    INPUT_COLUMNS = ["ID", "E_TEXT", "R_TEXT"]

    def __init__(self, input_path, to_line_number=None):
        self.path = input_path
        self.to_line_number = to_line_number

    def __iter__(self):
        for line_i, line in enumerate(open(self.path)):
            values = line.replace("\n", "").split("\t")
            if line_i == 0:
                if not all([column in values for column in self.INPUT_COLUMNS]):
                    raise Exception("%s not has all columns %s" % (self.path, self.INPUT_COLUMNS))
                self.columns = values
            else:
                data = {column: value for column, value in zip(self.columns, values)}
                yield tuple([data[column] for column in self.INPUT_COLUMNS])


class Writer(object):

    OUTPUT_COLUMNS = ["ID"]

    def __init__(self, output_path, *measures):
        self.path = output_path
        self.f = open(self.path, "w")

        self.OUTPUT_COLUMNS = Writer.OUTPUT_COLUMNS + [m.COLUMN_NAME for m in measures]
        self.measures = measures

        self._write(*self.OUTPUT_COLUMNS)

    def _write(self, *args):
        self.f.write("%s\n" % "\t".join(map(str, args)))

    def write(self, qid, eval_text, ref_text):
        scores = [m(eval_text, ref_text) for m in self.measures]
        self._write(qid, *scores)

    def close(self):
        self.f.close()


class Measure(object):

    COLUMN_NAME = None

    def __init__(self):
        if not self.COLUMN_NAME:
            raise Exception("Not implemented with COLUMN_NAME")

    def __call__(self, e_text, r_text):
        return self._calc(e_text, r_text)


class Rouge(Measure):

    def __init__(self, n=1):
        self.n = n
        self.COLUMN_NAME = "ROUGE-%d" % self.n
        Measure.__init__(self)
        import rouge as rouge_lib
        self._rouge = rouge_lib.Rouge()

    def _calc(self, e_text, r_text):
        res = self._rouge.get_scores(e_text, r_text)[0]
        # Check
        # import ipdb
        # ipdb.set_trace()
        return res["rouge-%d" % self.n]["f"]  # ?


def main():
    # to_line_number = 2
    to_line_number = None

    inputname = "samples.tsv"
    reader = Reader(inputname)

    outputname = inputname + ".measures.tsv"
    measures = [Rouge()]
    writer = Writer(outputname, *measures)

    for _id, e_text, r_text in reader:
        print(_id, e_text, r_text)
        writer.write(_id, e_text, r_text)

    writer.close()


if __name__ == "__main__":
    main()
