# fetchctg 

The clinicaltrials.gov is a wonderful resource to explore completed, ongoing and planned clinical trials. However using the APIs can be a bit tedious, especially when there is high level of heretogenity is involved in the results published on the website.

In order to help with this issue., this fetch-ctg library contains helper functions to fetch formatted safety data from the clinicaltrials.gov API.


* Free software: MIT license


## Tutorial
--------


### How to install

```sh
$ pip install fetchctg
```

### Basic Usage

```sh
import ctgfetch as ctf
	
# Get serious adverse events from trial id NCT01859988
df = get_sae("NCT01859988")

# Save non-serious adverse events to excel file in local directory
save_oae("NCT01859988")

# Get non-serious adverse events from trial id NCT01859988
df = get_oae("NCT01859988")

# Save serious adverse events to excel file in local directory
save_sae("NCT01859988")

# Get all (serious and non-serious) adverse events from trial id NCT01859988
df = get_all_ae("NCT01859988")

# Save all (serious and non-serious) adverse events to excel file in local directory
save_all_ae("NCT01859988")
```
