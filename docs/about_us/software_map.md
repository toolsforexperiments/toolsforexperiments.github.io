# The Software Landscape

Our software is spread across four packages, each solving a distinct problem in a computer-controlled physics experiment. They are designed to be used together, but they are also deliberately separable: you can pull in only what you need, and each package's job is narrow enough that it can evolve on its own. This page is a map, a quick orientation to what each package is for, how the pieces depend on each other, and what a typical experiment looks like when you put them together.

Although this stack grew out of the everyday needs of a superconducting-qubit lab, none of it is tied to that setting. The tools are general enough to support any experimental lab whose work consists of repeated, computer-controlled measurements.

The instrument-facing parts of our code sit on top of [QCoDeS](https://microsoft.github.io/Qcodes/), which provides the base abstractions for instruments and parameters. The rest of the stack (the sweep framework, the storage layer, the analysis tools, and the plotting apps) does not require QCoDeS at all, so you are free to adopt only the pieces you find useful, even if QCoDeS is not part of your workflow.

## The packages

### labcore

[labcore](https://toolsforexperiments.github.io/labcore/) is our general-purpose toolkit. It is the part of the stack that does not care what you are measuring; it provides the scaffolding that every kind of experiment needs. If you are writing a new measurement from scratch, labcore is almost certainly the first thing you reach for.

It contains:

- A **measurement and sweep framework** that lets you declare independent and dependent variables and compose sweeps with simple operators. Existing sweeps snap together into larger ones like Lego blocks, so bigger experiments are built out of small, well-tested pieces rather than rewritten from scratch.
- A **structured HDF5 storage layer** (the `DataDict` and `DDH5Writer`) that writes self-describing datasets with units, axes, and metadata. Through `run_and_save_sweep` you can attach arbitrary metadata and auxiliary files (configs, notes, images) alongside the data itself, so the full context of a measurement lives in one folder.
- An **analysis and fitting layer** built on lmfit, with a `Fit` base class and a library of common fit functions, so routine analysis does not need to be reinvented every time. The `DatasetAnalysis` helper then lets you store arbitrary analysis results and derived data next to the original dataset, keeping raw measurement and interpretation together.
- A **protocols layer** for automating and intelligently chaining measurements together, so a multi-step characterization sequence can run end-to-end without hand-holding.
- **Command-line utilities** for live autoplotting and for recovering data from partially-written HDF5 files.

### instrumentserver

[instrumentserver](https://toolsforexperiments.github.io/instrumentserver/) puts QCoDeS instruments on the network. A single process holds and owns the hardware, and any number of clients on the network (Jupyter kernels, measurement scripts, GUIs) can talk to those instruments as if they were local Python objects. The same set of instruments can be shared across different computers on the same network, so a measurement notebook on one machine, a live monitor on another, and a tuning GUI on a third all see a consistent view of the hardware without ever stepping on each other.

It contains:

- A **server** that wraps a QCoDeS station and handles concurrent client requests with per-instrument locking.
- **Client-side proxies** (`Client`, `ProxyInstrument`, `ProxyParameter`) that mirror the native QCoDeS API, so remote instruments feel local to the code using them.
- An **optional Qt GUI** for inspecting the station, watching parameters update in real time, and running a detached server with a visible status window. The server itself can run headless, and a set of generic, customizable client-side widgets is available for building your own instrument-specific UIs.
- A runtime **parameter manager** for holding experiment-level parameters (e.g. qubit frequencies, pulse amplitudes) that are not tied to any one physical instrument.
- **Long-term instrument monitoring** via a Grafana dashboard, so parameters like fridge temperatures, line voltages, or generator outputs can be logged and visualized over hours, days, or months. See the [instrument monitoring guide](https://toolsforexperiments.github.io/instrumentserver/user_guide/instrumentmonitoring.html) for how to set it up.

### plottr

[plottr](https://toolsforexperiments.github.io/plottr/) is, first and foremost, a set of graphical applications you launch to look at your data. Where the other packages focus on producing and organizing data, plottr focuses on looking at it. You typically use it by running one of its programs alongside your measurements, not by importing it from your code.

The main apps are:

- **`plottr-monitr`** for live-monitoring a directory of HDF5 datasets, with plots that update as new data lands on disk.
- **`plottr-inspectr`** for browsing QCoDeS `.db` files and opening datasets from them.
- **`plottr-autoplot-ddh5`** for generating plots automatically from the structure of a DDH5 file.

Underneath the apps, plottr is also a library you can extend when you need something custom. It is built around composable flowchart nodes (selection, filtering, gridding, fitting, plotting), backed by `DataDict` (the data model it shares with labcore), and with plotting backends for matplotlib and pyqtgraph. You reach for this side of plottr when you want to build a new analysis pipeline or embed a plot in a tool of your own, but most day-to-day use is simply launching one of the apps above.

### CQEDToolbox

[CQEDToolbox](https://github.com/toolsforexperiments/CQEDToolbox) is our opinionated library. It is the code **we** actually use, day to day, in Pfafflab to run circuit-QED experiments on superconducting qubits. It is full of the assumptions we make about how our lab operates, what our hardware looks like, and what a sensible measurement sequence is, so it is tuned to work well for us rather than to be universal. It also doubles as a worked example: if you want to see how we put the other three packages together in practice, or how we tend to structure and implement our tools, CQEDToolbox is where to look.

It contains:

- **Measurement protocols** for single-transmon and fluxonium characterization (spectroscopy, Rabi, T1, T2, AllXY, randomized benchmarking) implemented against OPX (Quantum Machines), QICK (Xilinx RFSoC), and VNA-based backends.
- **Custom QCoDeS drivers** for instruments we use that are not covered by the QCoDeS core set (SignalCore generators, Oxford Triton fridges, Yokogawa DC sources, and others).
- **Readout calibration and discrimination** utilities for turning raw IQ shots into qubit-state assignments.
- A **measurement setup harness** (`setup_measurements.py`) that wires everything together: it pulls instrument proxies from instrumentserver, defines the sweep with labcore, runs it, and saves it.

## How they fit together

```
                           ┌────────────┐                         ┌────────────┐
                           │   QCoDeS   │                         │   HDF5 /   │
                           │            │                         │  QCoDeS db │
                           └─────┬──────┘                         └──────┬─────┘
                                 │                                       │
                   ┌─────────────┴──────────────┐                        │
                   │                            │                        │
                   ▼                            ▼                        ▼
          ┌────────────────┐          ┌──────────────────┐        ┌──────────────┐
          │    labcore     │          │ instrumentserver │        │   plottr     │
          │  (sweeps,      │          │  (networked      │        │  (inspect,   │
          │   storage,     │          │   QCoDeS         │        │   plot,      │
          │   analysis)    │          │   instruments)   │        │   analyze)   │
          └───────┬────────┘          └────────┬─────────┘        └──────────────┘
                  │                            │
                  └──────────────┬─────────────┘
                                 │
                                 ▼
    ┌────────────────────────────────────────────────────────────┐
    │                        CQEDToolbox                         │
    │      (circuit-QED protocols, drivers, readout, setup)      │
    └────────────────────────────────────────────────────────────┘
```


The diagram reads top-down as a dependency graph: each arrow points from a foundation to what is built on top of it. At the top, **QCoDeS** is the foundation for everything instrument-related, and the **HDF5 / QCoDeS database files** are the corresponding foundation on the data side, the formats in which experiments get written to disk.

In the middle sit **labcore** and **instrumentserver**, the two reusable, general-purpose pieces. Labcore handles the *"what is the measurement and what does its data look like"* side; instrumentserver handles the *"where does the hardware live and how do I talk to it"* side. They are independent of each other, you can use one without the other, but the two together cover most of what you need to run an experiment.

At the bottom, **CQEDToolbox** consumes both: it uses labcore's sweep and fitting machinery to define its protocols, and it uses instrumentserver's client to reach the hardware. It is the most opinionated of the four packages, and how we actually run our lab.

**plottr** is deliberately off to the side. It does not depend on any of the other three, and it does not participate in data acquisition. It reads the same HDF5 and QCoDeS formats that labcore and QCoDeS write, and does its job (displaying and analyzing data) entirely on its own. The `DataDict` abstraction, now central to labcore, in fact started in plottr and was extracted for wider reuse.

## A typical workflow

A circuit-QED measurement session tends to look like this:

1. **Start the instrument server.** A long-lived instrumentserver process owns all the physical instruments for the fridge (generators, VNA, DC sources, the fridge itself) and exposes them over the network.
2. **Connect a client.** From a Jupyter notebook or a measurement script, you connect an instrumentserver `Client` and get proxies for the instruments you need. They behave exactly like local QCoDeS objects.
3. **Define a measurement.** You use a CQEDToolbox protocol (or a custom measurement written with labcore's decorators) to describe the sweep: what is swept, what is recorded, and how the data is shaped.
4. **Run and save.** The CQEDToolbox harness runs the sweep and uses labcore's `DDH5Writer` to stream the data into a structured HDF5 file, complete with axes, units, and metadata.
5. **Inspect and analyze.** You point `plottr-monitr` at the data directory for live plots during the run, and open `plottr-autoplot-ddh5` or a notebook using labcore's fitting tools for deeper analysis afterward.

Each step uses a different package, but you rarely notice the seams, and that is the point. The packages are separate so that each can be developed, tested, and documented on its own terms, not so that you have to think about them separately as a user.

## Where to go next

- **labcore**: [source](https://github.com/toolsforexperiments/labcore) and [documentation](https://toolsforexperiments.github.io/labcore/)
- **instrumentserver**: [source](https://github.com/toolsforexperiments/instrumentserver) and [documentation](https://toolsforexperiments.github.io/instrumentserver/)
- **plottr**: [source](https://github.com/toolsforexperiments/plottr) and [documentation](https://toolsforexperiments.github.io/plottr/)
- **CQEDToolbox**: [source](https://github.com/toolsforexperiments/CQEDToolbox) (see the repository README for setup and usage)

