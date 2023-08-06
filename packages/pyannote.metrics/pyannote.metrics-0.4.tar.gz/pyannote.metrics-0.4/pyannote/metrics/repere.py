#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2012-2014 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr

from __future__ import unicode_literals

from identification import IDMatcher
from pyannote.base.annotation import Unknown


class REPEREIDMatcher(IDMatcher):
    """
    REPERE ID matcher:
    Two IDs match if:
    * they are both anonymous, or
    * they are both named and equal.

    """

    def __init__(self):
        super(REPEREIDMatcher, self).__init__()

    def __call__(self, identifier1, identifier2):
        return (self.is_anonymous(identifier1) and
                self.is_anonymous(identifier2)) \
            or (identifier1 == identifier2 and
                self.is_named(identifier1) and
                self.is_named(identifier2))

    def ncorrect(self, identifiers1, identifiers2):
        # Slightly faster than inherited .ncorrect() method
        named1 = self.named_from(identifiers1)
        named2 = self.named_from(identifiers2)
        anonymous1 = self.anonymous_from(identifiers1)
        anonymous2 = self.anonymous_from(identifiers2)
        return len(named1 & named2) + min(len(anonymous1), len(anonymous2))

    # ------------------------------------------------------------ #
    def is_anonymous(self, identifier):
        return isinstance(identifier, Unknown) or \
            (isinstance(identifier, str) and
                (identifier[:8] == 'Inconnu_' or
                 identifier[:7] == 'speaker'))

    def anonymous_from(self, identifiers):
        return set([identifier for identifier in identifiers
                    if self.is_anonymous(identifier)])
    # ------------------------------------------------------------ #

    def is_named(self, identifier):
        return not self.is_anonymous(identifier)

    def named_from(self, identifiers):
        return set([identifier for identifier in identifiers
                    if self.is_named(identifier)])

# --------------------------------------------------------------------------- #

from base import BaseMetric
from pyannote.algorithm.tagging.segment import ArgMaxDirectTagger

EGER_TOTAL = 'total'

EGER_REF_NAME = 'total named in reference'
EGER_REF_ANON = 'total anonymous in reference'
EGER_HYP_NAME = 'total named in hypothesis'
EGER_HYP_ANON = 'total anonymous in hypothesis'

EGER_CORRECT_NAME = 'correct named'
EGER_CORRECT_ANON = 'correct anonymous'

EGER_CONFUSION_NAME_NAME = 'confusion named/named'
EGER_CONFUSION_NAME_ANON = 'confusion named/anonymous'
EGER_CONFUSION_ANON_NAME = 'confusion anonymous/named'

EGER_FALSE_ALARM_NAME = 'false alarm named'
EGER_FALSE_ALARM_ANON = 'false alarm anonymous'

EGER_MISS_NAME = 'miss named'
EGER_MISS_ANON = 'miss anonymous'

EGER_NAME = 'estimated global error rate'


class EstimatedGlobalErrorRate(BaseMetric):
    """
    Estimated Global Error Rate

    Pour chaque image annotée (annotated timeline) de la reference, la liste
    des personnes présentes et/ou parlant à l’instant associé est constituée,
    et ce du point de vue référence et du point de vue système.

    Ces deux listes sont comparées en associant les personnes une à une, chaque
    personne ne pouvant être associée au plus qu’une fois. Une association
    entre deux personnes nommées compte pour un correct, tout comme
    l’association entre deux anonymes. L’association entre deux personnes avec
    des noms différents ou entre un nommé et un anonyme donne une confusion.
    Chaque personne de l’hypothèse non associée compte pour une fausse alarme,
    et chaque personne de la référence non associée pour un oubli. Un coût est
    associé par confusion, et un par oubli/fausse alarme.

    De toutes les associations possibles est choisie celle qui donne le coût
    total (erreur pour l’image) le plus faible.
    La somme de tous ces comptes d’erreur par image permet d’obtenir le nombre
    d’erreurs global. Le nombre global d’entrées attendues est lui aussi
    comptabilisé en cumulant le nombre de personnes présentes dans la référence
    à chaque image. Le taux d’erreur est alors le nombre d’erreurs global
    divisé par le nombre global d’entrées attendues.

    Nous nous proposons d’utiliser un coût de 1 pour oubli/fausse alarme et de
    0,5 pour confusion.

    Example

    >>> xgtf = XGTFParser(path2xgtf, path2idx)
    >>> reference = xgtf.head()
    >>> annotated = xgtf.annotated()
    >>> hypothesis = my_super_algorithm()
    >>> eger = EstimatedGlobalErrorRate()
    >>> error_rate = eger(reference, hypothesis, annotated=annotated)

    """

    @classmethod
    def metric_name(cls):
        return EGER_NAME

    @classmethod
    def metric_components(cls):
        return [EGER_CONFUSION_NAME_NAME, EGER_CONFUSION_NAME_ANON,
                EGER_CONFUSION_ANON_NAME,
                EGER_FALSE_ALARM_NAME, EGER_FALSE_ALARM_ANON,
                EGER_MISS_NAME, EGER_MISS_ANON,
                EGER_REF_NAME, EGER_REF_ANON, EGER_TOTAL,
                EGER_HYP_NAME, EGER_HYP_ANON,
                EGER_CORRECT_NAME, EGER_CORRECT_ANON]

    def __init__(self, confusion=1., anonymous=False):

        super(EstimatedGlobalErrorRate, self).__init__()
        self.matcher = REPEREIDMatcher()
        self.confusion = confusion
        self.anonymous = anonymous
        self.tagger = ArgMaxDirectTagger()

    def __get_precision(self):
        if self[EGER_HYP_NAME] > 0:
            precision = 1. * self[EGER_CORRECT_NAME] / self[EGER_HYP_NAME]
        else:
            precision = 1.
        return precision
    precision = property(fget=__get_precision)
    """Overall precision."""

    def __get_recall(self):
        if self[EGER_HYP_NAME] > 0:
            recall = 1. * self[EGER_CORRECT_NAME] / self[EGER_REF_NAME]
        else:
            recall = 1.
        return recall
    recall = property(fget=__get_recall)
    """Overall recall."""

    def __get_fmeasure(self):
        precision = self.precision
        recall = self.recall
        return 2 * precision * recall / (precision + recall)
    f_measure = property(fget=__get_fmeasure)
    """Overall F1-measure."""

    def _get_details(self, reference, hypothesis, annotated=None):

        if annotated is None:
            raise ValueError("'annotated' argument is mandatory.")

        detail = self._init_details()

        reference = self.tagger(reference, annotated)
        hypothesis = self.tagger(hypothesis, annotated)

        for frame in annotated:

            ref = reference.get_labels(frame)
            hyp = hypothesis.get_labels(frame)

            if not self.anonymous:
                ref = self.matcher.named_from(ref)
                hyp = self.matcher.named_from(hyp)

            name_ref = self.matcher.named_from(ref)
            name_hyp = self.matcher.named_from(hyp)
            detail[EGER_REF_NAME] += len(name_ref)
            detail[EGER_HYP_NAME] += len(name_hyp)

            anon_ref = ref - name_ref
            anon_hyp = hyp - name_hyp
            detail[EGER_REF_ANON] += len(anon_ref)
            detail[EGER_HYP_ANON] += len(anon_hyp)

            detail[EGER_TOTAL] += detail[EGER_REF_NAME] + detail[EGER_REF_ANON]

            # correct named/named matches
            detail[EGER_CORRECT_NAME] += len(name_ref & name_hyp)
            for known in name_ref & name_hyp:
                name_ref.remove(known)
                name_hyp.remove(known)

            # correct anonymous/anonymous matches
            n = min(len(anon_ref), len(anon_hyp))
            detail[EGER_CORRECT_ANON] += n
            for i in range(n):
                anon_ref.pop()
                anon_hyp.pop()

            # named/named confusion
            n = min(len(name_ref), len(name_hyp))
            detail[EGER_CONFUSION_NAME_NAME] += n
            for i in range(n):
                name_ref.pop()
                name_hyp.pop()

            # named/anonymous confusion
            n = min(len(name_ref), len(anon_hyp))
            detail[EGER_CONFUSION_NAME_ANON] += n
            for i in range(n):
                name_ref.pop()
                anon_hyp.pop()

            # anonymous/named confusion
            n = min(len(anon_ref), len(name_hyp))
            detail[EGER_CONFUSION_ANON_NAME] += n
            for i in range(n):
                anon_ref.pop()
                name_hyp.pop()

            # miss
            detail[EGER_MISS_NAME] += len(name_ref)
            detail[EGER_MISS_ANON] += len(anon_ref)

            # false alarm
            detail[EGER_FALSE_ALARM_NAME] += len(name_hyp)
            detail[EGER_FALSE_ALARM_ANON] += len(anon_hyp)

        return detail

    def _get_rate(self, detail):
        numerator = self.confusion * detail[EGER_CONFUSION_NAME_NAME] + \
            self.confusion * detail[EGER_CONFUSION_NAME_ANON] + \
            self.confusion * detail[EGER_CONFUSION_ANON_NAME] + \
            1. * detail[EGER_FALSE_ALARM_NAME] + \
            1. * detail[EGER_FALSE_ALARM_ANON] + \
            1. * detail[EGER_MISS_NAME] + \
            1. * detail[EGER_MISS_ANON]
        denominator = 1. * detail[EGER_REF_NAME] + \
            1. * detail[EGER_REF_ANON]
        if denominator == 0.:
            if numerator == 0:
                return 0.
            else:
                return 1.
        else:
            return numerator/denominator

    def _pretty(self, detail):

        string = ""

        ref_name = detail[EGER_REF_NAME]
        ref_anon = detail[EGER_REF_ANON]
        string += "  - reference entries: %d (%d named, %d anonymous)\n" % \
                  (ref_name+ref_anon, ref_name, ref_anon)

        hyp_name = detail[EGER_HYP_NAME]
        hyp_anon = detail[EGER_HYP_ANON]
        string += "  - hypothesis entries: %d (%d named, %d anonymous)\n" % \
                  (hyp_name+hyp_anon, hyp_name, hyp_anon)

        correct_name = detail[EGER_CORRECT_NAME]
        correct_anon = detail[EGER_CORRECT_ANON]
        string += "  - correct: %d (%d named, %d anonymous)\n" % \
                  (correct_name+correct_anon, correct_name, correct_anon)

        confusion_nn = detail[EGER_CONFUSION_NAME_NAME]
        confusion_na = detail[EGER_CONFUSION_NAME_ANON]
        confusion_an = detail[EGER_CONFUSION_ANON_NAME]
        string += "  - confusions: %d (%d n-n, %d n-a, %d a-n)\n" % \
                  (confusion_nn+confusion_na+confusion_an,
                   confusion_nn, confusion_na, confusion_an)

        miss_name = detail[EGER_MISS_NAME]
        miss_anon = detail[EGER_MISS_ANON]
        string += "  - miss: %d (%d named, %d anonymous)\n" % \
                  (miss_name+miss_anon, miss_name, miss_anon)

        fa_name = detail[EGER_FALSE_ALARM_NAME]
        fa_anon = detail[EGER_FALSE_ALARM_ANON]
        string += "  - fa: %d (%d named, %d anonymous)\n" % \
                  (fa_name+fa_anon, fa_name, fa_anon)

        if detail[EGER_HYP_NAME] > 0:
            precision = 1. * detail[EGER_CORRECT_NAME] / detail[EGER_HYP_NAME]
        else:
            precision = 1.
        string += "  - precision (named): %.2f %%\n" % (100*precision)

        if detail[EGER_HYP_NAME] > 0:
            recall = 1. * detail[EGER_CORRECT_NAME] / detail[EGER_REF_NAME]
        else:
            recall = 1.
        string += "  - recall (named): %.2f %%\n" % (100*recall)

        if (precision + recall > 0):
            fmeasure = 2 * precision * recall / (precision + recall)
        else:
            fmeasure = 0.
        string += "  - F1-measure (named): %.2f %%\n" % (100*fmeasure)

        string += "  - EGER: %.2f %%\n" % (100*detail[self.name])

        return string


if __name__ == "__main__":
    import doctest
    doctest.testmod()
