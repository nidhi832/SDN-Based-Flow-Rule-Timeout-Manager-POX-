"""
Flow Rule Timeout Manager using POX Controller
Project No. 22

This controller installs flow rules with:
- Idle Timeout: 10 seconds
- Hard Timeout: 30 seconds

It demonstrates automatic removal of inactive flows
in a Software Defined Network (SDN).
"""

from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()


class TimeoutManager(object):
    """
    Handles PacketIn events and installs flow rules with timeouts.
    """

    def __init__(self, connection):
        self.connection = connection
        connection.addListeners(self)
        log.info("TimeoutManager initialized for switch %s", connection)

    def _handle_PacketIn(self, event):
        """
        Called when the switch sends a packet to the controller.
        Installs a flow rule with idle and hard timeouts.
        """
        packet = event.parsed

        if not packet.parsed:
            log.warning("Ignoring incomplete packet")
            return

        in_port = event.port
        log.info("Packet received on port %s", in_port)

        # Create flow rule
        flow_mod = of.ofp_flow_mod()
        flow_mod.match = of.ofp_match.from_packet(packet, in_port)

        # Set timeout values
        flow_mod.idle_timeout = 10   # Flow expires after 10 seconds of inactivity
        flow_mod.hard_timeout = 30   # Flow expires after 30 seconds regardless of activity
        flow_mod.priority = 10

        # Action: Flood packets (simple forwarding)
        flow_mod.actions.append(
            of.ofp_action_output(port=of.OFPP_FLOOD)
        )

        # Send flow rule to switch
        self.connection.send(flow_mod)

        # Send the current packet immediately
        packet_out = of.ofp_packet_out()
        packet_out.data = event.ofp
        packet_out.in_port = in_port
        packet_out.actions.append(
            of.ofp_action_output(port=of.OFPP_FLOOD)
        )
        self.connection.send(packet_out)

        log.info(
            "Flow installed | idle_timeout=%s | hard_timeout=%s",
            flow_mod.idle_timeout,
            flow_mod.hard_timeout
        )


class TimeoutController(object):
    """
    Main controller that listens for switch connections.
    """

    def __init__(self):
        core.openflow.addListeners(self)
        log.info("Flow Rule Timeout Manager Started")

    def _handle_ConnectionUp(self, event):
        """
        Triggered when a switch connects to the controller.
        """
        log.info("Switch connected: %s", event.connection)
        TimeoutManager(event.connection)


def launch():
    """
    Launches the POX module.
    """
    log.info("Launching Flow Rule Timeout Manager...")
    core.registerNew(TimeoutController)