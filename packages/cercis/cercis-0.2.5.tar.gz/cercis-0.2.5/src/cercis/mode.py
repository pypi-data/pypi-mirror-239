"""Data structures configuring Black behavior.

Mostly around Python language feature support per version and Black configuration
chosen by the user.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from hashlib import sha256
from operator import attrgetter
from typing import Dict, Final, Set
from warnings import warn

from cercis.const import (
    DEFAULT_BASE_INDENTATION_SPACES,
    DEFAULT_CLOSING_BRACKET_EXTRA_INDENT,
    DEFAULT_COLLAPSE_NESTED_BRACKETS,
    DEFAULT_FUNCTION_DEFINITION_EXTRA_INDENT,
    DEFAULT_KEEP_BLANK_LINES_IN_BRACKETS,
    DEFAULT_LINE_LENGTH,
    DEFAULT_OTHER_LINE_CONTINUATION_EXTRA_INDENT,
    DEFAULT_SINGLE_QUOTE,
    DEFAULT_TAB_WIDTH,
    DEFAULT_USE_TABS,
    DEFAULT_WRAP_COMMENTS,
    DEFAULT_WRAP_LINE_WITH_LONG_STRING,
    DEFAULT_WRAP_PRAGMA_COMMENTS,
)


class TargetVersion(Enum):
    PY33 = 3
    PY34 = 4
    PY35 = 5
    PY36 = 6
    PY37 = 7
    PY38 = 8
    PY39 = 9
    PY310 = 10
    PY311 = 11
    PY312 = 12


class Feature(Enum):
    F_STRINGS = 2
    NUMERIC_UNDERSCORES = 3
    TRAILING_COMMA_IN_CALL = 4
    TRAILING_COMMA_IN_DEF = 5
    # The following two feature-flags are mutually exclusive, and exactly one should be
    # set for every version of python.
    ASYNC_IDENTIFIERS = 6
    ASYNC_KEYWORDS = 7
    ASSIGNMENT_EXPRESSIONS = 8
    POS_ONLY_ARGUMENTS = 9
    RELAXED_DECORATORS = 10
    PATTERN_MATCHING = 11
    UNPACKING_ON_FLOW = 12
    ANN_ASSIGN_EXTENDED_RHS = 13
    EXCEPT_STAR = 14
    VARIADIC_GENERICS = 15
    DEBUG_F_STRINGS = 16
    PARENTHESIZED_CONTEXT_MANAGERS = 17
    TYPE_PARAMS = 18
    FORCE_OPTIONAL_PARENTHESES = 50

    # __future__ flags
    FUTURE_ANNOTATIONS = 51


FUTURE_FLAG_TO_FEATURE: Final = {
    "annotations": Feature.FUTURE_ANNOTATIONS,
}


VERSION_TO_FEATURES: Dict[TargetVersion, Set[Feature]] = {
    TargetVersion.PY33: {Feature.ASYNC_IDENTIFIERS},
    TargetVersion.PY34: {Feature.ASYNC_IDENTIFIERS},
    TargetVersion.PY35: {Feature.TRAILING_COMMA_IN_CALL, Feature.ASYNC_IDENTIFIERS},
    TargetVersion.PY36: {
        Feature.F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_IDENTIFIERS,
    },
    TargetVersion.PY37: {
        Feature.F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_KEYWORDS,
        Feature.FUTURE_ANNOTATIONS,
    },
    TargetVersion.PY38: {
        Feature.F_STRINGS,
        Feature.DEBUG_F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_KEYWORDS,
        Feature.FUTURE_ANNOTATIONS,
        Feature.ASSIGNMENT_EXPRESSIONS,
        Feature.POS_ONLY_ARGUMENTS,
        Feature.UNPACKING_ON_FLOW,
        Feature.ANN_ASSIGN_EXTENDED_RHS,
    },
    TargetVersion.PY39: {
        Feature.F_STRINGS,
        Feature.DEBUG_F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_KEYWORDS,
        Feature.FUTURE_ANNOTATIONS,
        Feature.ASSIGNMENT_EXPRESSIONS,
        Feature.RELAXED_DECORATORS,
        Feature.POS_ONLY_ARGUMENTS,
        Feature.UNPACKING_ON_FLOW,
        Feature.ANN_ASSIGN_EXTENDED_RHS,
        Feature.PARENTHESIZED_CONTEXT_MANAGERS,
    },
    TargetVersion.PY310: {
        Feature.F_STRINGS,
        Feature.DEBUG_F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_KEYWORDS,
        Feature.FUTURE_ANNOTATIONS,
        Feature.ASSIGNMENT_EXPRESSIONS,
        Feature.RELAXED_DECORATORS,
        Feature.POS_ONLY_ARGUMENTS,
        Feature.UNPACKING_ON_FLOW,
        Feature.ANN_ASSIGN_EXTENDED_RHS,
        Feature.PARENTHESIZED_CONTEXT_MANAGERS,
        Feature.PATTERN_MATCHING,
    },
    TargetVersion.PY311: {
        Feature.F_STRINGS,
        Feature.DEBUG_F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_KEYWORDS,
        Feature.FUTURE_ANNOTATIONS,
        Feature.ASSIGNMENT_EXPRESSIONS,
        Feature.RELAXED_DECORATORS,
        Feature.POS_ONLY_ARGUMENTS,
        Feature.UNPACKING_ON_FLOW,
        Feature.ANN_ASSIGN_EXTENDED_RHS,
        Feature.PARENTHESIZED_CONTEXT_MANAGERS,
        Feature.PATTERN_MATCHING,
        Feature.EXCEPT_STAR,
        Feature.VARIADIC_GENERICS,
    },
    TargetVersion.PY312: {
        Feature.F_STRINGS,
        Feature.DEBUG_F_STRINGS,
        Feature.NUMERIC_UNDERSCORES,
        Feature.TRAILING_COMMA_IN_CALL,
        Feature.TRAILING_COMMA_IN_DEF,
        Feature.ASYNC_KEYWORDS,
        Feature.FUTURE_ANNOTATIONS,
        Feature.ASSIGNMENT_EXPRESSIONS,
        Feature.RELAXED_DECORATORS,
        Feature.POS_ONLY_ARGUMENTS,
        Feature.UNPACKING_ON_FLOW,
        Feature.ANN_ASSIGN_EXTENDED_RHS,
        Feature.PARENTHESIZED_CONTEXT_MANAGERS,
        Feature.PATTERN_MATCHING,
        Feature.EXCEPT_STAR,
        Feature.VARIADIC_GENERICS,
        Feature.TYPE_PARAMS,
    },
}


def supports_feature(target_versions: Set[TargetVersion], feature: Feature) -> bool:
    return all(feature in VERSION_TO_FEATURES[version] for version in target_versions)


class Preview(Enum):
    """Individual preview style features."""

    add_trailing_comma_consistently = auto()
    blank_line_after_nested_stub_class = auto()
    blank_line_between_nested_and_def_stub_file = auto()
    hex_codes_in_unicode_sequences = auto()
    improved_async_statements_handling = auto()
    multiline_string_handling = auto()
    no_blank_line_before_class_docstring = auto()
    prefer_splitting_right_hand_side_of_assignments = auto()
    # NOTE: string_processing requires wrap_long_dict_values_in_parens
    # for https://github.com/psf/black/issues/3117 to be fixed.
    string_processing = auto()
    parenthesize_conditional_expressions = auto()
    parenthesize_long_type_hints = auto()
    respect_magic_trailing_comma_in_return_type = auto()
    skip_magic_trailing_comma_in_subscript = auto()
    wrap_long_dict_values_in_parens = auto()
    wrap_multiple_context_managers_in_parens = auto()
    dummy_implementations = auto()
    walrus_subscript = auto()
    module_docstring_newlines = auto()
    accept_raw_docstrings = auto()
    fix_power_op_line_length = auto()
    hug_parens_with_braces_and_square_brackets = auto()
    allow_empty_first_line_before_new_block_or_comment = auto()
    single_line_format_skip_with_multiple_comments = auto()
    long_case_block_line_splitting = auto()


class Deprecated(UserWarning):
    """Visible deprecation warning."""


@dataclass
class Mode:
    target_versions: Set[TargetVersion] = field(default_factory=set)
    line_length: int = DEFAULT_LINE_LENGTH
    string_normalization: bool = True
    is_pyi: bool = False
    is_ipynb: bool = False
    skip_source_first_line: bool = False
    magic_trailing_comma: bool = True
    experimental_string_processing: bool = False
    python_cell_magics: Set[str] = field(default_factory=set)
    preview: bool = False
    function_definition_extra_indent: bool = DEFAULT_FUNCTION_DEFINITION_EXTRA_INDENT
    closing_bracket_extra_indent: bool = DEFAULT_CLOSING_BRACKET_EXTRA_INDENT
    single_quote: bool = DEFAULT_SINGLE_QUOTE
    wrap_line_with_long_string: bool = DEFAULT_WRAP_LINE_WITH_LONG_STRING
    collapse_nested_brackets: bool = DEFAULT_COLLAPSE_NESTED_BRACKETS
    wrap_pragma_comments: bool = DEFAULT_WRAP_PRAGMA_COMMENTS
    wrap_comments: bool = DEFAULT_WRAP_COMMENTS
    keep_blank_lines_in_brackets: bool = DEFAULT_KEEP_BLANK_LINES_IN_BRACKETS
    base_indentation_spaces: int = DEFAULT_BASE_INDENTATION_SPACES
    other_line_continuation_extra_indent: bool = (
        DEFAULT_OTHER_LINE_CONTINUATION_EXTRA_INDENT
    )
    use_tabs: bool = DEFAULT_USE_TABS
    tab_width: int = DEFAULT_TAB_WIDTH

    def __post_init__(self) -> None:
        if self.experimental_string_processing:
            warn(
                "`experimental string processing` has been included in `preview`"
                " and deprecated. Use `preview` instead.",
                Deprecated,
            )

    def __contains__(self, feature: Preview) -> bool:
        """
        Provide `Preview.FEATURE in Mode` syntax that mirrors the ``preview`` flag.

        The argument is not checked and features are not differentiated.
        They only exist to make development easier by clarifying intent.
        """
        if feature is Preview.string_processing:
            return self.preview or self.experimental_string_processing
        return self.preview

    def get_cache_key(self) -> str:
        if self.target_versions:
            version_str = ",".join(
                str(version.value)
                for version in sorted(self.target_versions, key=attrgetter("value"))
            )
        else:
            version_str = "-"
        parts = [
            version_str,
            str(self.line_length),
            str(int(self.string_normalization)),
            str(int(self.is_pyi)),
            str(int(self.is_ipynb)),
            str(int(self.skip_source_first_line)),
            str(int(self.magic_trailing_comma)),
            str(int(self.experimental_string_processing)),
            str(int(self.preview)),
            sha256((",".join(sorted(self.python_cell_magics))).encode()).hexdigest(),
        ]
        return ".".join(parts)
