#include "uthreads.h"
#include <deque> 
#include <iostream>
#include <string> 
#include <signal.h>
#include <setjmp.h>
#include <map>
#include <sys/time.h>
#include <vector>
#include <algorithm>


#ifdef __x86_64__
/* code for 64 bit Intel arch */

typedef unsigned long address_t;
#define JB_SP 6
#define JB_PC 7

/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%fs:0x30,%0\n"
        "rol    $0x11,%0\n"
                 : "=g" (ret)
                 : "0" (addr));
    return ret;
}

#else
/* code for 32 bit Intel arch */

typedef unsigned int address_t;
#define JB_SP 4
#define JB_PC 5


/* A translation is required when using an address of a variable.
   Use this as a black box in your code. */
address_t translate_address(address_t addr)
{
    address_t ret;
    asm volatile("xor    %%gs:0x18,%0\n"
                 "rol    $0x9,%0\n"
    : "=g" (ret)
    : "0" (addr));
    return ret;
}


#endif

using std::string;
using std::cerr;
using std::endl;
typedef unsigned long address_t;


// thread states
enum ThreadState {
    READY,
    RUNNING,
    BLOCKED,
    TERMINATED
};
void unblock_virtual_alarm();
void block_virtual_alarm();
static void thread_trampoline();


// Thread Context Block Class
struct TCB {
    int tid;
    void* stack_pointer; 
    ThreadState state;
    sigjmp_buf env;
    thread_entry_point thread_function;
    int running_quantums=1; // Number of quantums the thread has been in the running state
    // Constructer with parameters:
    TCB(int id,void* stack,thread_entry_point entry_point): tid(id),stack_pointer(stack), state(READY),
     thread_function(entry_point),running_quantums(1){
        (env->__jmpbuf)[JB_SP] = translate_address((address_t) stack + STACK_SIZE - sizeof(address_t));
        (env->__jmpbuf)[JB_PC] = translate_address((address_t)thread_trampoline);
     }

    // Default constructor
    TCB() : tid(-1),stack_pointer(nullptr), state(READY) ,thread_function(nullptr),running_quantums(1){}
};
   

void jump_to_new();
int set_timer();

// global variables
struct itimerval timer;
struct sigaction sa = {0};
sigset_t block_sigvtalrm;
std::deque<int> ready_threads; // queue of tids in ready state
std::map<int, int> sleeping_threads;//shhhh quite theyre tired (thread_id, nap_time)
std::map<int,TCB> threads; // map of (tid,TCB of that thread)
int running_thread_tid = -1;
int total_quantums = 1;
int g_quantum_usecs;
static std::vector<void*> stacks_to_free;

static void thread_trampoline() {
    // still running with SIGVTALRM blocked here…
    unblock_virtual_alarm();            // now allow the timer to fire
    threads[running_thread_tid].thread_function();     // call the real entry point
}

/** 
 * This function prints a given system error and exits with code 1.
 */
void system_error(string msg){
    cerr << "system error: " << msg << endl;
    exit(1);
}

/** 
 * This function prints a given library error:
 */ 
void library_error(string msg){
    cerr << "thread library error: " << msg << endl;
}


void initialize_signal_mask() {
    if (sigemptyset(&block_sigvtalrm) != 0 || sigaddset(&block_sigvtalrm, SIGVTALRM) != 0) {
        system_error("Failed to initialize signal mask for SIGVTALRM.");
    }
}

/**
 * This function blocks the virtual time alarm signal:
*/
void block_virtual_alarm(){
    initialize_signal_mask();
    if(sigprocmask(SIG_BLOCK, &block_sigvtalrm, nullptr)!=0){
        system_error("sigprocmask failed when tried to block virtual alarm.");
    }
} 

/**
 * This function unblocks the virtual time alarm signal:
*/
void unblock_virtual_alarm(){
    initialize_signal_mask();
    if(sigprocmask(SIG_UNBLOCK, &block_sigvtalrm, nullptr)!=0){
        system_error("sigprocmask failed when tried to block virtual alarm.");
    }
}

/**
 *  A class that can be called at the begining of an atomic function. alarm will be blocked for the duration of the function
 *  unless excplicitly unblocked (say for a context switch trigger using kill).
 */
class SignalBlocker {
public:
    SignalBlocker() { block_virtual_alarm(); }
    ~SignalBlocker() { unblock_virtual_alarm();}
};

/** 
 * This function finds the next avaible tid:
*/
int allocate_tid(){
    if(threads.size()>=MAX_THREAD_NUM){
        library_error("Reached maximum number of threads.");
        return -1;
    }
    for(int i=0;i<MAX_THREAD_NUM;i++){
        if(threads.count(i) == 0){
            return i;
        }
    }
    return -1;

}

/**
 * This function iterates over all sleeping threads, subtracts 1 quantum from their nap time and if 0, wakes them up.
 */
void update_sleeper_threads() {
    for (auto it = sleeping_threads.begin(); it != sleeping_threads.end(); ) {
        it->second -= 1;
        if (it->second <= 0) {
            // Add the sleeping thread to ready threads if not in a blocked state
            if (threads[it->first].state != BLOCKED) {
                ready_threads.push_back(it->first);
            }
            // Erase the current element and update the iterator
            it = sleeping_threads.erase(it);
        } else {
            ++it;
        }
    }
}


/**
 * update thread adds old thread to ready threads if not sleeping or blocked, and wakes up threads that finish sleeping
*/ 
void update_ready_threads(int old_thread){
    if (threads[old_thread].state != BLOCKED && !sleeping_threads.count(old_thread)){
        ready_threads.push_back(old_thread);
        threads[old_thread].state=READY;
    }
}

/**
 * preforms a context switch from one thread to the next thread in ready_threads, implementing a round robin scheduling process. 
 * also handles a context switch from a terminated thread and a general termination of thread 0.
 */
void context_switch(){
    // perform a context switch only if the is at least one thread in ready state
    if(ready_threads.size()>0){

        // if(threads.count(running_thread_tid)) {
        if(threads[running_thread_tid].state!=TERMINATED) {
            int ret_val = sigsetjmp(threads[running_thread_tid].env, 0);

            // if just saved state than jump to next
            if (ret_val == 0) {
                int old_thread = running_thread_tid;
                // add to ready if not blocked or sleeping
                update_ready_threads(old_thread);
                jump_to_new();
            }else if (ret_val==42)
            {
                running_thread_tid = 0;
                uthread_terminate(0);
            }
            
        }else{ 
            //old thread is terminated and just go to next thread
            //defer terminated stack to be freed by a different thread
            stacks_to_free.push_back(threads[running_thread_tid].stack_pointer);
            threads.erase(running_thread_tid);
            jump_to_new();
        }

    }
}

/**
 * jumps to next thread in ready_threads
 */
void jump_to_new() {
    running_thread_tid = ready_threads.front();
    ready_threads.pop_front();
    threads[running_thread_tid].state = RUNNING;
    siglongjmp(threads[running_thread_tid].env, 1);
}

/**
 *  A custom timer handler that:
 *  1) frees all deferred stacks
 *  2) updates sleeper threads
 *  3) increments general_quantum count and running quantum count of the current thread (if thread isnt terminated).
 *  4) calls for context switch
 */
void timer_handler(int sig){//recieves sig for api reasons
    SignalBlocker sb;
    // update sleeper threads and perform a context switch
    update_sleeper_threads();
    total_quantums++;
    context_switch();
    for (void* p : stacks_to_free) {
        free(p);
    }
    stacks_to_free.clear();
    // incerement 1 when returning from context switch
    threads[running_thread_tid].running_quantums++;
    set_timer();

}

int uthread_init(int quantum_usecs){

    if(quantum_usecs <= 0){
        library_error("Quantum must be a positive integer.");
        return -1;
    }

    // Initialize the main thread:
    TCB main_thread;
    main_thread.tid = 0;
    main_thread.state = RUNNING;
    running_thread_tid = 0;
    threads[0] = main_thread;

    g_quantum_usecs = quantum_usecs;

    SignalBlocker sb;
    sa.sa_handler = &timer_handler;
    if (sigaction(SIGVTALRM, &sa, NULL) < 0)
    {
        system_error("sigaction error.");
        return -1;
    }
    if(set_timer()){
        system_error("failed to set timer");
    }

    return 0;
}

int set_timer() {

    timer.it_interval.tv_sec = g_quantum_usecs / 1000000;
    timer.it_interval.tv_usec = g_quantum_usecs % 1000000;
    timer.it_value.tv_sec = g_quantum_usecs / 1000000;
    timer.it_value.tv_usec = g_quantum_usecs % 1000000;
    if (setitimer(ITIMER_VIRTUAL, &timer, NULL))
    {
        system_error("setitimer error.");
        return -1;
    }
    return 0;
}


/**
 * A function that initializes a new thread:
*/ 
int new_thread(int new_tid,thread_entry_point entry_point){
    auto stack = malloc(STACK_SIZE);
    if(stack == nullptr){
        system_error("Malloc failed.");
        return -1;
    }

    TCB thread(new_tid,stack,entry_point);
    threads[new_tid]=thread;
    ready_threads.push_back(new_tid);

    return 0;
}



int uthread_spawn(thread_entry_point entry_point){
    SignalBlocker sb;

    // If entry point is nullptr return a library error
    if(entry_point == nullptr){
        library_error("entry_point can not be nullptr.");
        return -1;
    }

    // allocate next tid:
    int new_tid = allocate_tid();
    if(new_tid == -1){
        return -1;
    }

    // init new thread
    if(new_thread(new_tid,entry_point)==-1){
        return -1;
    }
    return new_tid;    
}

/**
 * This function frees all stacks not yet freed aside from stack 0.
*/ 
void release_all_threads(){
    // Free all stacks except the main thread (tid 0), exit takes care of that
    for (auto it = threads.begin(); it != threads.end(); ++it) {
        int tid = it->first;
        if (tid == 0) 
            continue;
        free(it->second.stack_pointer);
    }
    threads.clear();

    // Also clear any deferred frees (if you implemented stacks_to_free)
    for (void* p : stacks_to_free) {
        free(p);
    }
    stacks_to_free.clear();
}

int uthread_terminate(int tid){
    SignalBlocker sb;
    

    if(tid==0){ //terminate(0)
        // if were in thread 0 then we release all other threads amd exit the process with code 0
        if (running_thread_tid ==0)
        {
            release_all_threads();
            exit(0);
        }
        else{
            //jump to thread 0 with terminate return value. we will call terminate again from there and return here with running_thread_id==0
            siglongjmp(threads[0].env, 42); 
        }
        

    }
    
    // Check validity of input
    if(tid<0){
        library_error("The provided tid is invalid. Tid should be a non-negative integer.");
        return -1;
    }
    if(threads.count(tid)==0){
        library_error("The thread is not in the threads map.");
        return -1;
    }

    ThreadState thread_state = threads[tid].state;

    if (thread_state == READY) {

        auto it = std::find(ready_threads.begin(), ready_threads.end(), tid);
        if (it == ready_threads.end()) {
            library_error("The given tid of a ready thread is not in the ready_threads deque.");
            return -1;
        }
        ready_threads.erase(it);

    }if(sleeping_threads.count(tid)==1){
        sleeping_threads.erase(tid);
    }

    if(thread_state==RUNNING){
        threads[running_thread_tid].state = TERMINATED;
        unblock_virtual_alarm();
        kill(getpid(),SIGVTALRM);
    }
    
    //finally terminate the thread if not problematic
    free(threads[tid].stack_pointer);
    threads.erase(tid);


    return 0;
}

int uthread_block(int tid){
    SignalBlocker sb;

    if (tid < 0 || tid >= MAX_THREAD_NUM || threads.count(tid)==0) {
        library_error("BLOCK ERROR: Invalid thread ID or thread already terminated");
        return -1;
    }

    else if(tid==running_thread_tid){
        threads[running_thread_tid].state = BLOCKED;
        unblock_virtual_alarm();
        kill(getpid(),SIGVTALRM);
    }
    else if(tid==0){
        library_error("cannot block the main thread");
        return -1;
    }else{
        threads[tid].state = BLOCKED;
        //remove tid from ready_threads if there
        auto it = std::find(ready_threads.begin(), ready_threads.end(), tid);
        // Check if the tid is found
        if (it != ready_threads.end()) {
            ready_threads.erase(it); // Remove the element
        }
    }
    return 0;
}

int uthread_resume(int tid){
    SignalBlocker sb;

    if (tid < 0 || tid >= MAX_THREAD_NUM || threads.count(tid)==0) {
        library_error("RESUME ERROR: Invalid thread ID or thread already terminated");
        return -1;
    }
    // If the thread is in running or ready state do nothing.
    if(threads[tid].state == RUNNING or threads[tid].state == READY){
        return 0;
    }
    threads[tid].state=READY;
    // If thread is also sleeping we don't add the thread to ready list and wait for the sleep time to expire:
    if(sleeping_threads.count(tid)==0){
        ready_threads.push_back(tid);
    }
    return 0;
}

int uthread_sleep(int num_quantums){
    SignalBlocker sb;

    if(running_thread_tid == 0){
        library_error("Can't call sleep function on the main thread.");
        return -1;
    }
    sleeping_threads[running_thread_tid]=num_quantums+1;
    unblock_virtual_alarm();
    kill(getpid(),SIGVTALRM);
    return 0;
}

int uthread_get_tid(){
    SignalBlocker sb;
    return running_thread_tid;
}

int uthread_get_total_quantums(){
    SignalBlocker sb;
    return total_quantums;
}

int uthread_get_quantums(int tid){
    SignalBlocker sb;
    if (tid < 0 || tid >= MAX_THREAD_NUM || threads.count(tid)==0) {
        library_error("GET QUANTUMS ERROR: Invalid thread ID or thread already terminated");
        return -1;
    }
    int ret_val= threads[tid].running_quantums;
    return ret_val;
}