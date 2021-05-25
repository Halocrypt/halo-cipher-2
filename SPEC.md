# HaloCipher 2

HaloCipher 2 is a portable substitution cipher (Portable: Supports any mapping of characters to substitute and characters to be substituted more on that later)

## OK how does it work

![But Why](https://quic.ml/why)

So I should tell you, this might be the best time to get your programmer hat on. You theoretically _can_ crack the cipher with tools online, but it's going to get clunky.

With that said, let's get started

## What does it encode

Whatever the mapping you supply to it..but usually you will encounter ASCII Letters only (rest will be passed as it is) (...usually)

## How..

1 thing to keep in mind is, a string CANNOT be encoded with the same VALID_CHARS twice..the behaviour is undefined
Let's see what happens under the hood

```bash
$ python encode.py
> the quick brown fox jump over the lazy dog
<S(0x4a70):126(0x4a70)ES><I(0x4a70):4001,4,12003,0,20005,14,28007,19,36010,0,44012,28,52014,33,60016,0,68018,43,76021,0,84023,52,92025,57,100027,0,108029,66,116031,71,0,76,132036,80,0,85,148040,90,156043,0,164044,100,172047(0x4a70)EI><D(0x4a70):😈🏓Ζ Μइइ😤Ι 🙊Μ🤣Ξ💔 ΡΛ🕶 🏓😤ΞΟ🧠 ΦडढΩ ΗΗ🧠 थ💔🤒Τ 🌏αΗ(0x4a70)ED>
```

Let's fix it a little
![image](https://user-images.githubusercontent.com/29981503/119570218-7099b900-bdcd-11eb-9226-480d308a9e8a.png)

I think that might clear things up.

To sum up

**Each HaloCipher Text has 4 parts**
each part is of the format
<{FORMAT_ID}(0x4a70):{CONTENT}<E{FORMAT_ID>
Where FORMAT_ID could be `S` or `I` or `D`

..What?

1. S - Seed (Metadata)
2. I - Indices (Metadata)
3. D - Data (Actual Encoded Content)

Without the Seed or the indices, you cannot hope to decode the data
(maybe you can, it's not very secure)

# The algorithm

(next will be a lot of expressive pseudo code)
I will be telling you how you can encode a string in halo cipher.. decoding is left as an exercise to the reader.

```
let f(x) be our cipher function
```

important to note that our internal implementation of `f(x)` is NOT pure (idempotent), it relies on random data (the seed can be predictable but we add a randomizing vector)

`let x = INPUT STRING`
the core element now is the `DICTIONARY` and the `SOURCE_LIST`, it is just the list of characters you want to substitute the input with.

for each element of x, we will take the character and the index.
if the character is not in our SOURCE_LIST (usually ascii_letters), we will return it as it is (**spaces are usually not encoded by halocipher**)
next,
before any iteration, we will take all the odd indices and reduce them to the sum of their ascii codes
such as
`ascii_sum = [ord(x) for odd x in INPUT_STRING]`
`let OUT = ""`
now

```
let i = index
let L = X[L] // the letter
```

if i is odd
then

```
let NUM = SOURCE_LIST.indexOf(L) + (seed * (index + 1)
```

and

```
quotient,remainder  = divmod(NUM,LENGTH(DICTIONARY))
OUT+=SHIFT_LIST_BY(quotient,DICTIONARY)[remainder]
```

where SHIFT_LIST_BY rotates the list by `quotient` places

we will store the quotient in another list called `INDICES` (FORMAT_ID = I )`

if `i` is even we will wait (first iteration, we only process odd indices as the output of even indices depends directly on the odd )

if `i` is odd:
`let NUM = SOURCE_LIST.indexOf(i) + (seed * ascii_sum * (index + 1))`
`quotient,remainder = divmod(NUM,LENGTH(DICTIONARY)) OUT+=SHIFT_LIST_BY(quotient,DICTIONARY)[remainder]`
again, we will add the quotient to our list of indices

now that we have our seed, indices and encrypted chunk, we pack the data
(there is no whitespace, just to make it look clear)

```
  "<S(0x4a70):         {seed}          (0x4a70)ES>
  <I(0x4a70):   {INDICES_SEPARATED_BY_COMMAS}  (0x4a70)EI>
<D(0x4a70):     {OUT}     (0x4a70)ED>""
```

now that you know what happens under the hood..go reverse it
