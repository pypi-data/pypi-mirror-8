# -*- coding: utf-8 -*-
import unittest
from unihandecode import Unihandecoder

class TestUnidecodeAdvanced(unittest.TestCase):

    def test_long_japanese_text(self):

        input = u"日本国民は、正当に選挙された国会における代表者を通じて行動し、われらとわれらの子孫のために、諸国民との協和による成果と、わが国全土にわたつて自由のもたらす恵沢を確保し、政府の行為によつて再び戦争の惨禍が起ることのないやうにすることを決意し、ここに主権が国民に存することを宣言し、この憲法を確定する。そもそも国政は、国民の厳粛な信託によるものであつて、その権威は国民に由来し、その権力は国民の代表者がこれを行使し、その福利は国民がこれを享受する。これは人類普遍の原理であり、この憲法は、かかる原理に基くものである。われらは、これに反する一切の憲法、法令及び詔勅を排除する。"
        # FIXME last space
        output = "Nihonkokumin ha, Seitou ni Senkyo sareta Kokkai niokeru Daihyousha wo Tsuuji te Koudou shi, wareratowarerano Shison notameni, Shokokumin tono Kyouwa niyoru Seika to, waga Kuni Zendo niwatatsute Jiyuu nomotarasu Keitaku wo Kakuho shi, Seifu no Koui niyotsute Futatabi Sensou no Sanka ga Okoru kotononaiyaunisurukotowo Ketsui shi, kokoni Shuken ga Kokumin ni Sonsu rukotowo Sengen shi, kono Kenpou wo Kakuteisu ru. somosomo Kokusei ha, Kokumin no Genshuku na Shintaku niyorumonodeatsute, sono Ken'i ha Kokumin ni Yurai shi, sono Kenryoku ha Kokumin no Daihyousha gakorewo Koushi shi, sono Fukuri ha Kokumin gakorewo Kyouju suru. koreha Jinruifuhen no Genri deari, kono Kenpou ha, kakaru Genri ni Motozuku monodearu. wareraha, koreni Hansu ru Issai no Kenpou, Hourei Oyobi Shouchoku wo Haijo suru. "

        u = Unihandecoder(lang="ja")
        self.assertEqual(u.decode(input), output)
