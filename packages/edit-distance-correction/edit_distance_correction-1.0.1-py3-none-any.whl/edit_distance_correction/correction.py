import Levenshtein
import pypinyin

class Corrector:
    def __init__(self):
        self.pinyin_di = dict()


    def load_target_words(self, target_words):
        for word in target_words:
            res = self._get_pinyin(word)
            if res not in self.pinyin_di:
                self.pinyin_di[res] = set()
            self.pinyin_di[res].add(word)


    def _get_pinyin(self, word):
        word_pinyin = pypinyin.pinyin(word, style=pypinyin.NORMAL)
        res = "|".join([elem[0] for elem in word_pinyin])
        return res


    def find_word(self, word, pinyin_threshold=0, char_threshold=4):
        word_pinyin = self._get_pinyin(word)
        pinyin_dis = [(elem, Levenshtein.distance(word_pinyin, elem)) for elem in self.pinyin_di]
        pinyin_dis = list(filter(lambda x: x[1] <= pinyin_threshold, pinyin_dis))
        valid_choice = dict()
        for pinyin in pinyin_dis:
            candidate_chars = self.pinyin_di[pinyin[0]]
            for cc in candidate_chars:
                char_dis = Levenshtein.distance(word, cc)
                if char_dis <= char_threshold:
                    valid_choice[cc] = pinyin[1] + char_dis
        if len(valid_choice) > 0:
            res = sorted(valid_choice.items(), key=lambda x:x[1])
            return res[0][0]
        return None

# c = Corrector()
# c.load_target_words(["化肥", "话费"])
# res = c.find_word("花费")
# print(res)



















