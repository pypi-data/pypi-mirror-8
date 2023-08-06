
import os
import sys
import radical.pilot as rp

# READ: The RADICAL-Pilot documentation: 
#   http://radicalpilot.readthedocs.org/en/latest
#
# Try running this example with RADICAL_PILOT_VERBOSE=debug set if 
# you want to see what happens behind the scenes!


#------------------------------------------------------------------------------
#
def pilot_state_cb (pilot, state) :
    """ this callback is invoked on all pilot state changes """

    print "[Callback]: ComputePilot '%s' state: %s." % (pilot.uid, state)

    if  state == rp.FAILED:
        sys.exit (1)


#------------------------------------------------------------------------------
#
def unit_state_cb (unit, state) :
    """ this callback is invoked on all unit state changes """

    print "[Callback]: ComputeUnit  '%s' state: %s." % (unit.uid, state)

    if state in [rp.FAILED] :
        print "stdout: %s" % unit.stdout
        print "stderr: %s" % unit.stderr


#------------------------------------------------------------------------------
#
if __name__ == "__main__":

    try :

        # prepare some input files for the compute units
        os.system ('hostname > file1.dat')
        os.system ('date     > file2.dat')
    
        # Create a new session. A session is the 'root' object for all other
        # RADICAL-Pilot objects. It encapsulates the MongoDB connection(s) as
        # well as security credentials.
        session = rp.Session()
    
        # Add an ssh identity to the session.
        c = rp.Context('ssh')
        #c.user_id = "alice"
        #c.user_pass = "ILoveBob!"
        session.add_context(c)
    
        # Add a Pilot Manager. Pilot managers manage one or more ComputePilots.
        pmgr = rp.PilotManager(session=session)
    
        # Register our callback with the PilotManager. This callback will get
        # called every time any of the pilots managed by the PilotManager
        # change their state.
        pmgr.register_callback(pilot_state_cb)
        pdescs = list()
    
        for i in range (1) :
            # Define a 32-core on stampede that runs for 15 minutes and
            # uses $HOME/radical.pilot.sandbox as sandbox directory.
            pdesc = rp.ComputePilotDescription()
            pdesc.resource  = "xsede.stampede"
            pdesc.runtime   = 120
            pdesc.cores     = 1024
            pdesc.cleanup   = True
            pdesc.queue     = "normal"
            pdesc.project   = "TG-MCB090174"
    
            pdescs.append (pdesc)
    
        # Launch the pilot.
        pilots = pmgr.submit_pilots(pdescs)
    
        # Combine the ComputePilot, the ComputeUnits and a scheduler via
        # a UnitManager object.
        umgr = rp.UnitManager(
            session=session,
            scheduler=rp.SCHED_BACKFILLING)
    
        # Register our callback with the UnitManager. This callback will get
        # called every time any of the units managed by the UnitManager
        # change their state.
        umgr.register_callback(unit_state_cb)
    
        # Add the previsouly created ComputePilot to the UnitManager.
        umgr.add_pilots(pilots)
    
        # Create a workload of 8 ComputeUnits (tasks). Each compute unit
        # uses /bin/cat to concatenate two input files, file1.dat and
        # file2.dat. The output is written to STDOUT. cu.environment is
        # used to demonstrate how to set environment variables within a
        # ComputeUnit - it's not strictly necessary for this example. As
        # a shell script, the ComputeUnits would look something like this:
        #
        #    export INPUT1=file1.dat
        #    export INPUT2=file2.dat
        #    /bin/cat $INPUT1 $INPUT2
        #
        cuds = list()
    
        for unit_count in range(0, 10240):
            cud = rp.ComputeUnitDescription()
            cud.executable    = "/bin/sleep 600"
            cud.cores         = 1
            cuds.append(cud)
    
        # Submit the previously created ComputeUnit descriptions to the
        # PilotManager. This will trigger the selected scheduler to start
        # assigning ComputeUnits to the ComputePilots.
        units = umgr.submit_units(cuds)
    
        # Wait for all compute units to reach a terminal state (DONE or FAILED).
        umgr.wait_units()
    
        for unit in units:
            print "* Unit %s (executed @ %s) state: %s, exit code: %s, started: %s, finished: %s, output: %s" \
                % (unit.uid, unit.execution_locations, unit.state, unit.exit_code, unit.start_time, unit.stop_time,
                   unit.stdout)

    except Exception as e:

        print "error caught: %s" % e


    finally : 
    
        # Close automatically cancels the pilot(s).
        print "==========================================="
        print session.uid
        print "==========================================="
        session.close(delete=False)
    
        # delete the test data files
        os.system ('rm file1.dat')
        os.system ('rm file2.dat')

# ------------------------------------------------------------------------------

