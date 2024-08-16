# Results

I ran an approximation of a best-case, where all tests can be run in the same
process and the tests themselves are relatively lightweight. The same code with
minor variations is added as 1000 integration tests and as 1000 doctests. The
code in question is:

```rust
/// This is a demo function, that contains a doc example.
///
/// # Example
///
/// ```
/// let mut vec_example_fn_0 = vec![1, 2, 85590];
/// vec_example_fn_0.push(3);
/// assert_eq!(vec_example_fn_0, [1, 2, 85590, 3]);
/// ```
pub fn example_fn_0() {}

#[test]
fn example_fn_0() {
    let mut vec_example_fn_0 = vec![1, 2, 16996];
    vec_example_fn_0.push(3);
    assert_eq!(vec_example_fn_0, [1, 2, 16996, 3]);
}
```

## Results Linux

### Setup

```
Linux 6.10
rustc 1.82.0-nightly (2c93fabd9 2024-08-15)
AMD Ryzen 9 5900X 12-Core Processor (Zen 3 micro-architecture)
CPU boost enabled.
```

### edition = "2021"

```
$ hyperfine --min-runs 3 --prepare 'cargo clean' 'cargo t'
  Time (mean ± σ):     10.545 s ±  0.022 s    [User: 104.292 s, System: 95.885 s]
  Range (min … max):   10.522 s … 10.565 s    3 runs
```

Breakdown: Clean compile ~1.4s, integration tests ~0.02s, doctests ~16.8s \[1\]

### edition = "2024"

```
$ hyperfine --min-runs 3 --prepare 'cargo clean' 'cargo t'
  Time (mean ± σ):      2.846 s ±  0.015 s    [User: 3.548 s, System: 0.743 s]
  Range (min … max):    2.829 s …  2.859 s    3 runs
```

Breakdown: Clean compile ~1.4s, integration tests ~0.02s, doctests ~0.1s \[1\]

## edition = "2024" and doctest = false

```
$ hyperfine --min-runs 3 --prepare 'cargo clean' 'cargo t'
  Time (mean ± σ):      1.470 s ±  0.001 s    [User: 1.552 s, System: 0.219 s]
  Range (min … max):    1.469 s …  1.471 s    3 runs
```

Breakdown: Clean compile ~1.4s, integration tests ~0.02s \[1\]

\[1\] Numbers as reported by cargo, in reality felt latency can be quite
different, and very small numbers are inaccurate. E.g. the integration test
binary alone takes ~60ms when measured with `perf stat` which accounts for
process startup, which is 3x what cargo reported. Doctests claim to to run in
100ms but that does not account for some other step, maybe compiling them,
beforehand. Without any code changes `perf stat -d cargo t --test it` is ~90ms.
In contrast running `perf stat -d cargo t --doc` the wall time rises to ~2750ms,
for the exact same test coverage. I'm not sure how to further drill into how
much of that is process startup and how much is compiling the doctests.

## Key takeaways:

- #126245 is a huge improvement!
- The numbers reported by cargo and wall-time waited by users can show large
  discrepancies.
- Given a sufficient quantity of doctests, iterative `cargo t` will become slow,
  no matter how little content is tested.

## Repro

All code can be found here: https://github.com/Voultapher/doctest-parallel-experiment