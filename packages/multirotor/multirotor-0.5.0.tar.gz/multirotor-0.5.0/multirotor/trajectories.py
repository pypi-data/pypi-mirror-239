from typing import Iterable

import numpy as np
try:
    from pyscurve import ScurvePlanner
    from pyscurve.trajectory import PlanningError
except ImportError:
    ScurvePlanner = False
    PlanningError = Exception

from multirotor.simulation import Multirotor



class Trajectory:
    """
    Iterate over waypoints for a multirotor. The trajectory class can segment a
    list of waypoints into smaller sections and feed them to the controller when
    the vehicle is within a radius of its current waypoint.

    For example:

        m = Multirotor(...)
        traj = Trajectory(
            points=[(0,0,0), (0,0,2), (10,0,2)],
            vehicle=m, proximity=0.1, resolution=0.5)
        for point in traj:
            Each point is spaced `resolution` units apart in euclidean distance.
            When m.position is within `proximity` of current point, the next
            point in the trajectory is yielded.
    """


    def __init__(
        self, vehicle: Multirotor, points: np.ndarray, proximity: float=None,
        resolution: float=None    
    ):
        """
        Parameters
        ----------
        vehicle : Multirotor
            The vehicle to track.
        points : np.ndarray
            A list of 3D coordinates.
        proximity : float, optional
            The distance from current waypoint at which to send the next waypoint,
            by default None. If None, simply iterates over provided points.
        resolution : float, optional
            The segmentation of the trajectory, by default None. If provided, it
            is the distance between intermediate points generated from the waypoints
            provided. For e.g. resolution=2 and points=(0,0,0), (10,0,0) will
            create intermediate points a distance 2 apart.
        """
        self.vehicle = vehicle
        if self.vehicle is not None:
            dtype = self.vehicle.dtype
        else:
            dtype = np.float32
        self.points = np.asarray(points, dtype)
        self.proximity = proximity
        self.resolution = resolution
        self.ref = None


    def __len__(self):
        return len(self._points)


    def __getitem__(self, i: int):
        return self._points[i]


    def get_params(self):
        return dict(
            proximity=self.proximity, resolution=self.resolution
        )


    def set_params(self, **params):
        self.proximity = params.get('proximity', self.proximity)
        self.proximity = params.get('resolution', self.resolution)


    def __iter__(self):
        self._points = self.generate_trajectory(self.vehicle.position)
        if self.proximity is not None:
            for i in range(1, len(self)):
                while not self.reached(self[i]):
                    self.ref = self[i]
                    yield self.ref, None
        else:
            for i in range(1, len(self)):
                self.ref = self[i]
                yield self.ref, None


    def generate_trajectory(self, curr_pos=None):
        if curr_pos is not None:
            points = [curr_pos, *self.points]
        else:
            points = self.points
        points = np.asarray([p[:3] for p in points])
        if self.resolution is not None:
            _points = []
            for i, (p1, p2) in enumerate(zip(points[:-1], points[1:])):
                pos_vec = p2 - p1
                dist = np.linalg.norm(pos_vec)
                unit_vec = pos_vec / (dist + 1e-6)
                # num = int(dist / self.resolution) + 1
                number = dist // self.resolution
                remainder  = dist % self.resolution
                pts = p1 + unit_vec * self.resolution * np.arange(0, number+1, step=1).reshape(-1,1)
                if remainder > 0 and i==len(points)-2: # if leftover distance and last point
                    pts = np.concatenate((pts, (p2,)))
                # pts = p1 + unit_vec * np.arange(0, dist + self.resolution, step=self.resolution).reshape(-1,1)
                # _points.extend(np.linspace(p1, p2, num=num, endpoint=True))
                _points.extend(pts)
        else:
            _points = points
        return _points


    def add_waypoint(self, point: np.ndarray):
        pass


    def next_waypoint(self):
        pass


    def reached(self, wp: np.ndarray) -> bool:
        return np.linalg.norm(self.vehicle.position - wp) <= self.proximity



class GuidedTrajectory:
    # Guided mode call stack overview
    # https://ardupilot.org/dev/docs/apmcopter-code-overview.html
    # Square-root controller for pos control, sets P value
    # https://github.com/ArduPilot/ardupilot/blob/master/libraries/AP_Math/control.cpp#L286

    def __init__(self, vehicle: Multirotor, waypoints: Iterable[np.ndarray],
        steps: int=10, proximity: float=2., max_velocity: float=7., max_acceleration: float=3.,
        max_jerk: float=100, turn_factor: float=(1/np.sqrt(2))) -> None:
        if not ScurvePlanner:
            raise ImportError('Py-Scurve is not installed.')
        self.vehicle = vehicle
        self.waypoints = np.asarray(waypoints)
        self.steps = int(steps)
        self.proximity = float(proximity)
        self.max_velocity = float(max_velocity)
        self.max_acceleration = float(max_acceleration)
        self.max_jerk = float(max_jerk)
        self.turn_factor = turn_factor
        self.trajectory = None
        self.trajs = []


    def _setup(self):
        if self.steps is None:
            dt = self.vehicle.simulation.dt
            # default run at 100Hz
            self.steps = int(max(1, 0.01 / dt))


    def __iter__(self):
        # https://www.youtube.com/watch?v=MQiNDJGJDWs
        self._setup()
        i = 0 # steps since beginning of trajectory
        j = 0 # steps since last trajectory replan
        k = 0 # waypoint index
        planner = ScurvePlanner(debug=False)
        self._ref = None
        for k, wp in enumerate(self.waypoints):
            replan = True # new waypoint, so replan immediately
            while not self.reached(wp):
                # Refresh trajectory plan
                if i % self.steps == 0 or replan:
                    r0 = rx = self.vehicle.position[:2]
                    v0 = vx = self.vehicle.velocity[:2]
                    r1 = wp[:2]
                    # Assume that destination velocity is 0
                    v1 = np.zeros(2)
                    # Unless there is another leg of flight, in which case
                    # target velocity should depend on the sharpness of turn
                    if k < len(self.waypoints)-1:
                        r2 = self.waypoints[k+1][:2]
                        # TODO: should this be the shortest path to the trajectory
                        # instead of the next waypoint? I.e prioritize returning
                        # to planned path, instead of taking the shortest diagonal path
                        # to the destination?
                        r01 = r1 - r0 # current desired heading vector
                        # r01 = v0
                        r12 = r2 - r1 # next desired heading vector
                        r01_ = r01 / np.linalg.norm(r01)
                        r12_ = r12 / np.linalg.norm(r12)
                        # Projection of vectors along current leg. If projection is <0,
                        # means vehicle needs to reverse. So clip to 0 so it comes
                        # to a stop at the waypoint.
                        projection = max(0, np.dot(r12_, r01_))
                        v1 = self.max_velocity * self.turn_factor * projection * r01_
                    try:
                        self.trajectory = planner.plan_trajectory(
                            q0=r0, q1=r1, v0=v0, v1=v1,
                            v_max=max(self.max_velocity, np.linalg.norm(v0)),
                            a_max=self.max_acceleration,
                            j_max=self.max_jerk
                        )
                        self.trajs.append(self.trajectory)
                        replan = False # once replanned, wait for next waypoint or steps
                        j = 0 # reset steps since replan
                    except PlanningError as e:
                        # If planning error was on a new point/or replanning was
                        # requested. When not choosing to raise exception, trust
                        # that the vehicle can catch up and later on the trajectory
                        # can become feasible again.
                        if replan:
                            # print('r0', r0, 'r1', r1)
                            # print('Err: %s' % e)
                            # raise e
                            pass
                        replan = True # after error, replan at next steps
                # Simulate trajectory plan over time
                for _ in range(self.steps):
                    target = self.trajectory(self.vehicle.simulation.dt * j)
                    point = target[:, 2]
                    velocity = target[:, 1]
                    self._ref = np.concatenate((point, wp[2:], [0])) # position, yaw
                    i += 1 # steps since beginning of trajectory
                    j += 1 # steps since last trajectory replan
                    yield self._ref, velocity


    def reached(self, wp: np.ndarray) -> bool:
        return np.linalg.norm(self.vehicle.position - wp) <= self.proximity



def eight_curve(a: float=10, N:int=20) -> np.ndarray:
    """
    Generate a list of points following the Eight curve pattern.

    Parameters
    ----------
    a : int, optional
        The scale of the curve, by default 50
    N : int, optional
        Number of points to generate, by default 20

    Returns
    -------
    np.ndarray
        A Nx3 array of points.
    """
    wp = np.zeros((N, 3), np.float32)
    t = np.linspace(0, 2 * np.pi, N)
    wp[:,0] = a * np.sin(t)
    wp[:,1] = a * np.sin(t) * np.cos(t)
    wp[:,2] = np.zeros(N)
    return wp
