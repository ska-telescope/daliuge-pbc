daliuge-pbc
===========

This package implements a Processing Block Controller
based on the DALiuGE execution framework.


Quick start
-----------

To try out this package in an isolated, automated manner try the following::

 $> docker-compose -f docker-compose.example.yml up

.. note::
 If you want you can use Docker Swarm instead
 to start the services on the background,
 but you will get no output by default into your screen::

  $> docker stack deploy -c docker-compose.example.yml dlg_pbc

This should start a DALiuGE Node Manager (nm),
a Data Island Manager (dim),
a redis server,
a Processing Controller instance,
and an instance of the DALiuGE-based Processing Block Controller (this package).

With these services running on the background
you can now add a new Scheduling Block instance
to this "live" system, like this::

 $> # If you don't have a copy yet:
 $> git clone https://github.com/SKA-ScienceDataProcessor/integration-prototype
 $> cd integration-prototype/sip/execution_control/configuration_db
 $> # If you don't have it installed yet:
 $> pip install -r requirements.txt
 $> # Finally:
 $> ./sip_config_db/scripts/skasip_config_db_add_sbi

This will internally create three Processing Blocks,
which in turn will end up triggering
the DALiuGE-based PBC to schedule a physical graph for execution
in the Node Manager via the Data Island Manager.
