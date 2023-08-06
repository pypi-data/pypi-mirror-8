BUILD graph rules
=================

A plugin for the pants build system to add lightweight validation of
graph rules.

Motivation
----------

Pants is great for building a variety of unrelated projects that all
reside in single monolithic repository. While this can make code-reuse,
refactoring, etc all much easier, it can also make it easier to
introduce undesireable dependencies between libraries that would be
impossible, or at least much more obvious, when using separate
repositories and explicitly published artifacts. Maintaining good
dependency hygine can be hard to enforce by hand as transitive
dependency graphs become larger so adding machine-readable rules to
targets allows automatic validation.

Rules
-----

Rules are written in terms of tags. A target can specify a rule such as
"all targets that transively depend on this target must have tag 'foo'".
Rules can require or ban a given tag, either in the dependencies or the
dependees of a target.

``dependencies_cannot_have:foo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A target can require all targets in its transitive dependencies not have
a particular tag. This can be useful to make sure a target never
depends, even indirectly, on code that uses a particular library or
service or to keep different subtrees separate.

``dependencies_must_have:foo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

A target can require all targets in its transitive dependencies have (a
particular tag. This can be useful to maintain a subtree of "common"
code that only depends on other "common" libs and does not develop deps
on feature code.

``dependees_must_have:foo``
^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a target wants to control what targets depend on it, form
``dependees_must_have:foo`` such that targets must have tag ``foo`` in
order to depend on it, or a ``PrivacyViolation`` will be thrown. This
can be particularly useful to restrict edges into a feature-specific
subtree, much like "private" or other visibility modifies in many
programming languages.

The ``exempt`` Tag
^^^^^^^^^^^^^^^^^^

Targets with tag ``exempt`` are not checked for rule violations and do
not cause rule violations in other targets. Examples: - a target *A*
with ``dependencies_must_have:foo`` can depend on a target *B* which has
``exempt`` even though *B* does not have ``foo``. - a target *A* with
``exempt`` can depend on a target *B* which has
``dependees_must_have:foo`` even though *A* does not have ``foo``.

Automatic Tagging
-----------------

Rather than mark every target in its BUILD file with a given tag or
rule, some tags can be inferred from directory structure. The ``tag``
task can add tags to targets based on their path prefix, based on
configuration in pants.ini.

If, for example, you had a directory ``lib/common`` for reusable, common
libs, it might make sense to automatically add the tag ``common`` to
every target in that subtree as well as the rule
``dependencies_must_have:common`` to prevent outbound edges into
non-common code. That might look like:

::

    [target-tags]
    by-prefix:  {
        'lib/common': ['common', 'dependencies_must_have:common'],
      }

Product Types
-------------

The ``tag`` Task provides ``tagged_build_graph``.

The ``validate`` task requires ``tagged_build_graph`` and provides
``validated_build_graph``.

A noop *TriggerValidation* Task, which requires
``validated_build_graph``, is installed in ``bootstrap`` with
``first=True``, to trigger validation as early as possible (to get
errors to the user before embarking on a potentially lengthy compile).
