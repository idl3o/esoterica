# Zeitgeist runs — the audit trail

One directory per reading, named by date. Each holds what the reading was written *from*, so a claim in a published reading can be traced to the digest that carried it and to the check that was run on it.

| file | station | what it is |
|---|---|---|
| `1-gather-a…d.md` | Step 1 | the four gather agents' neutral digests, as returned |
| `3a-verifier.md` | Step 3a | every quotation and load-bearing figure, checked against the page |
| `channel-probe.md` | occasional | reachability test of candidate channels, when one was run |

Rules of the directory:

- **Byte-exact, never edited.** These are records, not documents. A digest that was wrong stays wrong here; the correction lives in the verifier's report and in the reading.
- **Model output, at one remove from the page.** Agents search and fetch through tools that summarise; nothing here is a primary source. The verifier's report says what was confirmed, what was close, and what could not be reached.
- **Headline-level register.** The gather contract forbids operational or technical detail on security, conflict and crime stories. If a file here ever contains any, that is a fault in the run, to be removed and noted.
- **Not part of the library.** This is process memory. The reading in `corpus/synthesis/zeitgeist/` is the published thing.

The first entry, `2026-09-19/`, was recovered from the session transcript after the fact. That run is also where the verifier station was first tried: it corrected about twenty of the twenty-five items it was given.
