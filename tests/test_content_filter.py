import unittest
from llamove.content_filter import ContentFilter

class TestContentFilter(unittest.TestCase):
    def setUp(self):
        self.content_filter = ContentFilter()

    def test_is_short_line(self):
        text = "short line"
        self.assertTrue(self.content_filter._is_short_line(text))

    def test_not_short_line(self):
        text = "this should be a long line instead dont filter me out pls"
        self.assertFalse(self.content_filter._is_short_line(text))

    def test_figure_table(self):
        text1 = "Figure 1: Description"
        text2 = "Table 2: Description"
        text3 = "We employ three types of regularization during training:"

        self.assertTrue(self.content_filter._is_table_or_figure(text1))
        self.assertTrue(self.content_filter._is_table_or_figure(text2))
        self.assertFalse(self.content_filter._is_table_or_figure(text3))

    def test_is_mostly_numerical(self):
        text1 = "To evaluate the importance of different components of the Transformer, we varied our base model"
        self.assertFalse(self.content_filter._is_mostly_numerical(text1))

        # Test for a string that's mostly numerical
        text2 = "123 456 789 Hello World 1011 1213"
        self.assertTrue(self.content_filter._is_mostly_numerical(text2))

        # Test for a string that's equally divided between numerical and non-numerical words
        text3 = "123 456 Hello World"
        self.assertTrue(self.content_filter._is_mostly_numerical(text3))

        # Test for a string that's entirely numerical
        text4 = "1234 5678 91011 121314"
        self.assertTrue(self.content_filter._is_mostly_numerical(text4))

        # Test for a string with no numerical words
        text5 = "Hello, this line has no numbers!"
        self.assertFalse(self.content_filter._is_mostly_numerical(text5))

        # Test for an empty string
        text6 = ""
        self.assertTrue(self.content_filter._is_mostly_numerical(text6))  # Depending on your function's behavior with empty strings

    def test_is_metadata(self):
        text1 = "To evaluate the importance of different components of the Transformer, we varied our base model"
        text2 = "Copyright 2023 by XYZ"
        text3 = "Conference on Natural Language Processing"
        text4 = "Page 23 of 120"

        self.assertFalse(self.content_filter._is_metadata(text1))
        self.assertTrue(self.content_filter._is_metadata(text2))
        self.assertTrue(self.content_filter._is_metadata(text3))
        self.assertTrue(self.content_filter._is_metadata(text4))

    def test_filtering(self):
        text1 = """
Provided proper attribution is provided, Google hereby grants permission to
reproduce the tables and figures in this paper solely for use in journalistic or
scholarly works.
Attention Is All You Need
Ashish Vaswani∗
Google Brain
avaswani@google.comNoam Shazeer∗
Google Brain
noam@google.comNiki Parmar∗
Google Research
nikip@google.comJakob Uszkoreit∗
Google Research
usz@google.com
Llion Jones∗
Google Research
llion@google.comAidan N. Gomez∗ †
University of Toronto
aidan@cs.toronto.eduŁukasz Kaiser∗
Google Brain
lukaszkaiser@google.com
Illia Polosukhin∗ ‡
illia.polosukhin@gmail.com
Abstract"""
        expect1 = """Provided proper attribution is provided, Google hereby grants permission to
reproduce the tables and figures in this paper solely for use in journalistic or"""

        text2 = """
The dominant sequence transduction models are based on complex recurrent or
convolutional neural networks that include an encoder and a decoder. The best
performing models also connect the encoder and decoder through an attention
mechanism. We propose a new simple network architecture, the Transformer,
based solely on attention mechanisms, dispensing with recurrence and convolutions
entirely. Experiments on two machine translation tasks show these models to
be superior in quality while being more parallelizable and requiring significantly
less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-
to-German translation task, improving over the existing best results, including
ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task,
our model establishes a new single-model state-of-the-art BLEU score of 41.8 after
training for 3.5 days on eight GPUs, a small fraction of the training costs of the
best models from the literature. We show that the Transformer generalizes well to
other tasks by applying it successfully to English constituency parsing both with
large and limited training data.
"""
        expect2 = """The dominant sequence transduction models are based on complex recurrent or
convolutional neural networks that include an encoder and a decoder. The best
performing models also connect the encoder and decoder through an attention
mechanism. We propose a new simple network architecture, the Transformer,
based solely on attention mechanisms, dispensing with recurrence and convolutions
entirely. Experiments on two machine translation tasks show these models to
be superior in quality while being more parallelizable and requiring significantly
less time to train. Our model achieves 28.4 BLEU on the WMT 2014 English-
to-German translation task, improving over the existing best results, including
ensembles, by over 2 BLEU. On the WMT 2014 English-to-French translation task,
our model establishes a new single-model state-of-the-art BLEU score of 41.8 after
training for 3.5 days on eight GPUs, a small fraction of the training costs of the
best models from the literature. We show that the Transformer generalizes well to
other tasks by applying it successfully to English constituency parsing both with"""


        text3 = """
Where the projections are parameter matrices WQ
i∈Rdmodel×dk,WK
i∈Rdmodel×dk,WV
i∈Rdmodel×dv
andWO∈Rhdv×dmodel.
"""
        expect3 = ""

        text4 = """
We employ three types of regularization during training:
7Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the
English-to-German and English-to-French newstest2014 tests at a fraction of the training cost.
ModelBLEU Training Cost (FLOPs)
EN-DE EN-FR EN-DE EN-FR
ByteNet [18] 23.75
Deep-Att + PosUnk [39] 39.2 1.0·1020
GNMT + RL [38] 24.6 39.92 2.3·10191.4·1020
ConvS2S [9] 25.16 40.46 9.6·10181.5·1020
MoE [32] 26.03 40.56 2.0·10191.2·1020
Deep-Att + PosUnk Ensemble [39] 40.4 8.0·1020
GNMT + RL Ensemble [38] 26.30 41.16 1.8·10201.1·1021
ConvS2S Ensemble [9] 26.36 41.29 7.7·10191.2·1021
Transformer (base model) 27.3 38.1 3.3·1018
Transformer (big) 28.4 41.8 2.3·1019"""
        expect4 = """7Table 2: The Transformer achieves better BLEU scores than previous state-of-the-art models on the
English-to-German and English-to-French newstest2014 tests at a fraction of the training cost."""

        self.assertEqual(self.content_filter.filter(text1), expect1)
        self.assertEqual(self.content_filter.filter(text2), expect2)
        self.assertEqual(self.content_filter.filter(text3), expect3)
        self.assertEqual(self.content_filter.filter(text4), expect4)

if __name__ == "__main__":
    unittest.main()