---
provenance: >
  Negative-space populate (2026-06-23). NATIVE-FORM specimen — Document B of a pair.
  This is the form-respecting companion to synthesis/topos-as-above-so-below.md:
  the same subject written in its own register (mathematical exposition), with no
  cross-links, no metaphor, no consciousness, no mysticism. The form IS the fill.
  do not correct toward house style / do not reconcile / do not enrich /
  do not enrich toward house style.
title: "Topos Theory: The Mathematics"
register: mathematical exposition
links: [topos_as_above_so_below]
---

# Topos Theory: The Mathematics

This is an exposition of the basic definitions of elementary and Grothendieck topos
theory. The aim is precision. Where a statement is a definition it is marked as such;
where it is a theorem requiring proof it is marked as such.

## Categories

A **category** $\mathcal{C}$ consists of: a collection of *objects*; for each ordered
pair of objects $(A,B)$ a collection $\mathrm{Hom}(A,B)$ of *morphisms* (arrows)
$f\colon A \to B$; for each object $A$ an *identity* morphism
$\mathrm{id}_A\colon A \to A$; and a *composition* operation assigning to
$f\colon A \to B$ and $g\colon B \to C$ a morphism
$g \circ f\colon A \to C$. Composition is required to be associative,
$h\circ(g\circ f) = (h\circ g)\circ f$, and the identities are required to be
two-sided units, $f\circ \mathrm{id}_A = f = \mathrm{id}_B \circ f$.

A morphism $m\colon A \to B$ is a **monomorphism** (mono) if it is left-cancellable:
$m\circ g = m\circ h$ implies $g = h$. An **isomorphism** is a morphism with a
two-sided inverse.

## Limits: terminal object, products, pullbacks

A **terminal object** $1$ is an object such that for every object $A$ there is exactly
one morphism $A \to 1$. Terminal objects are unique up to unique isomorphism.

A **product** of objects $A$ and $B$ is an object $A\times B$ with projections
$\pi_A\colon A\times B \to A$ and $\pi_B\colon A\times B \to B$ such that for every
object $X$ with morphisms $f\colon X\to A$, $g\colon X\to B$ there is a unique
$\langle f,g\rangle\colon X \to A\times B$ with $\pi_A\circ\langle f,g\rangle = f$ and
$\pi_B\circ\langle f,g\rangle = g$.

A **pullback** of $f\colon A \to C$ and $g\colon B \to C$ is an object $A\times_C B$
with morphisms $p\colon A\times_C B \to A$, $q\colon A\times_C B \to B$ satisfying
$f\circ p = g\circ q$, and universal among such: for every $X$ with $u\colon X\to A$,
$v\colon X\to B$ and $f\circ u = g\circ v$ there is a unique $X \to A\times_C B$
commuting with $p$ and $q$.

A category has **finite limits** if and only if it has a terminal object and pullbacks;
equivalently, a terminal object and all binary products and equalizers. (This
equivalence is a theorem.)

## Exponential objects and cartesian closure

Fix an object $A$. An **exponential object** $B^A$ is an object equipped with an
*evaluation* morphism $\mathrm{ev}\colon B^A \times A \to B$ such that for every object
$X$ and morphism $f\colon X\times A \to B$ there is a unique
$\lambda f\colon X \to B^A$ (the *transpose*, or *currying*) with
$\mathrm{ev}\circ(\lambda f \times \mathrm{id}_A) = f$.

A category with finite products is **cartesian closed** if every pair of objects has an
exponential object; equivalently, if for each $A$ the functor $(-)\times A$ has a right
adjoint $(-)^A$.

## The subobject classifier

A **subobject** of an object $A$ is an equivalence class of monomorphisms into $A$,
where $m\colon S \rightarrowtail A$ and $m'\colon S' \rightarrowtail A$ are identified
when each factors through the other by an isomorphism.

A **subobject classifier** is an object $\Omega$ together with a morphism
$\top\colon 1 \to \Omega$ ("true") such that for every monomorphism
$m\colon S \rightarrowtail A$ there is a *unique* morphism $\chi_m\colon A \to \Omega$
(the *characteristic* morphism) making the square

$$
\begin{array}{ccc}
S & \longrightarrow & 1 \\
\downarrow m & & \downarrow \top \\
A & \xrightarrow{\ \chi_m\ } & \Omega
\end{array}
$$

a pullback. Equivalently, $\Omega$ represents the subobject functor: there is a natural
isomorphism $\mathrm{Sub}(A) \cong \mathrm{Hom}(A,\Omega)$.

## Elementary topos

**Definition.** An **elementary topos** is a category $\mathcal{E}$ that

1. has all finite limits,
2. is cartesian closed,
3. has a subobject classifier $\Omega$.

The standard example is $\mathbf{Set}$, with $1$ a one-element set, $A\times B$ the
cartesian product, $B^A$ the set of functions $A\to B$, and $\Omega = \{0,1\}$ with
$\top$ picking out $1$; here $\chi_m$ is the indicator function of the image of $m$.
For any small category $\mathcal{C}$ the presheaf category
$[\mathcal{C}^{\mathrm{op}}, \mathbf{Set}]$ is a topos.

## The internal Heyting algebra and intuitionistic logic

**Theorem.** In any elementary topos the subobject classifier $\Omega$ carries the
structure of an internal **Heyting algebra**: there are morphisms
$\wedge, \vee, \Rightarrow \colon \Omega\times\Omega \to \Omega$ and elements
$\top, \bot \colon 1 \to \Omega$ making $\Omega$ a Heyting algebra object. Consequently,
for each object $A$ the poset of subobjects $\mathrm{Sub}(A)$ is a Heyting algebra, and
these structures are stable under pullback.

A Heyting algebra is a bounded lattice with a relative pseudo-complement (the operation
$\Rightarrow$ right adjoint to $\wedge$); it need not satisfy the law of excluded middle
$a\vee\neg a = \top$, where $\neg a := (a\Rightarrow\bot)$. The internal logic of a topos
is therefore **intuitionistic** in general. A topos is **Boolean** when $\Omega$ is an
internal Boolean algebra, equivalently when excluded middle holds internally; $\mathbf{Set}$
is Boolean.

## Sites, sheaves, Grothendieck toposes

A **sieve** on an object $C$ of a category $\mathcal{C}$ is a collection $S$ of morphisms
with codomain $C$ that is closed under precomposition: if $(f\colon D \to C)\in S$ and
$g\colon E \to D$ then $f\circ g \in S$.

A **Grothendieck topology** $J$ assigns to each object $C$ a set $J(C)$ of *covering
sieves* on $C$ satisfying:

1. (*maximality*) the maximal sieve of all morphisms into $C$ is in $J(C)$;
2. (*stability*) if $S\in J(C)$ and $h\colon D\to C$, then the pullback sieve
   $h^{*}S = \{\,g \mid h\circ g \in S\,\}$ is in $J(D)$;
3. (*transitivity*) if $S\in J(C)$ and $R$ is a sieve on $C$ such that
   $h^{*}R \in J(D)$ for every $(h\colon D\to C)\in S$, then $R\in J(C)$.

A **site** is a category equipped with a Grothendieck topology. A presheaf
$F\colon \mathcal{C}^{\mathrm{op}}\to\mathbf{Set}$ is a **sheaf** for $J$ if for every
covering sieve every compatible family of sections has a unique amalgamation. The
category $\mathrm{Sh}(\mathcal{C},J)$ of sheaves on a (small) site is a
**Grothendieck topos**.

**Theorem.** Every Grothendieck topos is an elementary topos, and is moreover cocomplete
with a small generating set. Equivalently (Giraud's theorem), a category is a Grothendieck
topos iff it is the category of sheaves on some small site.

## Geometric morphisms

**Definition.** A **geometric morphism** $f\colon \mathcal{F} \to \mathcal{E}$ between
toposes is a pair of adjoint functors
$$f^{*} \dashv f_{*}, \qquad f^{*}\colon \mathcal{E}\to\mathcal{F}, \quad
f_{*}\colon \mathcal{F}\to\mathcal{E},$$
in which the left adjoint $f^{*}$ (the **inverse image**) preserves finite limits, i.e.
is left exact. The right adjoint $f_{*}$ is the **direct image**.

Geometric morphisms are the morphisms of the (2-)category of toposes; they generalize
continuous maps of topological spaces, recovering them via the assignment
$X \mapsto \mathrm{Sh}(X)$.
