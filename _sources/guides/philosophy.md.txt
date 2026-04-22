# Our Philosophy

**ToolsForExperiments** is an organization built around [Pfafflab](https://pfaff.physics.illinois.edu/) at the University of Illinois, together with a small group of collaborators from other labs who already use our code day to day. What holds us together is not a company or a funding line but a shared need: we run computer-controlled physics experiments, and we want the software underneath those experiments to be open, reusable, and ours to shape.

We are a physics group first, with one dedicated software developer. Code is a means to run better experiments, not the product we ship, and that shows in how we work. This page is less a set of rules and more a description of the habits and tradeoffs that fall out of our situation, so that anyone thinking about using or contributing to our tools can see what they are stepping into.

## Small, independent, cohesive

We prefer many small pieces over a few big ones. Each package in the stack does one thing, lives in its own repository, has its own release cycle, and stays useful on its own. You should be able to drop labcore into a codebase that has never seen the rest of our tools, or launch a plottr app against someone else's HDF5 files, and get value out of it without buying into the whole ecosystem.

At the same time we care that the pieces fit. Conventions are shared across the stack (the `DataDict` data model, the way sweeps are described, how metadata is attached), so that when you do use several packages together they feel like one thing, not four things bolted together. Modularity without cohesion is a pile of parts; cohesion without modularity is a trap. We try to stay in between.

## Specific first, generalized as it earns it

New code tends to start very close to whatever concrete problem we were trying to solve that week, whether that is getting a specific measurement running, handling a new kind of data, or smoothing out some part of the daily workflow. We do not plan features on a long roadmap; we let the experiments push, fulfill the need in front of us, and only later, once the same pattern shows up in a second or third place, pull the general-purpose piece out and move it somewhere it can be reused. Things grow where they are actually being used, which keeps us from over-designing for problems that never materialize.

Even so, the split between the general tool and our own implementation of it is something we keep in mind from the start. Over time every useful pattern finds its way into two places: a general-purpose home (usually labcore, or the relevant core package) that anyone can pick up, and an opinionated implementation on top (usually CQEDToolbox) where we are free to bake in assumptions about our hardware and our measurement sequences. The first is reusable; the second is ours.

That discipline is also why we try not to treat our own use case as the universal one. If someone else's lab can use labcore without inheriting our opinions about transmons, fridges, or readout chains, we have done our job.

The downside of working this way is that we can be slow to build things no one has needed yet. The upside is that the parts that do exist tend to be earning their keep.

## Functional first, polished as we go

We make things work first and polish them second. New code tends to start rough, grow alongside the experiment it was written for, and only later get the tests, type hints, cleaner APIs, and documentation it deserves. The recent push in labcore to add proper typing and a test suite is a good example: the library had proved itself useful, so it was time to shore it up. This means you will sometimes find corners of the codebase that are not yet as polished as we would like. We know; we get to them eventually, and contributions that help us get there faster are very welcome.

We do hold a line on quality. Code that ships has to be functional, legible, and roughly consistent with the rest of its package. "Not yet polished" is not a license for something that will not work tomorrow.

## Your data, your environment

Reproducibility is an explicit value, not a byproduct. Every measurement lives in its own folder, and everything inside that folder is considered part of the data: the recorded values themselves, with units and axes on every variable; the metadata attached to the run; and any configs, notebooks, images, or other files that capture the context in which the measurement was taken. Months or years later, you should be able to open that folder and see not just the numbers but the experiment around them, with enough information to analyze and reproduce what happened.

We also want the data itself to stay yours. Our formats are plain HDF5 with documented conventions, readable by anything that reads HDF5. There is no proprietary layer between you and your measurements, and no service you have to keep paying to get at them.

## Data that outlives the tools

We think about durability on a longer horizon than the next grant cycle. A measurement taken today should still be readable in twenty years, even if every package in this stack has been abandoned and all that is left is a folder on a hard drive somewhere. That contract shapes several of our choices: we stick to open, widely-supported formats (HDF5 for numerical data, plain text / JSON / YAML for anything human-readable); we document the conventions we layer on top of those formats in public, so that someone with just the files and a few hours of curiosity can recover the structure; and we avoid storing anything in a form that depends on our own code to be read. If every one of our tools disappeared tomorrow, the data would still be readable, and the context around it still intact.

## Build on the community when we can

We are happy to build on tools that already exist. [QCoDeS](https://microsoft.github.io/Qcodes/) is the foundation for everything instrument-related; [xarray](https://xarray.dev/) has a growing role inside labcore; lmfit handles most of our curve fitting. When something in the ecosystem covers what we need, we use it rather than re-invent it, and we are open to replacing our own code with a community alternative if we are convinced it genuinely covers the full shape of how our users rely on the thing we already have.

That last part is the real bar. We are not attached to our own code for its own sake, but we will not swap out something we understand for something we do not unless we can see that the replacement fits the actual use cases, not just the happy path.

## Working with us

You do not need to be in Pfafflab, or in a circuit-QED lab, to use or contribute to our tools. Any of the following is welcome:

- Opening issues on GitHub for feature ideas, bug reports, or questions about how something is supposed to work.
- Sending pull requests against any of the repositories.
- Emailing us directly if you are trying to adopt the tools and want help getting started, or if you want to talk through whether our stack fits your use case before committing to it.

We are a small team, so response times are human, not instant, but we care about the people who use our code, and we would much rather hear from you than not.
