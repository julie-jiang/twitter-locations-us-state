# twitter-locations-us-state
This is the repo for a short and simple piece of code to find potential US states that matches a freeform location string.

Twitter data usually come with a ``location``, which is a field that users can optionally fill in to indicate their location. This is self-reported and not validated by Twitter. We provide a fuzzy text-matching algorithm that can match these location strings to potential states in the US.

This code does not detect countries, but rather only US states if they are likely in a state in the US.

However, we do provide a helper function ``loc_is_usa`` that detects whether a location string refers to the United States. 

This code was developed for the paper Jiang et al., 2020. [Political polarization drives online conversations about COVID‐19 in the United States](https://onlinelibrary.wiley.com/doi/full/10.1002/hbe2.202)

# Usage
```
python get_countries_states.py "Los Angeles, CA"
```

Which would print:

```
US State for Los Angeles, CA is CA
```

# Citation
If you find this code useful, please cite:

Jiang, J, Chen, E, Yan, S, Lerman, K, Ferrara, E. Political polarization drives online conversations about COVID‐19 in the United States. Human Behavior & Emerging Technologies 2020; 2: 200– 211. https://doi.org/10.1002/hbe2.202

If you use this code in conjunction with Twitter data, please remain compliant with Twitter's [Terms of Service](https://developer.twitter.com/en/developer-terms/agreement-and-policy). 

# How we did it
* We match state names and state abbreviations
* We also document the 25 most populous cities and match them to their states
* We match some popular nicknames for certain cities (e.g. NYC for New York City)
* In the case of any conflicts (e.g. two potential state names in the same string), we won't match it. We'd rather have less false positives than false negatives.
An external human annotator verified that the precision of this algorithm is 96.3%. 
