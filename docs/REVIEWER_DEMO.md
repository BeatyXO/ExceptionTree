# Reviewer demo

A compact reviewer lifecycle should prove that ExceptionTree is not a generic `AI decides policy` wrapper.

## Example sealed policy

1. Root: purchase within 30 days => `ALLOW`
2. Exception: item is perishable => `DENY`
3. Nested exception: perishable item materially defective => `ALLOW`
4. Nested exception: defect reported more than 48h after discovery => `DENY`

## Cases to demonstrate

- within 30 days + non-perishable => root `ALLOW`;
- within 30 days + perishable => exception `DENY`;
- perishable + defective + timely => nested `ALLOW`;
- perishable + defective + late report => deeper `DENY`;
- unclear whether perishable => `AMBIGUOUS` because the uncertain exception could overturn the root;
- equal-ranked contradictory roots => `CONFLICT`;
- wrong definition hash => case submission rejected;
- resolved case second resolution attempt => rejected.

## Consumer proof

Deploy `ExceptionGate` with the finalized ExceptionTree address. Execute one action against a pinned `ALLOW` case, then show:

- exact pinned execution succeeds;
- wrong definition hash fails;
- wrong case hash fails;
- non-ALLOW case fails;
- same action hash replay fails.
