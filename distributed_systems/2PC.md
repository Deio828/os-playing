# 2PC - 2-Phase Commit

## 🧩 The Problem 2PC Solves
In distributed systems, you often need to perform a transaction that spans multiple services or databases. The challenge is ensuring all participants either commit or roll back together. Without coordination, you risk data inconsistency.

Imagine:

A money transfer where Service A debits one account and Service B credits another.

What if one succeeds and the other fails?

👉 You need atomicity across systems. That’s the problem 2PC is designed to solve.

## 👀 Example
- Imagine you have a system where there are multiple services `A`, `B`, `C` and `D`. 
- Now you have some request that requires a sequential process as follows:
```
INPUT1 --> A --> B --> C --> OUTPUT1
```
- And then you got another request that requires another sequence like:
```
INPUT2 --> A --> D --> OUTPUT2
```
- The problem here is that if `C` for example failed or not ready to handle a request then we will utilize `A`, `B` which will delay the excution of `OUTPUT2` and `OUTPUT1` will not be produced.

## 🔧 How 2PC Solves It
2PC coordinates a transaction across multiple nodes in two phases:

**Phase 1 – Prepare (Voting):**
- A coordinator sends a `prepare` message to all participants.
- Each participant executes the transaction but does not commit—it only says "I'm ready" (or not).
- They respond with a `vote` (Yes or No).

**Phase 2 – Commit or Rollback:**
- If all vote Yes, the coordinator sends `commit` to everyone.
- If any vote No, it sends `rollback` to all.

This ensures all-or-nothing outcomes:
- Either all `commit`, or all `rollback` — no partial updates.

## 🚫 When to Avoid 2PC
- Performance-sensitive systems: 2PC is slow and blocking—participants may hold locks while waiting for coordination.

- Unreliable networks: 2PC doesn’t handle network partitions well (can leave participants in uncertain state).

- Highly scalable microservices: Better to use Saga or eventual consistency in loosely coupled systems.

## ⚠️ WARNING!
2PC is more common in tightly controlled environments (e.g., databases in enterprise settings) than in modern cloud-native architectures.