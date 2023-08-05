Use NFS as cinder-volume backend driver.

Configuration
-------------

    cinder:
      include_nfs_backend: False
        # set to true to use the nfs backend
      nfs_shares: None
        # a list of nfs shares, each item in the list should be an nfs
        # share address. (e.g 192.0.2.5:/mnt/state/var/lib/nfs_share)

**NOTE:** make sure to use the 'nfs-client' element when building the
compute nodes too.