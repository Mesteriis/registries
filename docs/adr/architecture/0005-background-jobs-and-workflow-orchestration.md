# ADR-0005: Run heavy processing as background jobs and orchestrated workflows

- Status: Accepted
- Date: 2026-03-25
- Deciders: avm
- Supersedes:
- Superseded by:

## Related ADRs

- [ADR-0003](./0003-event-driven-internal-integration.md)
- [ADR-0009](./0009-deployment-topology-and-runtime-model.md)
- [ADR-0010](./0010-use-taskiq-redis-streams-and-postgresql.md)
- [ADR-1004](../product/1004-storage-strategy-for-artifacts-metadata-and-decisions.md)

## Context

Some platform operations are heavy, slow, or depend on external systems.
Running everything inline inside a request makes the API slower and recovery
harder.

## Decision

Heavy and potentially long-running stages run as background jobs or workflow
steps.

Baseline execution stack:

- `Taskiq` as the runtime for deferred tasks;
- `Redis Streams` as the broker and transport between producers and workers.

Only the minimum remains synchronous:

- accept the request;
- store the input or a reference to it;
- register process start;
- return a tracking reference or current status.

Orchestration must support retry, idempotency, timeout, and dead-letter
semantics. Domain state and durable execution results remain in the primary
storage and are not delegated to the broker.

## Consequences

### Positive

- API latency stays predictable;
- failed steps are easier to retry and isolate;
- heavy handlers can scale independently.

### Negative

- an explicit state-machine pipeline is required;
- eventual consistency and operational complexity appear.

### Neutral

- small synchronous checks remain acceptable if they do not violate the latency budget.

## Alternatives considered

- a fully synchronous pipeline;
- batch-only processing;
- one large worker with no explicit workflow model.

## Follow-up work

- [ ] define queues, priorities, and job classes on top of `Taskiq`
- [ ] document retry, backoff, and dead-letter policy
- [ ] define the idempotency strategy
