from tooz import coordination

coordinator = coordination.get_coordinator('kazoo://localhost', b'host-1')
coordinator.start()
coordinator.stop()
