# MC Diag Boat

A set of utilities for building diagonal boat roads in Minecraft

## Run in Google Colab:

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/ribqahisabsent/mc-diag-boat/blob/main/examples/mc_diag_boat.ipynb)

## Watch the Video

Notebook tutorial included at *timestamp*

[![Diagonal Boat Roads](https://img.youtube.com/vi/88TybxATxiw/0.jpg)](https://www.youtube.com/watch?v=88TybxATxiw)

## A note about installing this package locally

MC Diag Boat is a set of utilities for manipulating 2D vectors in simple ways
with a focus on relevance to Minecraft and the angles Minecraft boats can face.
It also includes generation of [Litematica](https://modrinth.com/mod/litematica)
schematics and some basic UI functionality.
However, the actual user-facing scripts are only included in the `examples/` directory
of this repository.

If you only intend to use the user-facing scripts,
you are best off using the Google Colab notebook, linked [above](#run-in-google-colab).

Installing the module via pip *will not* include the user-facing scripts
and is best done if you intend to write your own scripts which utilize
MC Diag Boat functions.
If you want to modify or contribute to MC Diag Boat, it's best to follow
the [editable installation](#editable-installation) steps
when following the [installation](#installation) instructions.

## Installation

### Install Conda

[Instructions for installing Conda](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

### Create a Conda environment

In a terminal window, run the following command:

```
conda create -n mcdboat -y python=3.11
```

### Activate your Conda environment

In a terminal window, run the following command:

```
conda activate mcdboat
```

### Install MC Diag Boat and dependencies

#### Normal installation

In a terminal window, run the following command:

```
pip install mc-diag-boat
```

#### Editable installation

Alternatively, if you have git installed and want to clone this repository and install
an editable version, run the following commands in the directory you want this
repository to be added to:

```
git clone https://github.com/ribqahisabsent/mc-diag-boat.git
pip install -e mc-diag-boat/.
```

