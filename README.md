# Lens X Astrace Natal Chart App

An app that generates natal charts based on a person's birth information. The natal charts are "minted" as [Lens Publications](https://docs.lens.xyz/docs/publication) and the birth information is stored as metadata in the minters Lens [ProfileNFT](https://docs.lens.xyz/docs/profile). The repo is organized into four main components:
- natal chart generation (`./natal-chart-generation`)
- smart contracts (`./blockchain`)
- frontend (`./frontend`)
- deployment code (`./cdk`)

## Table of Contents

- [Table of Contents](#table-of-contents)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
  - [Image Algorithm](#image-algorithm)
  - [Frontend](#frontend)
  - [Smart Contracts](#smart-contracts)
- [Deployment](#deployment)

## Getting Started

### Prerequisites

### Installation

## Usage

### Image Algorithm

For detailed information about the algorithm, [click here](./natal-chart-generation/README.md).

#### Running Locally

Change directory. Set up a virtual environment. Install dependencies. Run script.
```
cd natal-chart-generation
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./natal_chart_cli.py -h
```

#### Testing Locally

#### Running Remotely
See: [Deployment](#deployment)

### Frontend

### Smart Contracts

# Deployment
