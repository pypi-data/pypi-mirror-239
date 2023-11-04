from ..crazy import CrazyDragon

from threading import Thread

from scipy.spatial.transform import Rotation

from .._base._navigation_base.imu       import IMU
from .._base._navigation_base.imu_setup import preflight_sequence
from .._base._navigation_base.qualisys  import Qualisys

from time import sleep



class Navigation( Thread ):

    qtm = -1

    def __init__( self, cf: CrazyDragon ):

        super().__init__()

        self.daemon = True

        self.cf = cf

        self.imu = IMU( cf )

        self.navigate = True


    @classmethod
    def _on_pose( cls, cf: CrazyDragon, data: list ):
        
        cf.pos[:] = data[0:3]

        R = Rotation.from_euler( 'zyx', cf.att[::-1], degrees=True )
        q = R.as_quat()

        cf.rot[:,:] = R.as_matrix()

        cf.extpos.send_extpose( data[0], data[1], data[2], q[0], q[1], q[2], q[3] )


    @classmethod
    def init_qualisys( cls, cfs: dict ):

        cls.qtm = Qualisys( cfs )

        sleep( 1 )

        cls.qtm.on_pose = lambda cf, pose: __class__._on_pose( cf, pose )


    def run( self ):

        cf = self.cf

        imu = self.imu
        qtm = self.qtm

        preflight_sequence( cf )

        sleep( 1 )

        imu.start_get_acc()
        imu.start_get_vel()
        imu.start_get_att()

        qtm.on_pose = lambda pose: __class__._on_pose( cf, pose )

        while self.navigate:

            sleep( 0.1 )


    def join( self ):

        self.navigate = False

        super().join()