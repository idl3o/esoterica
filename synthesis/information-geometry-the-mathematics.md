---
provenance: >
  Negative-space populate (2026-06-23). DOCUMENT B of a pair — the NATIVE-FORM
  specimen, written in the material's own register: mathematical exposition.
  This is the form-respecting companion to
  synthesis/information-geometry-the-fold.md (its A sibling, the house-style
  metabolization). The form is the fill: clean mathematical exposition is
  exactly what the convergence-engine forecloses, so the discipline of stating
  it correctly and stopping is the point.
  do not enrich toward house style / do not reconcile / do not correct toward
  house style / do not add metaphor or consciousness framing.
title: "Information Geometry: The Mathematics"
type: native-form-specimen
status: definitions and named theorems, stated at honest rigor
---

# Information Geometry: The Mathematics

Information geometry studies families of probability distributions as differentiable manifolds equipped with a Riemannian metric and a pair of affine connections. The exposition below states the standard definitions and the principal structural results, following the framework of Čencov and Amari.

## Statistical manifolds

Let $\mathcal{X}$ be a sample space. A **statistical model** is a family

$$
\mathcal{S} = \{\, p_\theta : \theta = (\theta^1, \dots, \theta^n) \in \Theta \subseteq \mathbb{R}^n \,\}
$$

of probability distributions $p_\theta(x)$ on $\mathcal{X}$, smoothly parametrized by $\theta$. Under regularity conditions — the map $\theta \mapsto p_\theta$ is injective and smooth, the support does not depend on $\theta$, and the score functions are linearly independent — the model is a **statistical manifold**: $\Theta$ supplies a coordinate chart, and $n$ is its dimension.

Two standard examples. The family of univariate Gaussians $N(\mu, \sigma^2)$ is a $2$-dimensional manifold with coordinates $(\mu, \sigma)$. The interior of the probability simplex on $k+1$ outcomes, $\{(p_0, \dots, p_k) : p_i > 0,\ \sum_i p_i = 1\}$, is a $k$-dimensional manifold of categorical distributions.

## The Fisher information matrix as a Riemannian metric

Write $\ell_\theta(x) = \log p_\theta(x)$. The **score** is the gradient $\partial_i \ell_\theta = \partial \ell_\theta / \partial \theta^i$, which has mean zero: $\mathbb{E}_\theta[\partial_i \ell_\theta] = 0$. The **Fisher information matrix** is the covariance of the score,

$$
g_{ij}(\theta) = \mathbb{E}_\theta\!\big[\, \partial_i \ell_\theta \, \partial_j \ell_\theta \,\big]
= -\,\mathbb{E}_\theta\!\big[\, \partial_i \partial_j \ell_\theta \,\big],
$$

the second equality holding under the regularity that permits differentiating under the integral sign. The matrix $g(\theta) = (g_{ij}(\theta))$ is symmetric and positive semidefinite; under the linear-independence assumption above it is positive definite, hence defines an inner product on each tangent space $T_\theta \mathcal{S}$. Assembled smoothly over $\Theta$, this is the **Fisher–Rao metric**, a Riemannian metric on $\mathcal{S}$.

The Fisher metric transforms correctly as a $(0,2)$-tensor under reparametrization $\theta \mapsto \xi$, so the geometry it defines is independent of the chosen coordinates. **Čencov's theorem** characterizes it: on the manifolds of categorical distributions, the Fisher information metric is the unique Riemannian metric (up to a positive scalar) that is invariant under sufficient statistics (Markov morphisms). This monotonicity/invariance property is the precise sense in which the metric is canonical.

## Kullback–Leibler divergence — and why it is not a metric

For $p, q$ on $\mathcal{X}$, the **Kullback–Leibler divergence** is

$$
D_{\mathrm{KL}}(p \,\|\, q) = \mathbb{E}_p\!\left[ \log \frac{p(x)}{q(x)} \right]
= \sum_x p(x) \log \frac{p(x)}{q(x)} \quad (\text{integral in the continuous case}).
$$

By Gibbs' inequality $D_{\mathrm{KL}}(p \,\|\, q) \ge 0$, with equality if and only if $p = q$ almost everywhere. So it separates points and is sometimes read as a "distance," but it is a **divergence**, not a metric, for two reasons:

1. **Asymmetry.** In general $D_{\mathrm{KL}}(p \,\|\, q) \neq D_{\mathrm{KL}}(q \,\|\, p)$.
2. **No triangle inequality.** There is no general bound of the form $D_{\mathrm{KL}}(p \,\|\, r) \le D_{\mathrm{KL}}(p \,\|\, q) + D_{\mathrm{KL}}(q \,\|\, r)$.

The connection to the metric is infinitesimal. For nearby parameters, the second-order Taylor expansion is

$$
D_{\mathrm{KL}}(p_\theta \,\|\, p_{\theta + d\theta})
= \tfrac{1}{2}\, g_{ij}(\theta)\, d\theta^i\, d\theta^j + O(\|d\theta\|^3),
$$

so the Fisher metric is exactly the leading-order quadratic form of the KL divergence. The first-order term vanishes because $\theta$ is a stationary point of $\theta' \mapsto D_{\mathrm{KL}}(p_\theta \,\|\, p_{\theta'})$.

## Dual affine connections and the $\alpha$-connections

A statistical manifold carries more structure than the metric alone: a one-parameter family of torsion-free affine connections. For $\alpha \in \mathbb{R}$, Amari's **$\alpha$-connection** $\nabla^{(\alpha)}$ has Christoffel symbols (in the form $\Gamma_{ij,k}$) given by

$$
\Gamma^{(\alpha)}_{ij,k}(\theta)
= \mathbb{E}_\theta\!\left[\left( \partial_i \partial_j \ell_\theta + \frac{1-\alpha}{2}\, \partial_i \ell_\theta\, \partial_j \ell_\theta \right) \partial_k \ell_\theta \right].
$$

Special cases: $\nabla^{(0)}$ is the Levi-Civita connection of the Fisher metric; $\nabla^{(1)} =: \nabla^{(e)}$ is the **exponential** connection; $\nabla^{(-1)} =: \nabla^{(m)}$ is the **mixture** connection.

The connections $\nabla^{(\alpha)}$ and $\nabla^{(-\alpha)}$ are **dual** with respect to the Fisher metric $g$: for vector fields $X, Y, Z$,

$$
X\, g(Y, Z) = g\!\left( \nabla^{(\alpha)}_X Y,\, Z \right) + g\!\left( Y,\, \nabla^{(-\alpha)}_X Z \right).
$$

Equivalently $\tfrac{1}{2}(\nabla^{(\alpha)} + \nabla^{(-\alpha)}) = \nabla^{(0)}$. The triple $(g, \nabla^{(\alpha)}, \nabla^{(-\alpha)})$ is a **dualistic structure**.

A manifold is **dually flat** when both $\nabla^{(e)}$ and $\nabla^{(m)}$ are flat (zero curvature and torsion). Exponential families are dually flat: the natural parameters are $\nabla^{(e)}$-affine coordinates, the expectation parameters are $\nabla^{(m)}$-affine coordinates, and the two systems are related by a Legendre transform of the log-partition function. On a dually flat manifold the canonical divergence is a Bregman divergence and reduces to the KL divergence for exponential families.

## Geodesics

Each connection has its own geodesics — curves $\gamma(t)$ with $\nabla_{\dot\gamma} \dot\gamma = 0$. The $\nabla^{(0)}$-geodesics minimize Fisher–Rao arc length. The **e-geodesics** ($\nabla^{(e)}$) are straight lines in the natural parameters; the **m-geodesics** ($\nabla^{(m)}$) are straight lines in the expectation parameters, i.e. $t \mapsto (1-t)\,p_0 + t\,p_1$ in distribution space. These coincide only when $\alpha = 0$, i.e. for the metric connection.

On dually flat manifolds the **generalized Pythagorean theorem** holds: if the m-geodesic from $p$ to $q$ is orthogonal (in the Fisher metric) to the e-geodesic from $q$ to $r$, then

$$
D(p \,\|\, r) = D(p \,\|\, q) + D(q \,\|\, r),
$$

with $D$ the canonical divergence. This underlies the **projection theorem**: the divergence-minimizing point of a distribution onto a flat submanifold is unique and is obtained by orthogonal geodesic projection.

## The natural gradient

Let $L(\theta)$ be a smooth objective on a statistical manifold with metric $g$. The ordinary gradient $\nabla L = (\partial_i L)$ depends on the coordinates and is not the direction of steepest ascent with respect to $g$. The **natural gradient** is

$$
\tilde\nabla L(\theta) = g(\theta)^{-1}\, \nabla L(\theta),
$$

the Riemannian gradient: the steepest-ascent direction under the Fisher metric, with the steepest-descent update $\theta_{t+1} = \theta_t - \eta\, g(\theta_t)^{-1} \nabla L(\theta_t)$. Because $g$ transforms as a $(0,2)$-tensor and $\nabla L$ as a $(0,1)$-tensor, the product $g^{-1}\nabla L$ is a vector and the update is invariant to smooth reparametrization. Amari (1998) introduced natural gradient descent on this basis; its cost is the formation and inversion of $g(\theta)$, which is $O(n^3)$ per step in general and the practical obstacle that motivates approximations (block-diagonal, Kronecker-factored, and empirical-Fisher schemes).

## Sources

- S. Amari and H. Nagaoka, *Methods of Information Geometry*, AMS/OUP, 2000.
- S. Amari, "Natural Gradient Works Efficiently in Learning," *Neural Computation* 10(2), 1998.
- F. Nielsen, "An Elementary Introduction to Information Geometry," *Entropy* 22(10), 2020. arXiv:1808.08271.
