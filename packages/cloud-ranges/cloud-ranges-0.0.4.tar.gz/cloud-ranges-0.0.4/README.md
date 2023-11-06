# cloud-ranges

Discover if IP belongs to cloud providers.

## Example

Here there are some usage examples:

```
$ echo 20.236.44.162 | cloud-ranges
20.236.44.162 azure westus2 20.236.0.0/18
```

```
$ echo 20.236.44.162 | cloud-ranges -j
{"cloud": "azure", "services": [], "region": "westus2", "network": "20.236.0.0/18", "target": "20.236.44.162"}
```

## Supported Cloud Providers

- AWS
- GCP
- Azure
- IBM
- DigitalOcean
- IBM Cloud


## Installation

```
pip install cloud-ranges
```
