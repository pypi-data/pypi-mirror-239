import spistats.desynchronization as dsync

packet_count = dsync.NumberOfPacketBeforeDsync(0.2,5)
packet_count.eigenvalues()

median = packet_count.cdf_inv(0.5)

print(median)
print(packet_count.cdf(median))
