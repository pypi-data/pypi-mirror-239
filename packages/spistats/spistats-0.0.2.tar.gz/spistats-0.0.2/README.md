# Installation 
```bash
pip install spistats
```

# Usage
## Collision
```python
import spistats as spi
col = spi.Collision(nbr_dev, nbr_adr, adr_per_dev)
```

## Desynchronization
```python
import spistats.desynchronization as dsync
packet_count = dsync.NumberOfPacketBeforeDsync(0.2,5)
packet_count = dsync.NumberOfPacketBeforeDsync_multi([0.2,0.3],5)
```

## Plotting
```python
import spistats.plot as plt
import spistats.desynchronization as dsync
dsync_count = dsync.NumberOfDsync(0.2,2,10)
plt.cdf(dsync_count)
```

