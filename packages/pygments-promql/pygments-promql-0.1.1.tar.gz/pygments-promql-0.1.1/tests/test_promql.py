# -*- coding: utf-8 -*-
"""
    Basic PromQLLexer Tests
    ~~~~~~~~~~~~~~~~~~~~~~~

    :copyright: Copyright 2006-2020 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

import pytest

from pygments.token import Token
from pygments_promql import PromQLLexer


@pytest.fixture(scope="module")
def lexer():
    yield PromQLLexer()


def test_metric(lexer):
    fragment = u"go_gc_duration_seconds"
    tokens = [
        (Token.Name.Variable, "go_gc_duration_seconds"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_metric_one_label(lexer):
    fragment = u'go_gc_duration_seconds{instance="localhost:9090"}'
    tokens = [
        (Token.Name.Variable, "go_gc_duration_seconds"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "instance"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "localhost:9090"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, "}"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_metric_multiple_labels(lexer):
    fragment = u'go_gc_duration_seconds{instance="localhost:9090",job="alertmanager"}'
    tokens = [
        (Token.Name.Variable, "go_gc_duration_seconds"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "instance"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "localhost:9090"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Name.Label, "job"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "alertmanager"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, "}"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_metric_multiple_labels_with_spaces(lexer):
    fragment = (
        u'go_gc_duration_seconds{ instance="localhost:9090",  job="alertmanager" }'
    )
    tokens = [
        (Token.Name.Variable, "go_gc_duration_seconds"),
        (Token.Punctuation, "{"),
        (Token.Text.Whitespace, " "),
        (Token.Name.Label, "instance"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "localhost:9090"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "  "),
        (Token.Name.Label, "job"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "alertmanager"),
        (Token.Punctuation, '"'),
        (Token.Text.Whitespace, " "),
        (Token.Punctuation, "}"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_expression_and_comment(lexer):
    fragment = u'go_gc_duration_seconds{instance="localhost:9090"} # single comment\n'
    tokens = [
        (Token.Name.Variable, "go_gc_duration_seconds"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "instance"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "localhost:9090"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, "}"),
        (Token.Text.Whitespace, " "),
        (Token.Comment.Single, "# single comment"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_function_delta(lexer):
    fragment = u'delta(cpu_temp_celsius{host="zeus"}[2h])'
    tokens = [
        (Token.Keyword.Reserved, "delta"),
        (Token.Operator, "("),
        (Token.Name.Variable, "cpu_temp_celsius"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "host"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "zeus"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, "}"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "2h"),
        (Token.Punctuation, "]"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_function_sum_with_args(lexer):
    fragment = u"sum by (app, proc) (instance_memory_usage_bytes)\n"
    tokens = [
        (Token.Keyword, "sum"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "by"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "("),
        (Token.Name.Label, "app"),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, " "),
        (Token.Name.Label, "proc"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "("),
        (Token.Name.Variable, "instance_memory_usage_bytes"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_function_multi_line(lexer):
    fragment = u"""label_replace(
    sum by (instance) (
        irate(node_disk_read_bytes_total[2m])
    ) / 1024 / 1024,
    "device",
    'disk',
    "instance",
    ".*"
)
"""
    tokens = [
        (Token.Keyword.Reserved, "label_replace"),
        (Token.Operator, "("),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Keyword, "sum"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "by"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "("),
        (Token.Name.Label, "instance"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "("),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "        "),
        (Token.Keyword.Reserved, "irate"),
        (Token.Operator, "("),
        (Token.Name.Variable, "node_disk_read_bytes_total"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "2m"),
        (Token.Punctuation, "]"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "/"),
        (Token.Text.Whitespace, " "),
        (Token.Literal.Number.Integer, "1024"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "/"),
        (Token.Text.Whitespace, " "),
        (Token.Literal.Number.Integer, "1024"),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "device"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "disk"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "instance"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, ".*"),
        (Token.Punctuation, '"'),
        (Token.Text.Whitespace, "\n"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_function_multi_line2(lexer):
    fragment = u"""label_replace(
    avg by(instance)
        (irate(node_cpu_seconds_total{mode = "idle"}[5m] offset 3s)
    ) * 100,
    "device",
    "cpu",
    "instance",
    ".*"
)"""
    tokens = [
        (Token.Keyword.Reserved, "label_replace"),
        (Token.Operator, "("),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Keyword, "avg"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "by"),
        (Token.Operator, "("),
        (Token.Name.Label, "instance"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "        "),
        (Token.Operator, "("),
        (Token.Keyword.Reserved, "irate"),
        (Token.Operator, "("),
        (Token.Name.Variable, "node_cpu_seconds_total"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "mode"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "="),
        (Token.Text.Whitespace, " "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "idle"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, "}"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "5m"),
        (Token.Punctuation, "]"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "offset"),
        (Token.Text.Whitespace, " "),
        (Token.Literal.String, "3s"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "*"),
        (Token.Text.Whitespace, " "),
        (Token.Literal.Number.Integer, "100"),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "device"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "cpu"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "instance"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Text.Whitespace, "\n"),
        (Token.Text.Whitespace, "    "),
        (Token.Punctuation, '"'),
        (Token.Literal.String, ".*"),
        (Token.Punctuation, '"'),
        (Token.Text.Whitespace, "\n"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_complex_exp_double_quotes(lexer):
    fragment = u'(sum(rate(metric_test_app{app="turtle",proc="web"}[2m])) by(node))\n'
    tokens = [
        (Token.Operator, "("),
        (Token.Keyword, "sum"),
        (Token.Operator, "("),
        (Token.Keyword.Reserved, "rate"),
        (Token.Operator, "("),
        (Token.Name.Variable, "metric_test_app"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "app"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "turtle"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, ","),
        (Token.Name.Label, "proc"),
        (Token.Operator, "="),
        (Token.Punctuation, '"'),
        (Token.Literal.String, "web"),
        (Token.Punctuation, '"'),
        (Token.Punctuation, "}"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "2m"),
        (Token.Punctuation, "]"),
        (Token.Operator, ")"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "by"),
        (Token.Operator, "("),
        (Token.Name.Label, "node"),
        (Token.Operator, ")"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_complex_exp_single_quotes(lexer):
    fragment = u"(sum(rate(metric_test_app{app='turtle',proc='web'}[2m])) by(node))\n"
    tokens = [
        (Token.Operator, "("),
        (Token.Keyword, "sum"),
        (Token.Operator, "("),
        (Token.Keyword.Reserved, "rate"),
        (Token.Operator, "("),
        (Token.Name.Variable, "metric_test_app"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "app"),
        (Token.Operator, "="),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "turtle"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, ","),
        (Token.Name.Label, "proc"),
        (Token.Operator, "="),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "web"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, "}"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "2m"),
        (Token.Punctuation, "]"),
        (Token.Operator, ")"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "by"),
        (Token.Operator, "("),
        (Token.Name.Label, "node"),
        (Token.Operator, ")"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_matching_operator_no_regexmatch(lexer):
    fragment = u"metric_test_app{status!~'(4|5)..'}[2m]"
    tokens = [
        (Token.Name.Variable, "metric_test_app"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "status"),
        (Token.Operator, "!~"),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "(4|5).."),
        (Token.Punctuation, "'"),
        (Token.Punctuation, "}"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "2m"),
        (Token.Punctuation, "]"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_by_clause_label_list(lexer):
    fragment = u"sum(irate(metric_histogram{a=~'(1|2|3)',b=~'(1|2|3)',c=~'(1|2|3)',d=~'(1|2|3)'}[1m])) by(a,b,c)"
    tokens = [
        (Token.Keyword, "sum"),
        (Token.Operator, "("),
        (Token.Keyword.Reserved, "irate"),
        (Token.Operator, "("),
        (Token.Name.Variable, "metric_histogram"),
        (Token.Punctuation, "{"),
        (Token.Name.Label, "a"),
        (Token.Operator, "=~"),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "(1|2|3)"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, ","),
        (Token.Name.Label, "b"),
        (Token.Operator, "=~"),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "(1|2|3)"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, ","),
        (Token.Name.Label, "c"),
        (Token.Operator, "=~"),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "(1|2|3)"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, ","),
        (Token.Name.Label, "d"),
        (Token.Operator, "=~"),
        (Token.Punctuation, "'"),
        (Token.Literal.String, "(1|2|3)"),
        (Token.Punctuation, "'"),
        (Token.Punctuation, "}"),
        (Token.Punctuation, "["),
        (Token.Literal.String, "1m"),
        (Token.Punctuation, "]"),
        (Token.Operator, ")"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "by"),
        (Token.Operator, "("),
        (Token.Name.Label, "a"),
        (Token.Punctuation, ","),
        (Token.Name.Label, "b"),
        (Token.Punctuation, ","),
        (Token.Name.Label, "c"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens


def test_without_clause_label_list(lexer):
    fragment = u"sum without (instance,) (http_requests_total)"
    tokens = [
        (Token.Keyword, "sum"),
        (Token.Text.Whitespace, " "),
        (Token.Keyword, "without"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "("),
        (Token.Name.Label, "instance"),
        (Token.Punctuation, ","),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, " "),
        (Token.Operator, "("),
        (Token.Name.Variable, "http_requests_total"),
        (Token.Operator, ")"),
        (Token.Text.Whitespace, "\n"),
    ]
    assert list(lexer.get_tokens(fragment)) == tokens
