from enum import Enum


class SocketNames(Enum):
    #### Sockets used on server ####
    # As soon as sessions are received from the remote drone the data will get retransmitted unaltered on this socket
    RAW_SESSIONS = 'inproc://rawSessionPublisher'
    # After sessions has been classified they will get retransmitted on this socket.
    # TODO: Does not actually happen yet
    PROCESSED_SESSIONS = 'inproc://processedSessionPublisher'
    # Request / Reply to config actor
    CONFIG_COMMANDS = 'inproc://configCommands'
    # Data sent on this socket will be retransmitted to the correct drone, the data must be prefixed with
    # the id of the drone.
    DRONE_COMMANDS = 'inproc://droneCommands'

    #### Sockets used on drones ####
    # Drone commands received from the server will be retransmitted  on this socket.
    SERVER_COMMANDS = 'inproc://serverCommands'
    # All messages transmitted on this socket will get retransmitted to the server
    SERVER_RELAY = 'inproc://serverRelay'
