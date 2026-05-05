# What We Are Working On

These are the ideas we have for where to take Tools for Experiments next. We are not committed to any of them, and the list will probably change as experiments push us in new directions. It is also not exhaustive — bug fixes and small improvements happen continuously and don't show up here.

If anything below would be useful to you, or you'd like to help, open an issue on the relevant repository, reach out, or open a PR directly!

## Right now: documentation, examples, packaging

Our current priority, ahead of new features, is making sure what we already have is well-documented, easy to install, and has at least one good worked example. The packages have grown faster than their public surface, and we want anyone landing on a repository to be able to see what it does and try it out without reading the source.

Concretely:

- **Publishing every package on PyPI**, so installing is `pip install plottr` rather than a clone. labcore, instrumentserver, and plottr are the immediate targets.
- **A documentation and examples audit** across the stack, package by package — every tool gets a worked example and a clear use-case statement, we close the most visible gaps in the docs we already have, and we make a deliberate pass at advertising the pieces that aren't well known yet.
- **A protocol tutorial** that walks through turning an existing measurement script into a `Protocol`, so other groups can adopt the workflow without having to reverse-engineer it from the source.
- **A proper docs page for the instrument-server monitor**, which is one of the more useful things we have built and currently one of the least visible.

## Next: a protocol-driven measurement workflow

The longer-running theme is making `Protocol` an active piece of the measurement workflow rather than a script wrapper. The pieces below build on each other in roughly this order.

- **A parameter-source interface for protocols.** A protocol should be able to take its starting state from `instrumentserver`, a plain config dictionary (including callable values for derived parameters), or anything else that satisfies the interface. This unblocks groups that want to use protocols without buying into the rest of the stack.
- **A plottr-app substrate for protocol GUIs.** plottr already provides the right kind of GUI primitives for live, data-driven applications; protocol GUIs should be built on top of it so users who only want a measurement GUI can use plottr directly.
- **Per-operation GUIs with live updates.** Each operation in a protocol gets a GUI that runs the measurement, populates the analysis, and shows fits as they appear, all reusing structure already encoded in the protocol class.
- **Multi-step protocol GUIs**, with a qubit tune-up sequence as the working demo: one window, several operations chained, raw data, and fits visible side by side as the run progresses.
- **Corrections and next-step suggestions.** When an analysis flags a measurement as failed, the protocol exposes what to try next, so the workflow becomes interactive instead of a one-shot script.

## Also on the bench

Usability and feature work that doesn't fit cleanly under the two themes above:

- **A spreadsheet-style batch editor for the parameter manager**, with keyboard-only navigation and batch import/export — the current GUI is the right shape but slow to use for non-trivial edits.
- **Defining the role and workflow of the instrument-server monitor**, so the docs upgrade mentioned above has something to describe. The functionality is there; the framing is not.

## Further out

Things we expect to turn to once the above settles but aren't actively scoping yet:

- **Run-integrated lab-notebook entries.** Auto-recorded, searchable notes tied to specific measurement runs, surfaced inside the measurement GUI. The shape of this depends on a separate question we are still working through — how to keep our lab notebook sustainable for everyday use.
