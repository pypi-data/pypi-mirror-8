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

import numpy as np
from munkres import Munkres

from ..matcher import LabelMatcherWithUnknownSupport
from pyannote.core import Annotation, Unknown
from pyannote.core.matrix import LabelMatrix
from pyannote.algorithms.tagging import DirectTagger

from ..matcher import MATCH_CORRECT, MATCH_CONFUSION, \
    MATCH_MISSED_DETECTION, MATCH_FALSE_ALARM

from ..identification import UEMSupportMixin

REFERENCE_TOTAL = 'reference'
HYPOTHESIS_TOTAL = 'hypothesis'

REGRESSION = 'regression'
IMPROVEMENT = 'improvement'
BOTH_CORRECT = 'both_correct'
BOTH_INCORRECT = 'both_incorrect'


class IdentificationErrorAnalysis(UEMSupportMixin, object):
    """

    Parameters
    ----------
    matcher : `Matcher`, optional
        Defaults to `LabelMatcherWithUnknownSupport` instance
        i.e. two Unknowns are always considered as correct.
    unknown : bool, optional
        Set `unknown` to True (default) to take `Unknown` instances into
        account. Set it to False to get rid of them before evaluation.
    merge_unknowns : bool, optional
        See all `Unknown` instances as one unique label. Defaults to False.
    collar : float, optional
        Duration (in seconds) of collars removed from evaluation around
        boundaries of reference segments.

    """

    def __init__(self, matcher=None, unknown=True, merge_unknowns=False,
                 collar=0.):

        super(IdentificationErrorAnalysis, self).__init__()

        if matcher is None:
            matcher = LabelMatcherWithUnknownSupport()
        self.matcher = matcher
        self.munkres = Munkres()
        self.unknown = unknown
        self.merge_unknowns = merge_unknowns
        self.collar = collar

        self._tagger = DirectTagger()

    def _handle_unknowns(self, reference, hypothesis):

        # gather reference and hypothesis unknown labels
        rUnknown = set([u for u in reference.labels()
                        if isinstance(u, Unknown)])
        hUnknown = set([u for u in hypothesis.labels()
                        if isinstance(u, Unknown)])

        if self.unknown:

            if self.merge_unknowns:

                # create new unique `Unknown` instance label
                unknown = Unknown('?')

                # replace them all by unique unknown label
                translation = {u: unknown for u in rUnknown}
                reference = reference.translate(translation)

                translation = {u: unknown for u in hUnknown}
                hypothesis = hypothesis.translate(translation)

        else:

            reference = reference.subset(rUnknown, invert=True)
            hypothesis = hypothesis.subset(hUnknown, invert=True)

        return reference, hypothesis

    def difference(self, reference, hypothesis, uem=None, uemified=False):
        """Get error analysis as `Annotation`

        Labels are (status, reference_label, hypothesis_label) tuples.
        `status` is either 'correct', 'confusion', 'missed detection' or
        'false alarm'.
        `reference_label` is None in case of 'false alarm'.
        `hypothesis_label` is None in case of 'missed detection'.

        Parameters
        ----------
        uemified : bool, optional
            Returns "uemified" version of reference and hypothesis.
            Defaults to False.

        Returns
        -------
        errors : `Annotation`

        """

        reference, hypothesis = self.uemify(
            reference, hypothesis, uem=uem, collar=self.collar)

        reference, hypothesis = self._handle_unknowns(reference, hypothesis)

        # common (up-sampled) timeline
        common_timeline = reference.get_timeline().union(
            hypothesis.get_timeline())
        common_timeline = common_timeline.segmentation()

        # align reference on common timeline
        R = self._tagger(reference, common_timeline)

        # translate and align hypothesis on common timeline
        H = self._tagger(hypothesis, common_timeline)

        errors = Annotation(uri=reference.uri, modality=reference.modality)

        # loop on all segments
        for segment in common_timeline:

            # list of labels in reference segment
            rlabels = R.get_labels(segment, unknown=self.unknown, unique=False)

            # list of labels in hypothesis segment
            hlabels = H.get_labels(segment, unknown=self.unknown, unique=False)

            _, details = self.matcher(rlabels, hlabels)

            for r, h in details[MATCH_CORRECT]:
                track = errors.new_track(segment, prefix=MATCH_CORRECT)
                errors[segment, track] = (MATCH_CORRECT, r, h)

            for r, h in details[MATCH_CONFUSION]:
                track = errors.new_track(segment, prefix=MATCH_CONFUSION)
                errors[segment, track] = (MATCH_CONFUSION, r, h)

            for r in details[MATCH_MISSED_DETECTION]:
                track = errors.new_track(segment,
                                         prefix=MATCH_MISSED_DETECTION)
                errors[segment, track] = (MATCH_MISSED_DETECTION, r, None)

            for h in details[MATCH_FALSE_ALARM]:
                track = errors.new_track(segment, prefix=MATCH_FALSE_ALARM)
                errors[segment, track] = (MATCH_FALSE_ALARM, None, h)

        if uemified:
            return reference, hypothesis, errors
        else:
            return errors

    def _match_errors(self, before, after):
        b_type, b_ref, b_hyp = before
        a_type, a_ref, a_hyp = after
        return (b_ref == a_ref) * (1 + (b_type == a_type) + (b_hyp == a_hyp))

    def regression(self, reference, before, after, uem=None, uemified=False):

        _, before, errors_before = self.difference(
            reference, before, uem=uem, uemified=True)

        reference, after, errors_after = self.difference(
            reference, after, uem=uem, uemified=True)

        behaviors = Annotation(uri=reference.uri, modality=reference.modality)

        # common (up-sampled) timeline
        common_timeline = errors_after.get_timeline().union(
            errors_before.get_timeline())
        common_timeline = common_timeline.segmentation()

        # align 'before' errors on common timeline
        B = self._tagger(errors_before, common_timeline)

        # align 'after' errors on common timeline
        A = self._tagger(errors_after, common_timeline)

        for segment in common_timeline:

            old_errors = B.get_labels(segment, unique=False)
            new_errors = A.get_labels(segment, unique=False)

            n1 = len(old_errors)
            n2 = len(new_errors)
            n = max(n1, n2)

            match = np.zeros((n, n), dtype=int)
            for i1, e1 in enumerate(old_errors):
                for i2, e2 in enumerate(new_errors):
                    match[i1, i2] = self._match_errors(e1, e2)

            mapping = self.munkres.compute(2 - match)

            for i1, i2 in mapping:

                if i1 >= n1:
                    track = behaviors.new_track(segment,
                                                candidate=REGRESSION,
                                                prefix=REGRESSION)
                    behaviors[segment, track] = (
                        REGRESSION, None, new_errors[i2])

                elif i2 >= n2:
                    track = behaviors.new_track(segment,
                                                candidate=IMPROVEMENT,
                                                prefix=IMPROVEMENT)
                    behaviors[segment, track] = (
                        IMPROVEMENT, old_errors[i1], None)

                elif old_errors[i1][0] == MATCH_CORRECT:

                    if new_errors[i2][0] == MATCH_CORRECT:
                        track = behaviors.new_track(segment,
                                                    candidate=BOTH_CORRECT,
                                                    prefix=BOTH_CORRECT)
                        behaviors[segment, track] = (
                            BOTH_CORRECT, old_errors[i1], new_errors[i2])

                    else:
                        track = behaviors.new_track(segment,
                                                    candidate=REGRESSION,
                                                    prefix=REGRESSION)
                        behaviors[segment, track] = (
                            REGRESSION, old_errors[i1], new_errors[i2])

                else:

                    if new_errors[i2][0] == MATCH_CORRECT:
                        track = behaviors.new_track(segment,
                                                    candidate=IMPROVEMENT,
                                                    prefix=IMPROVEMENT)
                        behaviors[segment, track] = (
                            IMPROVEMENT, old_errors[i1], new_errors[i2])

                    else:
                        track = behaviors.new_track(segment,
                                                    candidate=BOTH_INCORRECT,
                                                    prefix=BOTH_INCORRECT)
                        behaviors[segment, track] = (
                            BOTH_INCORRECT, old_errors[i1], new_errors[i2])

        behaviors = behaviors.smooth()

        if uemified:
            return reference, before, after, behaviors
        else:
            return behaviors

    def matrix(self, reference, hypothesis, uem=None):

        reference, hypothesis, errors = self.difference(
            reference, hypothesis, uem=uem, uemified=True)

        chart = errors.chart()

        # rLabels contains reference labels
        # hLabels contains hypothesis labels confused with a reference label
        # falseAlarmLabels contains false alarm hypothesis labels that do not
        # exist in reference labels // corner case  //

        falseAlarmLabels = set(hypothesis.labels()) - set(reference.labels())
        hLabels = set(reference.labels()) | set(hypothesis.labels())
        rLabels = set(reference.labels())

        # sort these sets of labels
        cmp_func = reference._cmp_labels
        falseAlarmLabels = sorted(falseAlarmLabels, cmp=cmp_func)
        rLabels = sorted(rLabels, cmp=cmp_func)
        hLabels = sorted(hLabels, cmp=cmp_func)

        # append false alarm labels as last 'reference' labels
        # (make sure to mark them as such)
        rLabels = rLabels + [(MATCH_FALSE_ALARM, hLabel)
                             for hLabel in falseAlarmLabels]

        # prepend duration columns before the detailed confusion matrix
        hLabels = [
            REFERENCE_TOTAL, HYPOTHESIS_TOTAL,
            MATCH_CORRECT, MATCH_CONFUSION,
            MATCH_FALSE_ALARM, MATCH_MISSED_DETECTION
        ] + hLabels

        # initialize empty matrix
        matrix = LabelMatrix(
            rows=rLabels, columns=hLabels,
            data=np.zeros((len(rLabels), len(hLabels)))
        )

        # loop on chart
        for (status, rLabel, hLabel), duration in chart:

            # increment correct
            if status == MATCH_CORRECT:
                matrix[rLabel, hLabel] += duration
                matrix[rLabel, MATCH_CORRECT] += duration

            # increment confusion matrix
            if status == MATCH_CONFUSION:
                matrix[rLabel, hLabel] += duration
                matrix[rLabel, MATCH_CONFUSION] += duration
                if hLabel in falseAlarmLabels:
                    matrix[(MATCH_FALSE_ALARM, hLabel), rLabel] += duration
                    matrix[(MATCH_FALSE_ALARM, hLabel), MATCH_CONFUSION] += duration
                else:
                    matrix[hLabel, rLabel] += duration
                    matrix[hLabel, MATCH_CONFUSION] += duration

            if status == MATCH_FALSE_ALARM:
                # hLabel is also a reference label
                if hLabel in falseAlarmLabels:
                    matrix[(MATCH_FALSE_ALARM, hLabel), MATCH_FALSE_ALARM] += duration
                else:
                    matrix[hLabel, MATCH_FALSE_ALARM] += duration

            if status == MATCH_MISSED_DETECTION:
                matrix[rLabel, MATCH_MISSED_DETECTION] += duration

        # total reference and hypothesis duration
        for rLabel in rLabels:

            if isinstance(rLabel, tuple) and rLabel[0] == MATCH_FALSE_ALARM:
                r = 0.
                h = hypothesis.label_duration(rLabel[1])
            else:
                r = reference.label_duration(rLabel)
                h = hypothesis.label_duration(rLabel)

            matrix[rLabel, REFERENCE_TOTAL] = r
            matrix[rLabel, HYPOTHESIS_TOTAL] = h

        return matrix
