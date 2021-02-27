# Basic-context-sensitive-HMM
This small piece of code is a very basic implementation of a HMM (Hidden Markov Model) with a little bit of context sensitivity.

# How to use
Import the Context_HMM class into your code, then feed it a string from which to learn as you instantiate it (it should be a VERY long string). Once the model is built you can simply use the generate() methode to generate a sequence based on the model.

# How it works
In a HMM, each elements knows which elements it can be followed by, and at which probability. In this implementation, I tried adding a bit of context sensitivity by having previous elements (before the current one) influence the element that will be choosen next. The number of previous elements influencing the next element choice is determined by the "context_depth" passed when innitiating a Context_HMM object (Note: A context_depth of 0 will break the model. This wasn't made as a "vanilla" HMM). This is a very basic approach and it isn't particularly optimised, but it does work decently for fairly simple sequences.
