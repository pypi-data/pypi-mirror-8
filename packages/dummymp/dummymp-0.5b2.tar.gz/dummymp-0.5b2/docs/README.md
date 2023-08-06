DummyMP Documentation
======================

How to use?
------------
Note: Although the whole API is covered in this guide, it is not a
      substitute for the API documentation. The API documentation can
      be found in all of the source files, and is formatted to be
      accessible with pydoc.

### Step 0: Figure out your functions!
The first thing to do is to figure out what functions you can
parallelize. Functions that can run independently from other functions
are strong candidates for parallelization. Functions that depend on
each other's output (sequential functions) are weak candidates for
parallelization.

Functions that tend to be good candidates for parallelization include
functions that are repeated often, usually in a loop.

Note that it's not necessarily the function itself that defines if it
can be parallelized or not, but the use of the function.

Here are some examples to help explain what works and what doesn't.

This is an example of a function that works great with parallelization:

    def incr(n):
        return n + 1
    for x in range(0, 5):
        print incr(x)

This is an example of a function that will not work well with
parallelization:

    def incr(n):
        return n + 1
    x = 0
    while x < 10:
        x = incr(x)
        print(x)

Notice how the functions are exactly the same, but the usage of those
functions determined whether it could be parallelized or not.

The latter example requires the previous result before the next result
could be computed. Because of that, you must run the code in order, and
therefore you can not split the operation up.

With the former, however, you are simply incrementing each number in
the range. There is no dependency on any result, and therefore it's
possible to split the operation up.

If you have trouble visualizing this, try evaluating the statements.
Let's make the function more complicated so that we can't guess
anything.

    def setn(n):
        n = random.randint(0, n)
        return n

For the first example with the for loop, it will evaluate to:

    print setn(0)
    print setn(1)
    print setn(2)
    print setn(3)
    print setn(4)

For the second one, it's very different. We have no idea what the output
will be, and the input to the function depends on the output after the
intial run. Here's how it will look like:

    x = setn(0)
    print(x)
    x = setn(?)
    print(x)
    x = setn(?)
    print(x)
    ...

(? indicates unknown input.)

Furthermore, since we have a condition set on the output, we don't even
know when this loop will stop!

In the end, the general rule for determining parallelization:

  * If inputs (both variable and state, such as files) are known all of
    the time, it is likely to work with parallelization. (This includes
    pre-determined and static inputs.)
  * If there is any uncertainty for the inputs (variables depends on
    previous state, files need to be created, etc.), it is unlikely to
    work with parallelization.

To conclude, here are some applications that can be parallelized:

  * Some math algorithms (matrix multiplication of a large matrix, for
    instance)
  * Data file processing
  * Computing statistics from multiple data sets
  * Rendering multiple parts of a grid (such as map image rendering)
  * Bulk distributed database queries

### Step 1: Load and Configure DummyMP
First things first - we need to load the DummyMP module! Nothing special
here:

    import dummymp

DummyMP automatically tries to expose all functions and such through the
dummymp module, so there's no need to do anything more complicated than
this.

Next, we need to setup DummyMP, as necessary.

    # Remember - everything here is optional! Configure only things you
    # want to configure - no configuration necessary to run DummyMP!
    
    # Set the maximum number of processes to spawn. By default, this
    # value is 0 - the maximum defaults to the number of CPU cores on
    # the system. Note that the process manager won't spawn this many
    # processes - it still depends on system CPU usage and the
    # "aggression" level (see next code block).
    dummymp.set_max_processes(4)
    
    # Set the priority mode for the process manager. This determines
    # how aggressive the process manager should be when trying to
    # start running functions in the queue. The following modes are
    # available:
    #     dummymp.DUMMYMP_GENEROUS
    #         Very generous - on a crowded server, tries not to step on
    #         anyone's toes! This is for a task that you don't mind
    #         getting done later - much later.
    #           - SPECIAL FEATURE: if this is used, it will not try to
    #             start a process, even if all CPUs are used (and no
    #             processes have been deployed by DummyMP)!
    #           - The process manager checks activity the fastest -
    #             every 5s - because it cares about the other users on
    #             the server. Higher values mean less frequent checking.
    #           - The checking interval (top -d ##) is the slowest -
    #             0.5s - because it has a minimal impact on the server,
    #             and it allows processes to gain higher CPU usage
    #             values, as measured by DummyMP. Faster means lower
    #             measure CPU usage values (more instantaneous), and
    #             more impact on the server.
    #           - The CPU usage threshold is the lowest - 20% - because
    #             it wants to consider even potentially CPU intensive
    #             processes. It considers a process taking at least 20%
    #             CPU usage to be active. If a process does not meet 
    #             this threshold, it is not counted towards the amount
    #             of CPUs used. Higher thresholds means lower chances of
    #             a process counting towards this threshold.
    #           Summary:
    #           - Activity check interval: 5s
    #           - Checking interval: 0.5s
    #           - CPU usage threshold: 20%
    #     dummymp.DUMMYMP_NORMAL
    #         Just act normal - on a crowded server, be respectful, but
    #         you still need to get your work done!
    #           - Activity check interval: 10s
    #           - Checking interval: 0.35s
    #           - CPU usage threshold: 30%
    #     dummymp.DUMMYMP_AGGRESSIVE
    #         Be somewhat aggressive - you have a deadline to meet, but
    #         you don't want to piss off anyone, and slow down your own
    #         work, either!
    #           - Activity check interval: 20s
    #           - Checking interval: 0.2s
    #           - CPU usage threshold: 50%
    #     dummymp.DUMMYMP_EXTREME
    #         Be very aggressive - you have something due soon, and it's
    #         URGENT. You might piss off a few, but it's something you
    #         can apologize later over a coffee break.
    #           - Activity check interval: 30s
    #           - Checking interval: 0.1s
    #           - CPU usage threshold: 80%
    #     dummymp.DUMMYMP_NUCLEAR
    #         You need to get stuff done NOW, otherwise things will go
    #         wrong. Lots of things to get done, so little time. You
    #         may need to lock your office door and unplug your phone -
    #         this WILL piss off everyone on the server! You may need to
    #         buy everyone lunch for the day (maybe two) to make up for
    #         your insane aggression.
    #         
    #         NOTE: this won't necessarily help much if there are other
    #               CPU intensive processes on the server, since both
    #               DummyMP and the other processes will be fighting,
    #               eventually splitting CPU usage and decreasing
    #               efficiency.
    #           - SPECIAL FEATURE: This is truly nuclear. It will use
    #             the number of CPU cores available on the system,
    #             ALWAYS. Regardless of any CPU intensive processes,
    #             it will always spawn that number of processes - the
    #             maximum! Oh, and it doesn't check activity, since the
    #             number of CPUs available will stay constant.
    #           - Activity check interval: what checking?
    #           - Checking interval: 0.1s (not that this matters)
    #           - CPU usage threshold: the sky's the limit!
    dummymp.set_priority_mode(dummymp.DUMMYMP_AGGRESSIVE)

It is also possible to create a custom DummyMP mode:

    ####################################################################
    # ADVANCED USAGE:
    ####################################################################
    # You can also define your own priority mode. Note that this isn't
    # officially supported by the API (yet), but it should work as long
    # as everything required is done. (Basically, everything in this
    # code block!)
    # 
    # First, you need to make your own constant. We use positive and
    # negative numbers to denote the priority (a loose *nix nice style
    # priority, -20 to 20, lowest number indicating higest priority).
    # 
    # The current constants are:
    #   DUMMYMP_GENEROUS    = 15
    #   DUMMYMP_NORMAL      = 0
    #   DUMMYMP_AGGRESSIVE  = -5
    #   DUMMYMP_EXTREME     = -10
    #   DUMMYMP_NUCLEAR     = -20
    # Do NOT use any of these numbers, as they will conflict with
    # already defined modes. Instead, use a number between any two #s
    # (or a number between -20 and 20, inclusive) to denote your
    # priority:
    DUMMYMP_CUSTOM = -3
    
    # Now, add your own rules!
    # First, set the CPU threshold. The maximum CPU usage can be up to
    # infinity. The value is top-style percentage:
    #   (100% * # of cores used)
    dummymp.config.DUMMYMP_THRESHOLD[DUMMYMP_CUSTOM] = 75
    
    # Next, set the top -d ## interval. The value is in seconds - you
    # can test these values with the top command. Longer values
    # generally mean more accumulated CPU usage statistics. It also
    # means that the CPU statistics will take somewhat longer (since it
    # delays by 2 * interval secs).
    dummymp.config.DUMMYMP_MINTERVAL[DUMMYMP_CUSTOM] = 0.3
    
    # Now we need to set the refresh interval. This is how often DummyMP
    # will query system CPU usage.
    dummymp.config.DUMMYMP_MREFRESH[DUMMYMP_CUSTOM] = 12
    
    # Finally, we need to give it a name. The name shows up in the debug
    # logs of DummyMP.
    dummymp.config.DUMMYMP_STRING[DUMMYMP_CUSTOM] = "Custom"
    
    # That's it! Well, one more thing - set this new priority mode!
    dummymp.set_priority_mode(DUMMYMP_CUSTOM)

Alright, back to regular setup:
    
    # Set whether to deepcopy the arguments or not.
    # 
    # (Deepcopy is making a "true" copy of a variable, such that
    # changing the variable within DummyMP won't change the original,
    # since it's a deepcopy of said original.)
    # 
    # By default, this is set to True. You may wish to set this to False
    # if you are deepcopying yourself, or if your inputs do not require
    # deepcopying.
    # 
    # Lists and dictionaries usually require deepcopying, since the
    # function uses a reference of the list/dict, and any operation done
    # to them will reflect back to the original.
    dummymp.set_args_deepcopy(True)
    
    # Set whether to deepcopy the keyword arguments or not.
    # 
    # Same concept as above - default is True.
    dummymp.set_kwargs_deepcopy(True)
    
    # Set the callback function when a process is started.
    # 
    # This function is called with the following arguments:
    #     callback(total_completed, total_running, total_processes)
    #       total_completed: total processes that have finished running
    #       total_running:   current # of processes that are running
    #       total_processes: total processes overall
    #     All arguments are integers.
    # 
    # Callbacks are generally used for updating progress shown to the
    # user, since DummyMP does not show progress on its own.
    # An example function is given below:
    
    def update_start(total_completed, total_running, total_procs):
        # Example of what this might output:
        #     Starting process! (4 running, 4/10 completed)
        logging.info("Starting process! (%i running, %i/%i completed)" \
            % (total_running, total_completed, total_procs))
    
    set_start_callback(update_start)
    
    # Set the callback function when a process has completed.
    # 
    # Same concept as above, except the callback is run once the process
    # terminates.
    # An example function is given below:
    
    def update_end(total_completed, total_running, total_procs):
        # Example of what this might output:
        #     Process done! (3 running, 5/10 completed)
        logging.info("Process done! (%i running, %i/%i completed)" \
            % (total_running, total_completed, total_procs))
            
    set_end_callback(update_end)

That's it for configuration!

### Step 2: Queue Function into DummyMP
Remember our complicated function from earlier?

    def setn(n):
        n = random.randint(0, n)
        return n

Let's assume this is our code:

    y = []
    for x in range(0, 5):
        y.append(incr(x))

It might be tempting to assuming this can't be parallelized, since you
could unwrap it to look like this:

    y.append(?)
    y.append(?)
    y.append(?)
    y.append(?)
    y.append(?)

But wait! Remember that DummyMP supports ordered returns - that is, the
order you add the functions into DummyMP is the order they will come
back. Therefore, unwrapping it can now look like this:

    y.append(incr(0))
    y.append(incr(1))
    y.append(incr(2))
    y.append(incr(3))
    y.append(incr(4))

From here, let's make things work! First, let's rewrite the loop so that
we are queueing the functions instead!

    for x in range(0, 5):
        dummymp.run(incr, x)

Notice how the function call is converted to a queued function. This
works with keyword arguments as well. Here are some examples below.

    # Before:
    myfunc(x, y, z)
    
    # After:
    dummymp.run(myfunc, x, y, z)
    
    # Before:
    myfunc(a=1, b=2, c=3)
    
    # After:
    dummymp.run(myfunc, a=1, b=2, c=3)
    
    # Before:
    myfunc(x, y, z, a=1, b=2, c=3)
    
    # After:
    dummymp.run(myfunc, x, y, z, a=1, b=2, c=3)

Depending on your program, sometimes determing the function's arguments
may be a bit slow. An optional optimization would be to run the DummyMP
processing code within your loop:

    for x in range(0, 5):
        y = sluggish_function(x)
        dummymp.run(incr, y)
        # Start processing the queue while in the loop!
        dummymp.process_process()

(This is also available in the "Optimization" section.)

This will slow down the loop a bit, but will allow processes to start
sooner, rather than waiting for the queuing to finish.

### Step 3: Run DummyMP
This is the easiest step! The simplest thing to do is this:

    # Process everything until done. This blocks and doesn't move
    # forward until that condition is met.
    dummymp.process_until_done()

If you want to handle termination, you can do this:

    try:
        # Process everything until done. This blocks and doesn't move
        # forward until that condition is met.
        dummymp.process_until_done()
    except KeyboardInterrupt:
        # Stop all of the currently running processes.
        dummymp.killall()

For those who like to do things in a controllable loop, there's a way
to do it without blocking! (This is likely the case for GUI
applications, or applications that need to be able to accept user input
all the time.)

Remember this?

    dummymp.process_process()

This function also returns a boolean indicating whether processes are
still running or not. True if there are, False if there are not.

Therefore, you can write something like this:

    while not dummymp.process_process():
        # Keep processing the queue!
        dummymp.process_queue()
        time.sleep(0.001)

This is essentially the code for dummymp.process_until_done().

A more realistic version could look like this:

    while gui.alive():
        dmp_ready = dummymp.process_process()
        
        if not dmp_ready:
            dummymp.process_queue()
        else:
            gui.alert("Everything done!")
        
        gui.handle_input()

### Step 4: Fetch Return Results
After everything is said and done, you might want the results of
running these functions. Slightly more complcated, but still relatively
simple:

    rets = dummymp.get_returns()

The returns are serialized in a dictionary whose keys are the order the
functions were called, starting at 0.

For example, if this were the code:

    def bla(n):
        return n * 2
    
    dummymp.run(bla, 1)
    dummymp.run(bla, 2)
    dummymp.run(bla, 3)
    
    rets = dummymp.get_returns()

...rets would look like this:

    {0: 2, 1: 4, 2: 6}

For the example we had earlier:

    def setn(n):
        n = random.randint(0, n)
        return n
    
    y = []
    for x in range(0, 5):
        y.append(incr(x))

We can finally, with a bit of trickery, get the original desired result
with DummyMP:

    y = []
    for x in range(0, 5):
        dummymp.run(incr, x)
    
    dummymp.process_until_done()
    
    rets = dummymp.get_returns()
    
    for x in range(0, 5):
        y.append(rets[x])

That's it!

### Step 5: Cleanup (if necessary)
If you need to run more things with DummyMP, it may be a good idea to
reset everything, especially if there are returns involved. (Otherwise,
the return indexes will keep incrementing, resulting in a longer than
necessary return dictionary...)

That's easy to do:

    # Reset everything!
    dummymp.reset()

Note that this will purge everything, including configuration.
If you set any options (including advanced custom options), you will
need to set them up again.

Optimization
-------------
To speed things up, it's not a bad idea to get the CPU availability
at the very beginning so that DummyMP doesn't have to:

    # Get the CPU availability immediately
    dummymp.getCPUAvail()
    
    # Get processing! Processing/DummyMP code goes below...

If you have a lot of function calls, it may take a while before you
queue everything. Why not queue functions AND run them at the same time?

    # Loop
    for i in xrange(0, 1000):
        # Queue function with argument!
        dummymp.run(myfunc, i)
        
        # Process queue and handle processes!
        dummymp.process_process()
    
    # Now wait until everything's done!
    dummymp.process_until_done()
