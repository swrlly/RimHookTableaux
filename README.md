# Rim Hook Tableaux (ribbon tableaux)

A rim hook tableau of shape $\lambda$ and content $\mu = (\mu_1, \dots, \mu_\ell)$ is a filling of the cells of the Young diagram of $\lambda$ with rim hooks of lenghts $\mu_1, \dots, \mu_\ell$ labeled with $1, \dots, \ell$ such that the removal of the last $i$ rim hooks leaves a valid Young diagram of a smaller integer partition of $i$.

This python script generates all rim hook tableaux of a desired shape and content in French notation. You are allowed to insert the content in any order you'd like; a well known theorem says this [does not change the sign.](https://ajc.maths.uq.edu.au/pdf/73/ajc_v73_p132.pdf)
## How to use
`RimHookTableaux(shape : list, weight : list)`
- `shape`: Desired Young diagram shape of the rim hook tableaux. ith entry is the length of the ith row from the top.
- `weight`: Desired hook length order to insert. The ith entry is the length of the ith inserted hook.

## Example
The Young Diagram below will have shape $(4,3,2,1)$ and content will be inserted in the order $(3,4,2,1)$.
```
rht = RimHookTableaux([1,2,3,4], [3,4,2,1])
rht.PrettyPrint()

[2]
[2, 2]
[1, 2, 3]
[1, 1, 3, 4]

[2]
[2, 2]
[1, 2, 4]
[1, 1, 3, 3]

[3]
[3, 4]
[1, 2, 2]
[1, 1, 2, 2]

[4]
[3, 3]
[1, 2, 2]
[1, 1, 2, 2]
```

Here we can see the hook of length 3 was inserted first, then the hook of length 4, and so on.

```
rht.Sign()
0
```

The signed sum of the rim hook tableaux of shape $(4,3,2,1)$ and content $(3,4,2,1)$ is zero because the first and third tableaux have sign $-1$ while the second and fourth have sign $+1$. The sum is zero.

## Why does this exist?

This code was used in my masters thesis (link soon) to quickly generate all possible rim hook tableaux with arbitrary content. As we were looking for sign reversing involutions, inserting the content in a specific order can minimize the number of rim hook tableaux we would need to account for in the involution.