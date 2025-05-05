Thought for a second


# UThreads — User-Level Threads Library in C++

A lightweight cooperative/preemptive user-level threads (“uthreads”) library using `SIGVTALRM`, `setjmp/longjmp`, and round-robin scheduling.

---

## 📋 Overview

`uthreads` provides:

* **Thread creation** & lifecycle management (spawn, block, resume, sleep, terminate)
* **Preemptive scheduling** via virtual timer (`SIGVTALRM`) and quantums
* **Per-thread context switching** with `sigsetjmp`/`siglongjmp`
* **Memento-style snapshots** of stacks for clean teardown

---

## 🚀 Quick Start

```cpp
#include "uthreads.h"

int main() {
    if (uthread_init(100000 /* 100 ms quantum */) < 0) return 1;

    int tid1 = uthread_spawn(threadFuncA);
    int tid2 = uthread_spawn(threadFuncB);

    // … run until exit …
    return 0;
}
```

Compile and link with:

```bash
g++ -std=c++11 -Wall -pthread your_app.cpp uthreads.cpp -o your_app
```

---

## 🔑 Core API

| Function                              | Description                                                      | Return               |
| ------------------------------------- | ---------------------------------------------------------------- | -------------------- |
| `int uthread_init(int quantum_usecs)` | Initialize library, main thread, timer handler & signal mask.    | `0` on success, `-1` |
| `int uthread_spawn(fp)`               | Create new thread running `fp()`, assign TID, schedule it.       | new TID, or `-1`     |
| `int uthread_terminate(int tid)`      | Terminate thread `tid`. If `tid==0`, shuts down library & exits. | `0` or `-1`          |
| `int uthread_block(int tid)`          | Block runnable thread `tid` (cannot block main).                 | `0` or `-1`          |
| `int uthread_resume(int tid)`         | Unblock thread `tid`, enqueue if not sleeping.                   | `0` or `-1`          |
| `int uthread_sleep(int quantums)`     | Sleep current thread for `quantums` ticks. Main cannot sleep.    | `0` or `-1`          |
| `int uthread_get_tid()`               | Return calling thread’s TID.                                     | TID                  |
| `int uthread_get_total_quantums()`    | Total quantums since init (all threads).                         | quantum count        |
| `int uthread_get_quantums(int tid)`   | Quantums consumed by thread `tid`.                               | count or `-1`        |

---

## ⚙️ Design Highlights

1. **Thread Control Block (TCB)**

   * Holds `tid`, stack pointer, `sigjmp_buf env`, state, entry point & quantum count
   * Uses architecture-specific `translate_address()` hack for `env->__jmpbuf`

2. **Preemptive Scheduler**

   * Virtual timer (`ITIMER_VIRTUAL`) fires every quantum
   * `timer_handler()` blocks signals, updates sleepers, increments counters, then `context_switch()`

3. **Round-Robin**

   * Ready queue: `std::deque<int> ready_threads`
   * On switch: save current via `sigsetjmp`, enqueue if runnable, then `siglongjmp` to next

4. **Sleeping / Blocking**

   * `sleeping_threads` map of `(tid → remaining_quantums)`
   * Each tick decrements and re-enqueues when zero

5. **Signal Safety**

   * `SignalBlocker` RAII class blocks/unblocks `SIGVTALRM` in critical sections

6. **Memory Management**

   * Per-thread stack allocated via `malloc(STACK_SIZE)`
   * Deferred frees collected in `stacks_to_free` to avoid freeing active stack

---

## 🎯 Use Cases

* **Operating Systems projects**: demonstrate context-switching, preemption, and scheduling

---

## 🛠️ Requirements

* POSIX-compliant OS (Linux, macOS)
* C++11 or newer
* No external dependencies

---
