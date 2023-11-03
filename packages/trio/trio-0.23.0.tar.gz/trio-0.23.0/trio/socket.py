# This is a public namespace, so we don't want to expose any non-underscored
# attributes that aren't actually part of our public API. But it's very
# annoying to carefully always use underscored names for module-level
# temporaries, imports, etc. when implementing the module. So we put the
# implementation in an underscored module, and then re-export the public parts
# here.
# We still have some underscore names though but only a few.


# Uses `from x import y as y` for compatibility with `pyright --verifytypes` (#2625)

# Dynamically re-export whatever constants this particular Python happens to
# have:
import socket as _stdlib_socket
import sys
import typing as _t

from . import _socket

_bad_symbols: _t.Set[str] = set()
if sys.platform == "win32":
    # See https://github.com/python-trio/trio/issues/39
    # Do not import for windows platform
    # (you can still get it from stdlib socket, of course, if you want it)
    _bad_symbols.add("SO_REUSEADDR")

globals().update(
    {
        _name: getattr(_stdlib_socket, _name)
        for _name in _stdlib_socket.__all__  # type: ignore
        if _name.isupper() and _name not in _bad_symbols
    }
)

# import the overwrites
from contextlib import suppress as _suppress

from ._socket import (
    SocketType as SocketType,
    from_stdlib_socket as from_stdlib_socket,
    fromfd as fromfd,
    getaddrinfo as getaddrinfo,
    getnameinfo as getnameinfo,
    getprotobyname as getprotobyname,
    set_custom_hostname_resolver as set_custom_hostname_resolver,
    set_custom_socket_factory as set_custom_socket_factory,
    socket as socket,
    socketpair as socketpair,
)

# not always available so expose only if
if sys.platform == "win32" or not _t.TYPE_CHECKING:
    with _suppress(ImportError):
        from ._socket import fromshare as fromshare

# expose these functions to trio.socket
from socket import (
    gaierror as gaierror,
    gethostname as gethostname,
    herror as herror,
    htonl as htonl,
    htons as htons,
    inet_aton as inet_aton,
    inet_ntoa as inet_ntoa,
    inet_ntop as inet_ntop,
    inet_pton as inet_pton,
    ntohs as ntohs,
)

# not always available so expose only if
if sys.platform != "win32" or not _t.TYPE_CHECKING:
    with _suppress(ImportError):
        from socket import (
            if_indextoname as if_indextoname,
            if_nameindex as if_nameindex,
            if_nametoindex as if_nametoindex,
            sethostname as sethostname,
        )

if _t.TYPE_CHECKING:
    IP_BIND_ADDRESS_NO_PORT: int
else:
    try:
        IP_BIND_ADDRESS_NO_PORT  # noqa: B018  # "useless expression"
    except NameError:
        if sys.platform == "linux":
            IP_BIND_ADDRESS_NO_PORT = 24

del sys


# The socket module exports a bunch of platform-specific constants. We want to
# re-export them. Since the exact set of constants varies depending on Python
# version, platform, the libc installed on the system where Python was built,
# etc., we figure out which constants to re-export dynamically at runtime (see
# below). But that confuses static analysis tools like jedi and mypy. So this
# import statement statically lists every constant that *could* be
# exported. There's a test in test_exports.py to make sure that the list is
# kept up to date.
if _t.TYPE_CHECKING:
    from socket import (  # type: ignore[attr-defined]
        AF_ALG as AF_ALG,
        AF_APPLETALK as AF_APPLETALK,
        AF_ASH as AF_ASH,
        AF_ATMPVC as AF_ATMPVC,
        AF_ATMSVC as AF_ATMSVC,
        AF_AX25 as AF_AX25,
        AF_BLUETOOTH as AF_BLUETOOTH,
        AF_BRIDGE as AF_BRIDGE,
        AF_CAN as AF_CAN,
        AF_ECONET as AF_ECONET,
        AF_INET as AF_INET,
        AF_INET6 as AF_INET6,
        AF_IPX as AF_IPX,
        AF_IRDA as AF_IRDA,
        AF_KEY as AF_KEY,
        AF_LINK as AF_LINK,
        AF_LLC as AF_LLC,
        AF_NETBEUI as AF_NETBEUI,
        AF_NETLINK as AF_NETLINK,
        AF_NETROM as AF_NETROM,
        AF_PACKET as AF_PACKET,
        AF_PPPOX as AF_PPPOX,
        AF_QIPCRTR as AF_QIPCRTR,
        AF_RDS as AF_RDS,
        AF_ROSE as AF_ROSE,
        AF_ROUTE as AF_ROUTE,
        AF_SECURITY as AF_SECURITY,
        AF_SNA as AF_SNA,
        AF_SYSTEM as AF_SYSTEM,
        AF_TIPC as AF_TIPC,
        AF_UNIX as AF_UNIX,
        AF_UNSPEC as AF_UNSPEC,
        AF_VSOCK as AF_VSOCK,
        AF_WANPIPE as AF_WANPIPE,
        AF_X25 as AF_X25,
        AI_ADDRCONFIG as AI_ADDRCONFIG,
        AI_ALL as AI_ALL,
        AI_CANONNAME as AI_CANONNAME,
        AI_DEFAULT as AI_DEFAULT,
        AI_MASK as AI_MASK,
        AI_NUMERICHOST as AI_NUMERICHOST,
        AI_NUMERICSERV as AI_NUMERICSERV,
        AI_PASSIVE as AI_PASSIVE,
        AI_V4MAPPED as AI_V4MAPPED,
        AI_V4MAPPED_CFG as AI_V4MAPPED_CFG,
        ALG_OP_DECRYPT as ALG_OP_DECRYPT,
        ALG_OP_ENCRYPT as ALG_OP_ENCRYPT,
        ALG_OP_SIGN as ALG_OP_SIGN,
        ALG_OP_VERIFY as ALG_OP_VERIFY,
        ALG_SET_AEAD_ASSOCLEN as ALG_SET_AEAD_ASSOCLEN,
        ALG_SET_AEAD_AUTHSIZE as ALG_SET_AEAD_AUTHSIZE,
        ALG_SET_IV as ALG_SET_IV,
        ALG_SET_KEY as ALG_SET_KEY,
        ALG_SET_OP as ALG_SET_OP,
        ALG_SET_PUBKEY as ALG_SET_PUBKEY,
        BDADDR_ANY as BDADDR_ANY,
        BDADDR_LOCAL as BDADDR_LOCAL,
        BTPROTO_HCI as BTPROTO_HCI,
        BTPROTO_L2CAP as BTPROTO_L2CAP,
        BTPROTO_RFCOMM as BTPROTO_RFCOMM,
        BTPROTO_SCO as BTPROTO_SCO,
        CAN_BCM as CAN_BCM,
        CAN_BCM_CAN_FD_FRAME as CAN_BCM_CAN_FD_FRAME,
        CAN_BCM_RX_ANNOUNCE_RESUME as CAN_BCM_RX_ANNOUNCE_RESUME,
        CAN_BCM_RX_CHANGED as CAN_BCM_RX_CHANGED,
        CAN_BCM_RX_CHECK_DLC as CAN_BCM_RX_CHECK_DLC,
        CAN_BCM_RX_DELETE as CAN_BCM_RX_DELETE,
        CAN_BCM_RX_FILTER_ID as CAN_BCM_RX_FILTER_ID,
        CAN_BCM_RX_NO_AUTOTIMER as CAN_BCM_RX_NO_AUTOTIMER,
        CAN_BCM_RX_READ as CAN_BCM_RX_READ,
        CAN_BCM_RX_RTR_FRAME as CAN_BCM_RX_RTR_FRAME,
        CAN_BCM_RX_SETUP as CAN_BCM_RX_SETUP,
        CAN_BCM_RX_STATUS as CAN_BCM_RX_STATUS,
        CAN_BCM_RX_TIMEOUT as CAN_BCM_RX_TIMEOUT,
        CAN_BCM_SETTIMER as CAN_BCM_SETTIMER,
        CAN_BCM_STARTTIMER as CAN_BCM_STARTTIMER,
        CAN_BCM_TX_ANNOUNCE as CAN_BCM_TX_ANNOUNCE,
        CAN_BCM_TX_COUNTEVT as CAN_BCM_TX_COUNTEVT,
        CAN_BCM_TX_CP_CAN_ID as CAN_BCM_TX_CP_CAN_ID,
        CAN_BCM_TX_DELETE as CAN_BCM_TX_DELETE,
        CAN_BCM_TX_EXPIRED as CAN_BCM_TX_EXPIRED,
        CAN_BCM_TX_READ as CAN_BCM_TX_READ,
        CAN_BCM_TX_RESET_MULTI_IDX as CAN_BCM_TX_RESET_MULTI_IDX,
        CAN_BCM_TX_SEND as CAN_BCM_TX_SEND,
        CAN_BCM_TX_SETUP as CAN_BCM_TX_SETUP,
        CAN_BCM_TX_STATUS as CAN_BCM_TX_STATUS,
        CAN_EFF_FLAG as CAN_EFF_FLAG,
        CAN_EFF_MASK as CAN_EFF_MASK,
        CAN_ERR_FLAG as CAN_ERR_FLAG,
        CAN_ERR_MASK as CAN_ERR_MASK,
        CAN_ISOTP as CAN_ISOTP,
        CAN_J1939 as CAN_J1939,
        CAN_RAW as CAN_RAW,
        CAN_RAW_ERR_FILTER as CAN_RAW_ERR_FILTER,
        CAN_RAW_FD_FRAMES as CAN_RAW_FD_FRAMES,
        CAN_RAW_FILTER as CAN_RAW_FILTER,
        CAN_RAW_JOIN_FILTERS as CAN_RAW_JOIN_FILTERS,
        CAN_RAW_LOOPBACK as CAN_RAW_LOOPBACK,
        CAN_RAW_RECV_OWN_MSGS as CAN_RAW_RECV_OWN_MSGS,
        CAN_RTR_FLAG as CAN_RTR_FLAG,
        CAN_SFF_MASK as CAN_SFF_MASK,
        CAPI as CAPI,
        CMSG_LEN as CMSG_LEN,
        CMSG_SPACE as CMSG_SPACE,
        EAGAIN as EAGAIN,
        EAI_ADDRFAMILY as EAI_ADDRFAMILY,
        EAI_AGAIN as EAI_AGAIN,
        EAI_BADFLAGS as EAI_BADFLAGS,
        EAI_BADHINTS as EAI_BADHINTS,
        EAI_FAIL as EAI_FAIL,
        EAI_FAMILY as EAI_FAMILY,
        EAI_MAX as EAI_MAX,
        EAI_MEMORY as EAI_MEMORY,
        EAI_NODATA as EAI_NODATA,
        EAI_NONAME as EAI_NONAME,
        EAI_OVERFLOW as EAI_OVERFLOW,
        EAI_PROTOCOL as EAI_PROTOCOL,
        EAI_SERVICE as EAI_SERVICE,
        EAI_SOCKTYPE as EAI_SOCKTYPE,
        EAI_SYSTEM as EAI_SYSTEM,
        EBADF as EBADF,
        ETH_P_ALL as ETH_P_ALL,
        ETHERTYPE_ARP as ETHERTYPE_ARP,
        ETHERTYPE_IP as ETHERTYPE_IP,
        ETHERTYPE_IPV6 as ETHERTYPE_IPV6,
        ETHERTYPE_VLAN as ETHERTYPE_VLAN,
        EWOULDBLOCK as EWOULDBLOCK,
        FD_ACCEPT as FD_ACCEPT,
        FD_CLOSE as FD_CLOSE,
        FD_CLOSE_BIT as FD_CLOSE_BIT,
        FD_CONNECT as FD_CONNECT,
        FD_CONNECT_BIT as FD_CONNECT_BIT,
        FD_READ as FD_READ,
        FD_SETSIZE as FD_SETSIZE,
        FD_WRITE as FD_WRITE,
        HCI_DATA_DIR as HCI_DATA_DIR,
        HCI_FILTER as HCI_FILTER,
        HCI_TIME_STAMP as HCI_TIME_STAMP,
        INADDR_ALLHOSTS_GROUP as INADDR_ALLHOSTS_GROUP,
        INADDR_ANY as INADDR_ANY,
        INADDR_BROADCAST as INADDR_BROADCAST,
        INADDR_LOOPBACK as INADDR_LOOPBACK,
        INADDR_MAX_LOCAL_GROUP as INADDR_MAX_LOCAL_GROUP,
        INADDR_NONE as INADDR_NONE,
        INADDR_UNSPEC_GROUP as INADDR_UNSPEC_GROUP,
        INFINITE as INFINITE,
        IOCTL_VM_SOCKETS_GET_LOCAL_CID as IOCTL_VM_SOCKETS_GET_LOCAL_CID,
        IP_ADD_MEMBERSHIP as IP_ADD_MEMBERSHIP,
        IP_ADD_SOURCE_MEMBERSHIP as IP_ADD_SOURCE_MEMBERSHIP,
        IP_BLOCK_SOURCE as IP_BLOCK_SOURCE,
        IP_DEFAULT_MULTICAST_LOOP as IP_DEFAULT_MULTICAST_LOOP,
        IP_DEFAULT_MULTICAST_TTL as IP_DEFAULT_MULTICAST_TTL,
        IP_DROP_MEMBERSHIP as IP_DROP_MEMBERSHIP,
        IP_DROP_SOURCE_MEMBERSHIP as IP_DROP_SOURCE_MEMBERSHIP,
        IP_HDRINCL as IP_HDRINCL,
        IP_MAX_MEMBERSHIPS as IP_MAX_MEMBERSHIPS,
        IP_MULTICAST_IF as IP_MULTICAST_IF,
        IP_MULTICAST_LOOP as IP_MULTICAST_LOOP,
        IP_MULTICAST_TTL as IP_MULTICAST_TTL,
        IP_OPTIONS as IP_OPTIONS,
        IP_PKTINFO as IP_PKTINFO,
        IP_RECVDSTADDR as IP_RECVDSTADDR,
        IP_RECVOPTS as IP_RECVOPTS,
        IP_RECVRETOPTS as IP_RECVRETOPTS,
        IP_RECVTOS as IP_RECVTOS,
        IP_RETOPTS as IP_RETOPTS,
        IP_TOS as IP_TOS,
        IP_TRANSPARENT as IP_TRANSPARENT,
        IP_TTL as IP_TTL,
        IP_UNBLOCK_SOURCE as IP_UNBLOCK_SOURCE,
        IPPORT_RESERVED as IPPORT_RESERVED,
        IPPORT_USERRESERVED as IPPORT_USERRESERVED,
        IPPROTO_AH as IPPROTO_AH,
        IPPROTO_CBT as IPPROTO_CBT,
        IPPROTO_DSTOPTS as IPPROTO_DSTOPTS,
        IPPROTO_EGP as IPPROTO_EGP,
        IPPROTO_EON as IPPROTO_EON,
        IPPROTO_ESP as IPPROTO_ESP,
        IPPROTO_FRAGMENT as IPPROTO_FRAGMENT,
        IPPROTO_GGP as IPPROTO_GGP,
        IPPROTO_GRE as IPPROTO_GRE,
        IPPROTO_HELLO as IPPROTO_HELLO,
        IPPROTO_HOPOPTS as IPPROTO_HOPOPTS,
        IPPROTO_ICLFXBM as IPPROTO_ICLFXBM,
        IPPROTO_ICMP as IPPROTO_ICMP,
        IPPROTO_ICMPV6 as IPPROTO_ICMPV6,
        IPPROTO_IDP as IPPROTO_IDP,
        IPPROTO_IGMP as IPPROTO_IGMP,
        IPPROTO_IGP as IPPROTO_IGP,
        IPPROTO_IP as IPPROTO_IP,
        IPPROTO_IPCOMP as IPPROTO_IPCOMP,
        IPPROTO_IPIP as IPPROTO_IPIP,
        IPPROTO_IPV4 as IPPROTO_IPV4,
        IPPROTO_IPV6 as IPPROTO_IPV6,
        IPPROTO_L2TP as IPPROTO_L2TP,
        IPPROTO_MAX as IPPROTO_MAX,
        IPPROTO_MOBILE as IPPROTO_MOBILE,
        IPPROTO_MPTCP as IPPROTO_MPTCP,
        IPPROTO_ND as IPPROTO_ND,
        IPPROTO_NONE as IPPROTO_NONE,
        IPPROTO_PGM as IPPROTO_PGM,
        IPPROTO_PIM as IPPROTO_PIM,
        IPPROTO_PUP as IPPROTO_PUP,
        IPPROTO_RAW as IPPROTO_RAW,
        IPPROTO_RDP as IPPROTO_RDP,
        IPPROTO_ROUTING as IPPROTO_ROUTING,
        IPPROTO_RSVP as IPPROTO_RSVP,
        IPPROTO_SCTP as IPPROTO_SCTP,
        IPPROTO_ST as IPPROTO_ST,
        IPPROTO_TCP as IPPROTO_TCP,
        IPPROTO_TP as IPPROTO_TP,
        IPPROTO_UDP as IPPROTO_UDP,
        IPPROTO_UDPLITE as IPPROTO_UDPLITE,
        IPPROTO_XTP as IPPROTO_XTP,
        IPV6_CHECKSUM as IPV6_CHECKSUM,
        IPV6_DONTFRAG as IPV6_DONTFRAG,
        IPV6_DSTOPTS as IPV6_DSTOPTS,
        IPV6_HOPLIMIT as IPV6_HOPLIMIT,
        IPV6_HOPOPTS as IPV6_HOPOPTS,
        IPV6_JOIN_GROUP as IPV6_JOIN_GROUP,
        IPV6_LEAVE_GROUP as IPV6_LEAVE_GROUP,
        IPV6_MULTICAST_HOPS as IPV6_MULTICAST_HOPS,
        IPV6_MULTICAST_IF as IPV6_MULTICAST_IF,
        IPV6_MULTICAST_LOOP as IPV6_MULTICAST_LOOP,
        IPV6_NEXTHOP as IPV6_NEXTHOP,
        IPV6_PATHMTU as IPV6_PATHMTU,
        IPV6_PKTINFO as IPV6_PKTINFO,
        IPV6_RECVDSTOPTS as IPV6_RECVDSTOPTS,
        IPV6_RECVHOPLIMIT as IPV6_RECVHOPLIMIT,
        IPV6_RECVHOPOPTS as IPV6_RECVHOPOPTS,
        IPV6_RECVPATHMTU as IPV6_RECVPATHMTU,
        IPV6_RECVPKTINFO as IPV6_RECVPKTINFO,
        IPV6_RECVRTHDR as IPV6_RECVRTHDR,
        IPV6_RECVTCLASS as IPV6_RECVTCLASS,
        IPV6_RTHDR as IPV6_RTHDR,
        IPV6_RTHDR_TYPE_0 as IPV6_RTHDR_TYPE_0,
        IPV6_RTHDRDSTOPTS as IPV6_RTHDRDSTOPTS,
        IPV6_TCLASS as IPV6_TCLASS,
        IPV6_UNICAST_HOPS as IPV6_UNICAST_HOPS,
        IPV6_USE_MIN_MTU as IPV6_USE_MIN_MTU,
        IPV6_V6ONLY as IPV6_V6ONLY,
        J1939_EE_INFO_NONE as J1939_EE_INFO_NONE,
        J1939_EE_INFO_TX_ABORT as J1939_EE_INFO_TX_ABORT,
        J1939_FILTER_MAX as J1939_FILTER_MAX,
        J1939_IDLE_ADDR as J1939_IDLE_ADDR,
        J1939_MAX_UNICAST_ADDR as J1939_MAX_UNICAST_ADDR,
        J1939_NLA_BYTES_ACKED as J1939_NLA_BYTES_ACKED,
        J1939_NLA_PAD as J1939_NLA_PAD,
        J1939_NO_ADDR as J1939_NO_ADDR,
        J1939_NO_NAME as J1939_NO_NAME,
        J1939_NO_PGN as J1939_NO_PGN,
        J1939_PGN_ADDRESS_CLAIMED as J1939_PGN_ADDRESS_CLAIMED,
        J1939_PGN_ADDRESS_COMMANDED as J1939_PGN_ADDRESS_COMMANDED,
        J1939_PGN_MAX as J1939_PGN_MAX,
        J1939_PGN_PDU1_MAX as J1939_PGN_PDU1_MAX,
        J1939_PGN_REQUEST as J1939_PGN_REQUEST,
        LOCAL_PEERCRED as LOCAL_PEERCRED,
        MSG_BCAST as MSG_BCAST,
        MSG_CMSG_CLOEXEC as MSG_CMSG_CLOEXEC,
        MSG_CONFIRM as MSG_CONFIRM,
        MSG_CTRUNC as MSG_CTRUNC,
        MSG_DONTROUTE as MSG_DONTROUTE,
        MSG_DONTWAIT as MSG_DONTWAIT,
        MSG_EOF as MSG_EOF,
        MSG_EOR as MSG_EOR,
        MSG_ERRQUEUE as MSG_ERRQUEUE,
        MSG_FASTOPEN as MSG_FASTOPEN,
        MSG_MCAST as MSG_MCAST,
        MSG_MORE as MSG_MORE,
        MSG_NOSIGNAL as MSG_NOSIGNAL,
        MSG_NOTIFICATION as MSG_NOTIFICATION,
        MSG_OOB as MSG_OOB,
        MSG_PEEK as MSG_PEEK,
        MSG_TRUNC as MSG_TRUNC,
        MSG_WAITALL as MSG_WAITALL,
        NETLINK_CRYPTO as NETLINK_CRYPTO,
        NETLINK_DNRTMSG as NETLINK_DNRTMSG,
        NETLINK_FIREWALL as NETLINK_FIREWALL,
        NETLINK_IP6_FW as NETLINK_IP6_FW,
        NETLINK_NFLOG as NETLINK_NFLOG,
        NETLINK_ROUTE as NETLINK_ROUTE,
        NETLINK_USERSOCK as NETLINK_USERSOCK,
        NETLINK_XFRM as NETLINK_XFRM,
        NI_DGRAM as NI_DGRAM,
        NI_MAXHOST as NI_MAXHOST,
        NI_MAXSERV as NI_MAXSERV,
        NI_NAMEREQD as NI_NAMEREQD,
        NI_NOFQDN as NI_NOFQDN,
        NI_NUMERICHOST as NI_NUMERICHOST,
        NI_NUMERICSERV as NI_NUMERICSERV,
        PACKET_BROADCAST as PACKET_BROADCAST,
        PACKET_FASTROUTE as PACKET_FASTROUTE,
        PACKET_HOST as PACKET_HOST,
        PACKET_LOOPBACK as PACKET_LOOPBACK,
        PACKET_MULTICAST as PACKET_MULTICAST,
        PACKET_OTHERHOST as PACKET_OTHERHOST,
        PACKET_OUTGOING as PACKET_OUTGOING,
        PF_CAN as PF_CAN,
        PF_PACKET as PF_PACKET,
        PF_RDS as PF_RDS,
        PF_SYSTEM as PF_SYSTEM,
        POLLERR as POLLERR,
        POLLHUP as POLLHUP,
        POLLIN as POLLIN,
        POLLMSG as POLLMSG,
        POLLNVAL as POLLNVAL,
        POLLOUT as POLLOUT,
        POLLPRI as POLLPRI,
        POLLRDBAND as POLLRDBAND,
        POLLRDNORM as POLLRDNORM,
        POLLWRNORM as POLLWRNORM,
        RCVALL_MAX as RCVALL_MAX,
        RCVALL_OFF as RCVALL_OFF,
        RCVALL_ON as RCVALL_ON,
        RCVALL_SOCKETLEVELONLY as RCVALL_SOCKETLEVELONLY,
        SCM_CREDENTIALS as SCM_CREDENTIALS,
        SCM_CREDS as SCM_CREDS,
        SCM_J1939_DEST_ADDR as SCM_J1939_DEST_ADDR,
        SCM_J1939_DEST_NAME as SCM_J1939_DEST_NAME,
        SCM_J1939_ERRQUEUE as SCM_J1939_ERRQUEUE,
        SCM_J1939_PRIO as SCM_J1939_PRIO,
        SCM_RIGHTS as SCM_RIGHTS,
        SHUT_RD as SHUT_RD,
        SHUT_RDWR as SHUT_RDWR,
        SHUT_WR as SHUT_WR,
        SIO_KEEPALIVE_VALS as SIO_KEEPALIVE_VALS,
        SIO_LOOPBACK_FAST_PATH as SIO_LOOPBACK_FAST_PATH,
        SIO_RCVALL as SIO_RCVALL,
        SIOCGIFINDEX as SIOCGIFINDEX,
        SIOCGIFNAME as SIOCGIFNAME,
        SO_ACCEPTCONN as SO_ACCEPTCONN,
        SO_BINDTODEVICE as SO_BINDTODEVICE,
        SO_BROADCAST as SO_BROADCAST,
        SO_DEBUG as SO_DEBUG,
        SO_DOMAIN as SO_DOMAIN,
        SO_DONTROUTE as SO_DONTROUTE,
        SO_ERROR as SO_ERROR,
        SO_EXCLUSIVEADDRUSE as SO_EXCLUSIVEADDRUSE,
        SO_INCOMING_CPU as SO_INCOMING_CPU,
        SO_J1939_ERRQUEUE as SO_J1939_ERRQUEUE,
        SO_J1939_FILTER as SO_J1939_FILTER,
        SO_J1939_PROMISC as SO_J1939_PROMISC,
        SO_J1939_SEND_PRIO as SO_J1939_SEND_PRIO,
        SO_KEEPALIVE as SO_KEEPALIVE,
        SO_LINGER as SO_LINGER,
        SO_MARK as SO_MARK,
        SO_OOBINLINE as SO_OOBINLINE,
        SO_PASSCRED as SO_PASSCRED,
        SO_PASSSEC as SO_PASSSEC,
        SO_PEERCRED as SO_PEERCRED,
        SO_PEERSEC as SO_PEERSEC,
        SO_PRIORITY as SO_PRIORITY,
        SO_PROTOCOL as SO_PROTOCOL,
        SO_RCVBUF as SO_RCVBUF,
        SO_RCVLOWAT as SO_RCVLOWAT,
        SO_RCVTIMEO as SO_RCVTIMEO,
        SO_REUSEADDR as SO_REUSEADDR,
        SO_REUSEPORT as SO_REUSEPORT,
        SO_SETFIB as SO_SETFIB,
        SO_SNDBUF as SO_SNDBUF,
        SO_SNDLOWAT as SO_SNDLOWAT,
        SO_SNDTIMEO as SO_SNDTIMEO,
        SO_TYPE as SO_TYPE,
        SO_USELOOPBACK as SO_USELOOPBACK,
        SO_VM_SOCKETS_BUFFER_MAX_SIZE as SO_VM_SOCKETS_BUFFER_MAX_SIZE,
        SO_VM_SOCKETS_BUFFER_MIN_SIZE as SO_VM_SOCKETS_BUFFER_MIN_SIZE,
        SO_VM_SOCKETS_BUFFER_SIZE as SO_VM_SOCKETS_BUFFER_SIZE,
        SOCK_CLOEXEC as SOCK_CLOEXEC,
        SOCK_DGRAM as SOCK_DGRAM,
        SOCK_NONBLOCK as SOCK_NONBLOCK,
        SOCK_RAW as SOCK_RAW,
        SOCK_RDM as SOCK_RDM,
        SOCK_SEQPACKET as SOCK_SEQPACKET,
        SOCK_STREAM as SOCK_STREAM,
        SOL_ALG as SOL_ALG,
        SOL_CAN_BASE as SOL_CAN_BASE,
        SOL_CAN_RAW as SOL_CAN_RAW,
        SOL_HCI as SOL_HCI,
        SOL_IP as SOL_IP,
        SOL_RDS as SOL_RDS,
        SOL_SOCKET as SOL_SOCKET,
        SOL_TCP as SOL_TCP,
        SOL_TIPC as SOL_TIPC,
        SOL_UDP as SOL_UDP,
        SOMAXCONN as SOMAXCONN,
        SYSPROTO_CONTROL as SYSPROTO_CONTROL,
        TCP_CC_INFO as TCP_CC_INFO,
        TCP_CONGESTION as TCP_CONGESTION,
        TCP_CORK as TCP_CORK,
        TCP_DEFER_ACCEPT as TCP_DEFER_ACCEPT,
        TCP_FASTOPEN as TCP_FASTOPEN,
        TCP_FASTOPEN_CONNECT as TCP_FASTOPEN_CONNECT,
        TCP_FASTOPEN_KEY as TCP_FASTOPEN_KEY,
        TCP_FASTOPEN_NO_COOKIE as TCP_FASTOPEN_NO_COOKIE,
        TCP_INFO as TCP_INFO,
        TCP_INQ as TCP_INQ,
        TCP_KEEPALIVE as TCP_KEEPALIVE,
        TCP_KEEPCNT as TCP_KEEPCNT,
        TCP_KEEPIDLE as TCP_KEEPIDLE,
        TCP_KEEPINTVL as TCP_KEEPINTVL,
        TCP_LINGER2 as TCP_LINGER2,
        TCP_MAXSEG as TCP_MAXSEG,
        TCP_MD5SIG as TCP_MD5SIG,
        TCP_MD5SIG_EXT as TCP_MD5SIG_EXT,
        TCP_NODELAY as TCP_NODELAY,
        TCP_NOTSENT_LOWAT as TCP_NOTSENT_LOWAT,
        TCP_QUEUE_SEQ as TCP_QUEUE_SEQ,
        TCP_QUICKACK as TCP_QUICKACK,
        TCP_REPAIR as TCP_REPAIR,
        TCP_REPAIR_OPTIONS as TCP_REPAIR_OPTIONS,
        TCP_REPAIR_QUEUE as TCP_REPAIR_QUEUE,
        TCP_REPAIR_WINDOW as TCP_REPAIR_WINDOW,
        TCP_SAVE_SYN as TCP_SAVE_SYN,
        TCP_SAVED_SYN as TCP_SAVED_SYN,
        TCP_SYNCNT as TCP_SYNCNT,
        TCP_THIN_DUPACK as TCP_THIN_DUPACK,
        TCP_THIN_LINEAR_TIMEOUTS as TCP_THIN_LINEAR_TIMEOUTS,
        TCP_TIMESTAMP as TCP_TIMESTAMP,
        TCP_TX_DELAY as TCP_TX_DELAY,
        TCP_ULP as TCP_ULP,
        TCP_USER_TIMEOUT as TCP_USER_TIMEOUT,
        TCP_WINDOW_CLAMP as TCP_WINDOW_CLAMP,
        TCP_ZEROCOPY_RECEIVE as TCP_ZEROCOPY_RECEIVE,
        TIPC_ADDR_ID as TIPC_ADDR_ID,
        TIPC_ADDR_NAME as TIPC_ADDR_NAME,
        TIPC_ADDR_NAMESEQ as TIPC_ADDR_NAMESEQ,
        TIPC_CFG_SRV as TIPC_CFG_SRV,
        TIPC_CLUSTER_SCOPE as TIPC_CLUSTER_SCOPE,
        TIPC_CONN_TIMEOUT as TIPC_CONN_TIMEOUT,
        TIPC_CRITICAL_IMPORTANCE as TIPC_CRITICAL_IMPORTANCE,
        TIPC_DEST_DROPPABLE as TIPC_DEST_DROPPABLE,
        TIPC_HIGH_IMPORTANCE as TIPC_HIGH_IMPORTANCE,
        TIPC_IMPORTANCE as TIPC_IMPORTANCE,
        TIPC_LOW_IMPORTANCE as TIPC_LOW_IMPORTANCE,
        TIPC_MEDIUM_IMPORTANCE as TIPC_MEDIUM_IMPORTANCE,
        TIPC_NODE_SCOPE as TIPC_NODE_SCOPE,
        TIPC_PUBLISHED as TIPC_PUBLISHED,
        TIPC_SRC_DROPPABLE as TIPC_SRC_DROPPABLE,
        TIPC_SUB_CANCEL as TIPC_SUB_CANCEL,
        TIPC_SUB_PORTS as TIPC_SUB_PORTS,
        TIPC_SUB_SERVICE as TIPC_SUB_SERVICE,
        TIPC_SUBSCR_TIMEOUT as TIPC_SUBSCR_TIMEOUT,
        TIPC_TOP_SRV as TIPC_TOP_SRV,
        TIPC_WAIT_FOREVER as TIPC_WAIT_FOREVER,
        TIPC_WITHDRAWN as TIPC_WITHDRAWN,
        TIPC_ZONE_SCOPE as TIPC_ZONE_SCOPE,
        UDPLITE_RECV_CSCOV as UDPLITE_RECV_CSCOV,
        UDPLITE_SEND_CSCOV as UDPLITE_SEND_CSCOV,
        VM_SOCKETS_INVALID_VERSION as VM_SOCKETS_INVALID_VERSION,
        VMADDR_CID_ANY as VMADDR_CID_ANY,
        VMADDR_CID_HOST as VMADDR_CID_HOST,
        VMADDR_PORT_ANY as VMADDR_PORT_ANY,
        WSA_FLAG_OVERLAPPED as WSA_FLAG_OVERLAPPED,
        WSA_INVALID_HANDLE as WSA_INVALID_HANDLE,
        WSA_INVALID_PARAMETER as WSA_INVALID_PARAMETER,
        WSA_IO_INCOMPLETE as WSA_IO_INCOMPLETE,
        WSA_IO_PENDING as WSA_IO_PENDING,
        WSA_NOT_ENOUGH_MEMORY as WSA_NOT_ENOUGH_MEMORY,
        WSA_OPERATION_ABORTED as WSA_OPERATION_ABORTED,
        WSA_WAIT_FAILED as WSA_WAIT_FAILED,
        WSA_WAIT_TIMEOUT as WSA_WAIT_TIMEOUT,
    )
